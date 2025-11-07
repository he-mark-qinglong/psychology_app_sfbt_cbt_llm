from flask import render_template, jsonify, request, send_file  
from app import app  
from app.user_manager import UserManager  
from functools import wraps  
from typing import Dict, Any  
import logging  
import tempfile  
import os  
import io  
import json
from app.config import therapy_config
# 配置日志  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  

# 初始化用户管理器  
user_manager = UserManager()  

#单独放置是因为没尝试解决appconfig无法进行字典存储的现象，临时绕过去了该问题。
user_manager.init_config(app.config, therapy_config(app))  
# 添加文件上传大小限制配置  
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB  

def create_response(success: bool, data: Dict[str, Any] = None, error: str = None, status_code: int = 200) -> tuple:  
    """统一的响应创建函数"""  
    response = {  
        "success": success,  
        **({"data": data} if data is not None else {}),  
        **({"error": error} if error is not None else {})  
    }  
    return jsonify(response), status_code  

def error_handler(f):  
    """错误处理装饰器"""  
    @wraps(f)  
    def decorated_function(*args, **kwargs):  
        data = request.get_data()
        print('request error, data: ', data)
        try:  
            return f(*args, **kwargs)  
        except Exception as e:  
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)  
            return create_response(False, error=str(e), status_code=500)  
    return decorated_function  

def can_change_content(request_data):
    username = None  
    if isinstance(request_data, dict):  
        username = request_data.get('username')
    # 如果是 Flask request 对象且包含 JSON 数据  
    elif hasattr(request_data, 'data') and request_data.data:  
        try:  
            # 解析 JSON 数据  
            json_data = json.loads(request_data.data)  
            username = json_data.get('username')  
        except json.JSONDecodeError:  
            logger.error("Failed to parse JSON data") 

    elif hasattr(request_data, 'args'):  
        username = request_data.args.get('username')  
    
    if not username:  
        username = 'default_user'

    # if not username != 'smark':
    #     return False
    
    return True

def get_user_system(request_data):  
    """获取用户系统，如果不存在则创建新用户"""  
    username = None  
    if isinstance(request_data, dict):  
        username = request_data.get('username')
    # 如果是 Flask request 对象且包含 JSON 数据  
    elif hasattr(request_data, 'data') and request_data.data:  
        try:  
            # 解析 JSON 数据  
            json_data = json.loads(request_data.data)  
            username = json_data.get('username')  
        except json.JSONDecodeError:  
            logger.error("Failed to parse JSON data") 

    elif hasattr(request_data, 'args'):  
        username = request_data.args.get('username')  
    
    if not username:  
        username = 'default_user'  
    
    therapy_system = user_manager.get_user_system(username)  
    if not therapy_system:  
        # why:这里是为了临时处理没有相应的用户的问题，但是：
        # 这里不应该发生的，因为只有一个地方添加用户--->set_username
        user = user_manager.add_user(username, 'sfbt')  
        therapy_system = user.therapy_system  
    
    return therapy_system  

# 页面路由  
@app.route('/')  
@error_handler  
def index():  
    """渲染主页"""  
    # 为默认用户创建新的系统实例  
    user = user_manager.add_user('default_user')  
    return render_template('chat.html')  

# 页面路由  
@app.route('/login')  
@error_handler  
def login():  
    """渲染主页"""  
    # 为默认用户创建新的系统实例  
    user = user_manager.add_user('default_user')  
    return render_template('echo_psycho_login.html')  

@app.route('/voice.html')  
@error_handler  
def voice():  
    """渲染语音页面"""  
    return render_template('voice.html')  

@app.route('/phone')  
@error_handler  
def phone():  
    """渲染手机页面"""  
    user = user_manager.add_user('default_user')  
    return render_template('phone.html')  

