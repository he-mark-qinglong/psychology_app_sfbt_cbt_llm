# system_cbt.py  
from app.system_base import TherapySystemBase  
from app.state_cbt import CBTStateMachine  

from typing import Dict, List

class CBTSystem(TherapySystemBase):  
    def _init_state_machine(self):  
        return CBTStateMachine(self.stages_config) 