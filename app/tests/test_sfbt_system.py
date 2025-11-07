import sys  
import os  
import pytest  

# 添加项目根目录到 Python 路径  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  

from app.system_sfbt_old import SFBTSystem  
from app import app
class TestSFBTSystem:  
    @pytest.fixture  
    def system(self):  
        """创建一个 SFBTSystem 实例用于测试"""  
        sfbt_system = SFBTSystem(app.config['STAGE_GUIDE_FILE'])  
        sfbt_system.init_openai(app.config['OPENAI_API_KEY'])  
        return sfbt_system

    def test_initialization(self, system):  
        """测试系统初始化"""  
        assert system is not None  
        assert system.current_stage == 'initial_relationship' 
        assert hasattr(system, 'chat_history')  
        assert isinstance(system.chat_history, list)  

    def test_process_message(self, system):  
        """测试消息处理功能"""  
        # 测试基本对话  
        message = "你好"  
        response = system.get_response(message)  
        
        assert isinstance(response, dict)  
        assert 'response' in response  
        assert isinstance(response['response'], str)  
        assert len(response['response']) > 0  

    def test_stage_transition(self, system):  
        """测试阶段转换功能"""  
        # 测试设置阶段  
        stage_id = "initial_relationship"  
        success = system.set_stage(stage_id)  
        
        assert success  
        assert system.current_stage == stage_id  

        # 测试获取当前阶段  
        current_stage = system.get_current_stage()  
        assert current_stage is not None
        assert current_stage['stage']['id'] == stage_id  

    def test_chat_history(self, system):  
        """测试聊天历史记录功能"""  
        # 发送消息并检查历史记录  
        assert system.load_history_from_file()  

if __name__ == '__main__':  
    pytest.main(['-v'])