# API 路由  
@app.route('/set_username', methods=['POST'])  
@error_handler  
def set_username():  
    """设置用户名"""  
    data = request.json  
    username = data.get('username')  
    
    if not username or len(username.strip()) < 2:  
        return create_response(False, error="Invalid username", status_code=400)  
    
    username = username.strip()  
    try:  
        user = user_manager.add_user(username, 
        type=app.config['NORMAL_PSYCHOLOGY_METHOD'])  
        return create_response(True, data={"username": username})  
    except Exception as e:  
        logger.error(f"Error creating user: {str(e)}")  
        return create_response(False, error="Failed to create user", status_code=500)  

@app.route('/logout_user', methods=['POST'])  
@error_handler  
def logout_user():  
    """注销用户的 therapy_system"""  
    data = request.json  
    username = data.get('username')  
    
    if not username:  
        return create_response(False, error="No username provided", status_code=400)  
    
    try:  
        # 从 user_manager 中删除用户  
        success = user_manager.remove_user(username)  
        return create_response(success, data={"message": "User logged out successfully"})  
    except Exception as e:  
        logger.error(f"Error logging out user: {str(e)}")  
        return create_response(False, error="Failed to logout user", status_code=500)
    
@app.route('/chat', methods=['POST'])  
@error_handler  
def chat():  
    """处理聊天请求"""  
    data = request.json  
    user_message = data.get('message')  
    
    if not user_message:  
        return create_response(False, error="No message provided", status_code=400)  
        
    therapy_system = get_user_system(data)  
    result = therapy_system.get_response(user_message)  
    
    if result['success']:  
        return create_response(True, data={  
            "response": result['response'],  
            "history": result['history'],  
            "current_stage": result['current_stage'],  
            "current_task": result['current_task'],  
            "stage_changed": result['stage_changed']  
        })  
    else:  
        return create_response(False, error=result['error'], status_code=500)  

@app.route('/get_all_stages', methods=['GET', 'POST'])  
@error_handler  
def get_all_stages():  
    """获取所有阶段"""  
    therapy_system = get_user_system(request)  
    current_stage_info = therapy_system.get_current_stage()  
    stages = therapy_system.get_all_stages()
    
    return create_response(True, data={  
        "stages": stages,  
        "current_stage": {  
            "id": therapy_system.current_stage,  
            "info": current_stage_info,  
            "current_task": therapy_system.current_task  
        }  
    })  

@app.route('/get_stage', methods=['GET'])  
@error_handler  
def get_stage():  
    """获取指定阶段的内容"""  
    stage = request.args.get('stage')  
    if not stage:  
        return create_response(False, error="No stage specified", status_code=400)  
    
    therapy_system = get_user_system(request)  
    stage_info = therapy_system.get_stage_content(stage)  
    if stage_info is None:  
        return create_response(False, error="Stage not found", status_code=404)  
    
    current_stage_info = therapy_system.get_current_stage()  
    return create_response(True, data={  
        "stage": stage,  
        "stage_info": stage_info,  
        "current_stage": {  
            "id": therapy_system.current_stage,  
            "info": current_stage_info  
        }  
    })  

@app.route('/set_stage', methods=['POST'])  
@error_handler  
def set_stage():  
    """设置当前阶段"""  
    data = request.json  
    stage = data.get('stage')  
    task_id = data.get('task_id')  
    
    if not stage:  
        return create_response(False, error="No stage specified", status_code=400)  
    
    therapy_system = get_user_system(data)  
    stage_info = therapy_system.get_stage_content(stage)  
    if stage_info is None:  
        return create_response(False, error="Stage not found", status_code=404)  
    
    therapy_system.set_stage(stage, task_id)  
    return create_response(True, data={  
        "current_stage": {  
            "id": stage,  
            "info": stage_info,  
            "current_task": therapy_system.current_task  
        }  
    })  

