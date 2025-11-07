# user_manager.py  
from typing import Dict, Optional  
from threading import Lock  
import logging  
from app.system_base.therapy_system import TherapySystemBase
from app.system_sfbt import SFBTSystem  
from app.system_cbt import CBTSystem

logger = logging.getLogger(__name__)  

class User:  
    def __init__(self, username: str, 
                 stage_guide_file: str,
                 prompt_file:str,
                 openai_api_key: str,
                 claude_api_key:str,
                 type:str):  
        self.username = username  
        self.therapy_system = None
        self.last_active = None  

        # 为每个用户创建独立的 therapy_system 实例 
        if type == 'cbt':
            self.therapy_system = CBTSystem(stage_guide_file, 
                                            prompt_file,
                                            user=username)
            self.therapy_system.init_openai(openai_api_key)
            self.therapy_system.init_claude(claude_api_key)
        else:
            self.therapy_system = SFBTSystem(stage_guide_file,
                                             prompt_file,
                                             user=username)
            self.therapy_system.init_openai(openai_api_key)
            self.therapy_system.init_claude(claude_api_key)  


    def __str__(self):  
        return f"User(username={self.username})"  

class UserManager:  
    _instance = None  
    _lock = Lock()  

    def __new__(cls):  
        with cls._lock:  
            if cls._instance is None:  
                cls._instance = super(UserManager, cls).__new__(cls)  
                cls._instance._initialized = False  
            return cls._instance  

    def __init__(self):  
        if self._initialized:  
            return  
            
        self._users: Dict[str, User] = {}  
        self._lock = Lock()   
        self._openai_api_key = None  
        self._claude_api_key = None
        self._initialized = True  
        logger.info("UserManager initialized")  

    def init_config(self, appConfig, THERAPT_CONFIGS):  
        """初始化配置"""  
        self.THERAPT_CONFIGS = THERAPT_CONFIGS
        print(f'THERAPT_CONFIGS========{THERAPT_CONFIGS}')
        self._openai_api_key = appConfig['OPENAI_API_KEY']  
        self._claude_api_key = appConfig['CLAUDE_API_KEY'] 
    
    def add_user(self, username: str, type:str ='cbt') -> User:  
        """添加新用户或获取现有用户"""  
        with self._lock:  
            if username not in self._users:  
                if type not in self.THERAPT_CONFIGS.keys():
                    return None  # 内部不做错误处理，来不及搞。
                stage_guide_file = self.THERAPT_CONFIGS[type]['stages']
                prompt_file = self.THERAPT_CONFIGS[type]['prompts']
                if not stage_guide_file or (not self._openai_api_key and not self._claude_api_key):  
                    raise ValueError("UserManager not properly initialized")  
                self._users[username] = User(  
                    username,  
                    stage_guide_file,  
                    prompt_file,
                    self._openai_api_key,
                    self._claude_api_key,
                    type,
                )  
                logger.info(f"New user created: {username}")  
            return self._users[username]  
    def remove_user(self, username: str) -> bool:  
        """  
        删除用户及其 therapy_system  
        """  
        if self.user_exists(username):  
            # 清理用户相关资源  
            user = self._users[username]  
            if hasattr(user, 'therapy_system'):  
                # 如果有需要，在这里添加 therapy_system 的清理代码  
                user.therapy_system = None  
            
            # 从用户字典中删除  
            del self._users[username]  
            logger.info(f"User {username} removed successfully")  
            return True  
        return False  
    
    def get_user(self, username: str) -> Optional[User]:  
        """获取用户，如果不存在返回None"""  
        return self._users.get(username)  

    def get_user_system(self, username: str) -> Optional[TherapySystemBase]:  
        """获取用户的 SFBT 系统实例"""  
        user = self.get_user(username)  
        return user.therapy_system if user else None  

    def user_exists(self, username: str) -> bool:  
        """检查用户是否存在"""  
        return username in self._users