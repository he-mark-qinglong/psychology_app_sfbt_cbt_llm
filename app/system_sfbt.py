# system_sfbt.py  
from app.system_base import TherapySystemBase  
from app.state_sfbt import SFBTStateMachine  
from typing import Dict, List
from pathlib import Path  

class SFBTSystem(TherapySystemBase):  
    def _init_state_machine(self):  
        return SFBTStateMachine(self.stages_config)  