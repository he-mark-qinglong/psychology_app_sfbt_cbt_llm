# app/system_base/therapy_system.py  
from pathlib import Path  
import logging  
from typing import Dict, Optional, List  
import json  
import os  
from app.semantic_matcher import SemanticMatcherClient  

logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  

class TherapySystemBase:  
    def __init__(self, stage_file_path: str, prompt_file:str, user: str):  
        logger.info(f'{user}========================')  
        self.stage_file_path = stage_file_path  
        self.prompt_file_path = prompt_file 
        self.history_file_path = str(Path(stage_file_path).parent.parent / 'histories' / f'{user}_chat_history.json')  
        
        self.current_stage: Optional[str] = None  
        self.current_task: Optional[str] = None  
        self.stages_config: Dict = {}  
        self.chat_history: List[Dict] = []  
        self.client = None  
        self.basic_prompt = self.load_basic_prompt()  
        self.hello = ""

        os.makedirs(os.path.dirname(self.stage_file_path), exist_ok=True)  
        
        self.state_machine = self._init_state_machine()  
        self.sematic_matcher = SemanticMatcherClient()  
        
        self.load_stages()  
        self.load_history_from_file()  
        
        if len(self.chat_history) != 0:  
            last_assistant_message = self.chat_history[-1] if self.chat_history[-1]['role'] == 'assistant' else self.chat_history[-2]  
            extracted_stage = self.extract_stage_from_response(last_assistant_message['content'])  
            if extracted_stage:  
                self.set_stage(extracted_stage)  

    # 子类需要实现的方法  
    def _init_state_machine(self):  
        """初始化状态机（由子类实现）"""  
        raise NotImplementedError  

    def _get_initial_message(self) -> str:  
        """获取初始化消息（由子类实现）"""  
        raise NotImplementedError  
 

    # API客户端初始化方法  
    def init_openai(self, api_key: str) -> None:  
        from app.openai_api import OpenAIClient
        self.client = OpenAIClient(api_key=api_key)  

    def init_claude(self, api_key: str):  
        from app.anthropic_api import ClaudeClient  
        self.client = ClaudeClient(api_key=api_key)  

    # 基础提示词加载  
    def load_basic_prompt(self) -> str:  
        try:  
            if not os.path.exists(self.prompt_file_path):  
                logger.warning(f"Basic prompt file not found at {self.prompt_file_path}")  
                return ""  
            
            with open(self.prompt_file_path, 'r', encoding='utf-8') as f:  
                basic_prompt = f.read().strip()  
                print(f'basic_prompt is :{basic_prompt}')
            logger.info("Successfully loaded basic prompt")  
            return basic_prompt  
        except Exception as e:  
            logger.error(f"Error loading basic prompt: {e}")  
            return ""  

    # 阶段管理方法  
    def load_stages(self) -> Dict:  
        try:  
            if not os.path.exists(self.stage_file_path):  
                return {}  

            with open(self.stage_file_path, 'r', encoding='utf-8') as f:  
                config = json.load(f)  
            
            self.stages_config = {stage["id"]: stage for stage in config["stages"]}  
            self.hello = config['hello']

            if not self.current_stage and self.stages_config:  
                first_stage = next(iter(self.stages_config))  
                self.set_stage(first_stage)  
            
            return self.stages_config  
        except Exception as e:  
            logger.error(f"Error loading stages: {e}")  
            return {}  

    def save_stages(self) -> bool:  
        try:  
            config = {  
                "stages": list(self.stages_config.values())  
            }  

            with open(self.stage_file_path, 'w', encoding='utf-8') as f:  
                json.dump(config, f, ensure_ascii=False, indent=2)  
            return True  
        except Exception as e:  
            logger.error(f"Error saving stages: {e}")  
            return False  

    # 历史记录管理方法  
    def load_history_from_file(self) -> bool:  
        try:  
            if os.path.exists(self.history_file_path):  
                with open(self.history_file_path, 'r', encoding='utf-8') as f:  
                    self.chat_history = json.load(f)  
                return True  
            else:  
                # self._get_initial_message()
                self.chat_history = [{"role": "assistant", "content": self.hello}]  
            return False  
        except Exception as e:  
            logger.error(f"Error loading chat history: {e}")  
            return False  

    def save_history_to_file(self) -> bool:  
        try:  
            with open(self.history_file_path, 'w', encoding='utf-8') as f:  
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)  
            return True  
        except Exception as e:  
            logger.error(f"Error saving chat history: {e}")  
            return False  

    # 阶段和任务管理方法  
    def set_stage(self, stage_id: str, task_id: Optional[str] = None) -> bool:  
        if stage_id in self.stages_config:  
            if self.state_machine.transition_to(stage_id):  
                self.current_stage = stage_id  
                logger.info(f'self.current_stage==========={self.current_stage}')  
                stage_config = self.stages_config[stage_id]  
                
                if task_id:  
                    for task in stage_config["tasks"]:  
                        if task["id"] == task_id:  
                            self.current_task = task_id  
                            break  
                elif stage_config["tasks"]:  
                    self.current_task = stage_config["tasks"][0]["id"]  
                return True  
        else:  
            logger.error(f'++++++++++++++++++ state machine is {stage_id}, stage_config is {self.stages_config}')  
            return False  

    def get_current_prompt(self) -> str:  
        logger.info(f"current_state {self.current_stage} \n current_task:{self.current_task}")  
        if not self.current_stage or not self.current_task:  
            return ""  

        stage_config = self.stages_config.get(self.current_stage)  
        if not stage_config:  
            return ""  
        
        stage_prompt = stage_config["description"] + "\n这一步骤就结束了，之后你可以根据聊天内容来自由选择其他的步骤中的任意一个。\n你需要在这个步骤中完成以下任务："  
        for task in stage_config["tasks"]:  
            stage_prompt = stage_prompt + "\n" + task["prompt_template"]  
        return stage_prompt  

    def extract_stage_from_response(self, response: str) -> Optional[str]:  
        logger.info(f'+++++++++++extract_stage_from_response {response}')  
        try:  
            import re  
            stage_pattern = r'>>\[(.*?)\]'  
            matches = re.findall(stage_pattern, response)  
            if matches:  
                extracted_stage = matches[-1]  
                logger.info(f'Matched stage: {extracted_stage}')  
                
                for stage in self.stages_config:  
                    is_similar, score = self.sematic_matcher.get_similarity(  
                        self.stages_config[stage]['name'],   
                        extracted_stage  
                    )  
                    if is_similar:  
                        logger.info(f'return stage:{stage}')  
                        return stage  
                    
                    # 检查任务名称  
                    tasks = self.stages_config[stage]['tasks']  
                    for task in tasks:  
                        is_similar, score = self.sematic_matcher.get_similarity(  
                            task['name'],   
                            extracted_stage  
                        )  
                        if is_similar:  
                            logger.info(f'return stage:{stage}')  
                            return stage  
                            
                logger.warning(f"Extracted stage '{extracted_stage}' not found in defined stages")  
            return None  
        except Exception as e:  
            logger.error(f"Error extracting stage from response: {e}")  
            return None  

    # 响应生成方法  
    def get_response(self, user_message: str) -> Dict:  
        try:  
            if not self.client:  
                return {  
                    'success': False,  
                    'error': 'AI client not initialized'  
                }  

            current_prompt = self.get_current_prompt()  
            messages = []  
            
            if current_prompt:  
                messages.append({  
                    "role": "system",  
                    "content": f"{self.basic_prompt}\n\n{current_prompt}" if self.basic_prompt else current_prompt  
                })  
                logger.info(f'system: {messages[0]["content"]}')  
            
            for msg in self.chat_history:  
                messages.append({  
                    "role": msg["role"],  
                    "content": msg["content"]  
                })  
            
            messages.append({  
                "role": "user",  
                "content": user_message  
            })  

            response = self.client.get_completion(messages=messages)  
            ai_message = response  
            
            extracted_stage = self.extract_stage_from_response(ai_message)  
            stage_changed = False  
            if extracted_stage:  
                self.set_stage(extracted_stage)  
                stage_changed = True  

            self.chat_history.extend([  
                {"role": "user", "content": user_message},  
                {"role": "assistant", "content": ai_message}  
            ])  
            self.save_history_to_file()  
            
            
            return {  
                'success': True,  
                'response': self.split_text_by_marker(ai_message),  
                'history': self.user_chat_history(),  
                'current_stage': self.current_stage,  
                'current_task': self.current_task,  
                'stage_changed': stage_changed  
            }  

        except Exception as e:  
            logger.error(f"Error getting response: {e}")  
            return {  
                'success': False,  
                'error': str(e)  
            }

    # 验证AI回复的有效性并过滤不合适的回复
    def sanitize_ai_response(self, ai_message: str) -> str:
        """
        清理和验证AI回复内容
        """
        if not ai_message or not ai_message.strip():
            return "感谢您的提问。为了更好地帮助您，我需要更具体的信息。请您详细描述一下您想了解的问题。"
        
        # 过滤掉可能的模板占位符内容
        if ("关于'..." in ai_message and "的建议" in ai_message) or \
           ("template" in ai_message.lower()) or \
           ("placeholder" in ai_message.lower()) or \
           (ai_message.strip().startswith(">>>") and "phase" in ai_message.lower()):
            return "感谢您的提问。我将为您提供针对性的建议。请问您具体想了解什么方面的问题？"
        
        return ai_message
    def split_text_by_marker(self, text, marker=">>["):  
            """  
            将文本根据指定的标记切割，并保留标记前的部分。  

            参数:  
                text (str): 要切割的文本。  
                marker (str): 用于切割的标记，默认为 ">>["。  

            返回:  
                list: 包含切割后保留的部分的列表。  
            """  
            # 使用 marker 分割字符串  
            parts = text.split(marker)  
            
            # 保留标记前的部分  
            result = parts[0]  # 第一个部分一定是标记前的内容  
            # print(f'result is {result}')
            return result  
    def user_chat_history(self):
        def split_history_by_marker(chat_history, marker=">>["):
                t = []
                for node in chat_history:
                    t.append({"role":node["role"], "content":self.split_text_by_marker(node['content'])})
                return t
        return split_history_by_marker(self.chat_history)
    # 阶段查询方法  
    def get_current_stage(self) -> Optional[Dict]:  
        if self.current_stage:  
            stage_info = self.stages_config.get(self.current_stage)  
            if stage_info:  
                return {  
                    "stage": stage_info,  
                    "current_task": self.current_task  
                }  
        return None  

    def get_stage_content(self, stage_id: str) -> Optional[Dict]:  
        return self.stages_config.get(stage_id)  

    def get_stage_tasks(self, stage_id: str) -> List[Dict]:  
        stage_config = self.stages_config.get(stage_id)  
        if stage_config:  
            return stage_config["tasks"]  
        return []  

    def get_all_stages(self) -> Dict[str, Dict]:  
        return self.stages_config.copy()  

    def update_stage_content(self, stage_id: str, content: Dict) -> bool:  
        try:  
            required_keys = {"id", "name", "description", "tasks"}  
            if not all(key in content for key in required_keys):  
                logger.error("Missing required keys in content")  
                return False  

            self.stages_config[stage_id] = content  
            return self.save_stages()  
        except Exception as e:  
            logger.error(f"Error updating stage content: {e}")  
            return False  

    def clear_history(self) -> bool:  
        try:  
            self.chat_history = []  
            return self.save_history_to_file()  
        except Exception as e:  
            logger.error(f"Error clearing chat history: {e}")  
            return False