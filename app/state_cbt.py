from enum import Enum  
from typing import Optional, Dict, Callable, List  
from dataclasses import dataclass  
import logging  

logger = logging.getLogger(__name__)  

class CBTStage(Enum):  
    CCT_PHASE = "cct_phase"                    # 来访者中心阶段  
    PROBLEM_ASSESSMENT = "problem_assessment"   # 问题评估阶段  
    COGNITIVE_BEHAVIORAL_INTERVENTION = "cognitive_behavioral_intervention"  # 认知行为干预阶段  
    CONSOLIDATION_TERMINATION = "consolidation_termination"  # 成果巩固与结束阶段  

    @classmethod  
    def from_string(cls, stage_str: str) -> Optional['CBTStage']:  
        try:  
            return next(  
                (stage for stage in cls   
                 if stage.value == stage_str or stage_str in stage.value),  
                None  
            )  
        except Exception as e:  
            logger.error(f"Error converting string to CBTStage: {e}")  
            return None  

class CBTStateMachine:  
    def __init__(self, stages_content: Dict[str, str]):  
        self._current_stage: Optional[CBTStage] = None  
        self._stages_content = stages_content  
        self._stage_order = [  
            CBTStage.CCT_PHASE,                    # 来访者中心阶段  
            CBTStage.PROBLEM_ASSESSMENT,           # 问题评估阶段  
            CBTStage.COGNITIVE_BEHAVIORAL_INTERVENTION,  # 认知行为干预阶段  
            CBTStage.CONSOLIDATION_TERMINATION     # 成果巩固与结束阶段  
        ]  
        self._setup_initial_stage()  

    def _setup_initial_stage(self):  
        """设置初始阶段"""  
        if self._stages_content:  
            first_stage = next(iter(self._stages_content))  
            self._current_stage = CBTStage.from_string(first_stage)  

    def validate_transition(self, target_stage: str) -> bool:  
        """验证阶段转换是否合法"""  
        if not self._current_stage:  
            return True  
        
        target_enum = CBTStage.from_string(target_stage)  
        if not target_enum:  
            return False  

        # 验证阶段转换的顺序  
        current_index = self._stage_order.index(self._current_stage)  
        target_index = self._stage_order.index(target_enum)  
        
        # 只允许向前转换到下一个阶段  
        return True #target_index != current_index  

    def transition_to(self, stage: str) -> bool:  
        """尝试转换到新阶段"""  
        if self.validate_transition(stage):  
            new_stage = CBTStage.from_string(stage)  
            if new_stage:  
                self._current_stage = new_stage  
                return True  
            
        logger.error(f'+++++++++ validate_transition false {stage}')  
        return False  

    @property  
    def current_stage(self) -> Optional[str]:  
        """获取当前阶段的字符串表示"""  
        return self._current_stage.value if self._current_stage else None