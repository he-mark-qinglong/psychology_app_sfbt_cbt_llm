from enum import Enum  
from typing import Optional, Dict, Callable, List  
from dataclasses import dataclass  
import logging  

logger = logging.getLogger(__name__)  

class SFBTStage(Enum):  
    INITIAL_RELATIONSHIP = "initial_relationship"    # 初始阶段（建立关系）  
    PROBLEM_EXPLORATION = "problem_exploration"      # 问题探索阶段  
    EXCEPTION_EXPLORATION = "exception_exploration"  # 例外探索阶段  
    GOAL_CONSTRUCTION = "goal_construction"         # 目标构建阶段  
    SOLUTION_CONSTRUCTION = "solution_construction"  # 方案构建阶段  
    PROGRESS_EVALUATION = "progress_evaluation"     # 进展评估阶段  
    CONSOLIDATION = "consolidation"                 # 巩固成果阶段  
    TERMINATION = "termination"                     # 结束阶段  

    @classmethod  
    def from_string(cls, stage_str: str) -> Optional['SFBTStage']:  
        try:  
            return next(  
                (stage for stage in cls   
                 if stage.value == stage_str or stage_str in stage.value),  
                None  
            )  
        except Exception as e:  
            logger.error(f"Error converting string to SFBTStage: {e}")  
            return None  

class SFBTStateMachine:  
    def __init__(self, stages_content: Dict[str, str]):  
        self._current_stage: Optional[SFBTStage] = None  
        self._stages_content = stages_content  
        self._stage_order = [  
            SFBTStage.INITIAL_RELATIONSHIP,    # 初始阶段（建立关系）  
            SFBTStage.GOAL_CONSTRUCTION,       # 目标构建阶段  
            SFBTStage.PROBLEM_EXPLORATION,     # 问题探索阶段  
            SFBTStage.EXCEPTION_EXPLORATION,   # 例外探索阶段  
            SFBTStage.SOLUTION_CONSTRUCTION,   # 方案构建阶段  
            SFBTStage.PROGRESS_EVALUATION,     # 进展评估阶段  
            SFBTStage.CONSOLIDATION,          # 巩固成果阶段  
            SFBTStage.TERMINATION             # 结束阶段  
        ]  
        self._setup_initial_stage()  

    def _setup_initial_stage(self):  
        """设置初始阶段"""  
        if self._stages_content:  
            first_stage = next(iter(self._stages_content))  
            self._current_stage = SFBTStage.from_string(first_stage)  

    def validate_transition(self, target_stage: str) -> bool:  
        """验证阶段转换是否合法"""  
        if not self._current_stage:  
            return True  
        
        target_enum = SFBTStage.from_string(target_stage)  
        if not target_enum:  
            return False  

        # 允许转换到任何有效的阶段，但不允许转换到当前阶段  
        # 如果需要在同一阶段继续，应该使用其他方法而不是转换  
        return target_enum != self._current_stage and target_enum in self._stage_order

    def transition_to(self, stage: str) -> bool:  
        """尝试转换到新阶段"""  
        if self.validate_transition(stage):  
            new_stage = SFBTStage.from_string(stage)  
            if new_stage:  
                self._current_stage = new_stage  
                return True  
            
        logger.error(f'+++++++++ validate_transition false {stage}')  
        return False  

    @property  
    def current_stage(self) -> Optional[str]:  
        """获取当前阶段的字符串表示"""  
        return self._current_stage.value if self._current_stage else None