@app.route('/update_stage', methods=['POST'])  
@error_handler  
def update_stage():  
    """更新阶段内容"""  
    data = request.json  
    stage = data.get('stage')  
    content = data.get('content')  
    
    if not stage or content is None:  
        return create_response(False, error="Missing stage or content", status_code=400)  
    
    required_keys = {"id", "name", "description", "tasks"}  
    if not all(key in content for key in required_keys):  
        return create_response(  
            False,  
            error=f"Content must include all required fields: {', '.join(required_keys)}",  
            status_code=400  
        )  
    if can_change_content(data):
        therapy_system = get_user_system(data)  
        success = therapy_system.update_stage_content(stage, content)  
    else:
        success = False
    if success:  
        return create_response(True, data={  
            "stage": stage,  
            "updated_content": content  
        })  
    else:  
        return create_response(False, error="Failed to update stage content", status_code=500)  

@app.route('/load_history', methods=['GET', 'POST'])  
@error_handler  
def get_history():  
    """获取聊天历史"""  
    therapy_system = get_user_system(request)  
    return create_response(True, data={"history": therapy_system.user_chat_history()})  

@app.route('/api/transcribe', methods=['POST'])  
@error_handler  
def transcribe_audio():  
    """处理语音转文字请求"""  
    if 'file' not in request.files:  
        return create_response(False, error="No file provided", status_code=400)  
    
    audio_file = request.files['file']  
    username = request.form.get('username', 'default_user')  
    therapy_system = get_user_system({'username': username})  
    
    allowed_extensions = {'.webm', '.wav', '.mp3', '.m4a', '.mpga', '.mpeg', '.mp4'}  
    if not audio_file.filename or not any(audio_file.filename.lower().endswith(ext) for ext in allowed_extensions):  
        return create_response(False, error="Invalid audio file format", status_code=400)  

    try:  
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as tmp:  
            audio_file.save(tmp.name)  
            
            with open(tmp.name, 'rb') as audio:  
                transcript = therapy_system.client.audio.transcriptions.create(  
                    model="whisper-1",  
                    file=audio,  
                    response_format="text",  
                    temperature=0  
                )  
            
            os.unlink(tmp.name)  
            result = therapy_system.get_response(transcript)  
            
            if result['success']:  
                return create_response(True, data={  
                    "text": transcript,  
                    "response": result['response'],  
                    "history": result['history'],  
                    "current_stage": result['current_stage'],  
                    "current_task": result['current_task'],  
                    "stage_changed": result['stage_changed']  
                })  
            else:  
                return create_response(False, error=result['error'], status_code=500)  
            
    except Exception as e:  
        logger.error(f"Transcription error: {str(e)}", exc_info=True)  
        return create_response(False, error="Failed to transcribe audio", status_code=500)  

@app.route('/api/tts', methods=['POST'])  
@error_handler  
def text_to_speech():  
    """处理文字转语音请求"""  
    data = request.json  
    if not data or 'text' not in data:  
        return create_response(False, error="No text provided", status_code=400)  
    
    text = data['text']  
    therapy_system = get_user_system(data)  
    
    if len(text) > 4096:  
        return create_response(False, error="Text too long", status_code=400)  

    try:  
        response = therapy_system.client.audio.speech.create(  
            model=data.get('model', 'tts-1'),  
            voice=data.get('voice', 'alloy'),  
            input=text,  
            speed=data.get('speed', 1.0),  
            response_format='mp3'  
        )  
        
        audio_data = io.BytesIO(response.content)  
        audio_data.seek(0)  
        
        return send_file(  
            audio_data,  
            mimetype='audio/mpeg',  
            as_attachment=True,  
            download_name='speech.mp3'  
        )  
        
    except Exception as e:  
        logger.error(f"TTS error: {str(e)}", exc_info=True)  
        return create_response(False, error="Failed to generate speech", status_code=500)  

# 错误处理路由  
@app.errorhandler(404)  
def not_found_error(error):  
    return create_response(False, error="Not found", status_code=404)  

@app.errorhandler(500)  
def internal_error(error):  
    return create_response(False, error="Internal server error", status_code=500)  

@app.errorhandler(413)  
def request_entity_too_large(error):  
    return create_response(False, error="File too large", status_code=413)