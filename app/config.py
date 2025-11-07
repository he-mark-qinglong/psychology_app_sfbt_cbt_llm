import json, os
from pathlib import Path
from typing import Dict, Any

class Config:    
    #OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    #CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
    # 基础路径  
    BASE_DIR = Path(__file__).parent  
    
    # 文件路径配置  
    PROMPTS_DIR = BASE_DIR / 'prompts'  
    CHAT_HISTORY_FILE = BASE_DIR / 'data' / 'chat_history.json'  
    
    NORMAL_PSYCHOLOGY_METHOD = 'cbt'  # 或 'sfbt'

    
def therapy_config(app):
    return {
        "sfbt": {
            "stages": app.config['PROMPTS_DIR']/"sfbt/stages_sfbt_english.json",
            "prompts": app.config['PROMPTS_DIR']/"sfbt/progress_prompt_sfbt_english.md"
        },
        "cbt": {
            "stages": app.config['PROMPTS_DIR'] / "cbt/stages_cbt_english.json",
            "prompts": app.config['PROMPTS_DIR'] / "cbt/progress_prompt_CBT_with_CCT_english.md"
        }
    }




