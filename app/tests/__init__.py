"""  
测试包的初始化文件  
包含测试相关的通用配置和辅助函数  
"""  

import os  
import sys  

# 添加项目根目录到 Python 路径  
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
sys.path.append(PROJECT_ROOT)  

# 定义一些测试用的常量  
TEST_STAGES = {  
  "stages": [  
    {  
      "id": "RELATIONSHIP",  
      "name": "初始阶段（建立关系）",  
      "description": "建立咨询关系并收集初始信息",  
      "tasks": [  
        {  
          "id": "self_introduction",  
          "name": "自我介绍和期望收集表",  
          "description": "收集来访者的基本信息和期望",  
          "prompt_template": "请分享以下信息：\n1. 您希望通过咨询获得什么样的帮助\n2. 您对咨询的期待是什么\n3. 您认为什么样的改变会让您满意",  
          "required_fields": ["expectations", "goals"],  
          "optional_fields": ["background_info"]  
        },  
        {  
          "id": "initial_assessment",  
          "name": "初始评估问卷",  
          "description": "评估来访者的初始状态",  
          "prompt_template": "请评估以下方面：\n1. 目前困扰的主要问题\n2. 问题的影响程度（1-10分）\n3. 已经尝试过的解决方法",  
          "required_fields": ["main_problem", "impact_rating"]  
        }  
      ],  
      "process_steps": [  
        "建立咨询关系",  
        "了解来访者的期望",  
        "确定咨询目标的初步方向"  
      ]  
    },  
    {  
      "id": "problem_exploration",  
      "name": "问题探索阶段",  
      "description": "深入了解问题的具体表现和影响",  
      "tasks": [  
        {  
          "id": "problem_log",  
          "name": "问题描述日志",  
          "description": "详细记录问题的具体表现",  
          "prompt_template": "请记录：\n1. 问题出现的具体情况\n2. 触发因素是什么\n3. 当时的反应和感受",  
          "required_fields": ["situation", "triggers", "reactions"]  
        },  
        {  
          "id": "impact_assessment",  
          "name": "影响评估表",  
          "description": "评估问题对各个生活领域的影响",  
          "prompt_template": "评估问题对以下方面的影响（1-10分）：\n1. 工作/学习\n2. 人际关系\n3. 日常生活",  
          "required_fields": ["impact_areas", "severity_ratings"]  
        }  
      ],  
      "process_steps": [  
        "了解问题的具体表现",  
        "探索问题的影响范围",  
        "识别问题的严重程度"  
      ]  
    },  
    {  
      "id": "EXCEPTION",  
      "name": "例外探索阶段",  
      "description": "发现问题不存在或较轻的时刻",  
      "tasks": [  
        {  
          "id": "exception_record",  
          "name": "例外情况记录表",  
          "description": "记录问题不存在或较轻的时刻",  
          "prompt_template": "请记录：\n1. 什么时候问题没那么严重\n2. 当时的具体情况是什么\n3. 有什么不同的做法",  
          "required_fields": ["exception_situation", "difference_factors"]  
        },  
        {  
          "id": "success_log",  
          "name": "成功经验日志",  
          "description": "记录成功应对问题的经验",  
          "prompt_template": "请记录：\n1. 成功应对的具体做法\n2. 带来了什么样的改变\n3. 可以借鉴的经验",  
          "required_fields": ["successful_strategies", "outcomes"]  
        }  
      ],  
      "process_steps": [  
        "发现问题不存在或较轻的时刻",  
        "分析这些例外情况的特点",  
        "识别有效的应对策略"  
      ]  
    },  
    {  
      "id": "GOAL_SETTING",  
      "name": "目标构建阶段",  
      "description": "设定具体可行的咨询目标",  
      "tasks": [  
        {  
          "id": "miracle_question",  
          "name": "奇迹问题思考表",  
          "description": "探索理想状态和期望改变",  
          "prompt_template": "想象一下：\n1. 如果问题奇迹般解决了，生活会有什么不同\n2. 您会注意到什么变化\n3. 其他人会注意到什么变化",  
          "required_fields": ["ideal_state", "expected_changes"]  
        },  
        {  
          "id": "goal_specification",  
          "name": "目标具体化工作表",  
          "description": "将期望转化为具体目标",  
          "prompt_template": "请明确：\n1. 具体想要达到的目标\n2. 如何衡量目标的达成\n3. 实现目标的时间框架",  
          "required_fields": ["specific_goals", "measurement_criteria", "timeline"]  
        }  
      ],  
      "process_steps": [  
        "设想理想状态",  
        "将愿望转化为具体目标",  
        "设定可测量的成功标准"  
      ]  
    },  
    {  
      "id": "SOLUTION",  
      "name": "方案构建阶段",  
      "description": "设计和实施解决方案",  
      "tasks": [  
        {  
          "id": "solution_experiment",  
          "name": "解决方案实验日志",  
          "description": "记录解决方案的尝试和效果",  
          "prompt_template": "请记录：\n1. 尝试的具体方案\n2. 实施过程中的观察\n3. 方案的效果评估",  
          "required_fields": ["solution_tried", "observations", "effectiveness"]  
        },  
        {  
          "id": "progress_tracking",  
          "name": "进展跟踪表",  
          "description": "跟踪方案实施的进展",  
          "prompt_template": "记录：\n1. 方案执行的情况\n2. 遇到的困难和调整\n3. 取得的进展",  
          "required_fields": ["implementation_status", "adjustments", "progress"]  
        }  
      ],  
      "process_steps": [  
        "基于例外设计解决方案",  
        "尝试和评估不同策略",  
        "调整和优化方案"  
      ]  
    },  
    {  
      "id": "PROGRESS",  
      "name": "进展评估阶段",  
      "description": "评估咨询进展和效果",  
      "tasks": [  
        {  
          "id": "progress_score",  
          "name": "进展评分表",  
          "description": "对目标完成度进行评分",  
          "prompt_template": "请评估：\n1. 各项目标的完成程度（1-10分）\n2. 较上次的变化\n3. 促进进展的因素",  
          "required_fields": ["goal_ratings", "changes", "contributing_factors"]  
        },  
        {  
          "id": "change_log",  
          "name": "变化记录日志",  
          "description": "记录观察到的积极变化",  
          "prompt_template": "记录：\n1. 观察到的具体变化\n2. 变化带来的影响\n3. 维持变化的方法",  
          "required_fields": ["observed_changes", "impacts", "maintenance_strategies"]  
        }  
      ],  
      "process_steps": [  
        "评估目标完成度",  
        "确认积极变化",  
        "强化成功经验"  
      ]  
    },  
    {  
      "id": "consolidation",  
      "name": "巩固成果阶段",  
      "description": "巩固咨询成果并预防复发",  
      "tasks": [  
        {  
          "id": "strategy_summary",  
          "name": "应对策略总结表",  
          "description": "总结有效的应对策略",  
          "prompt_template": "总结：\n1. 最有效的应对方法\n2. 这些方法为什么有效\n3. 如何继续运用这些方法",  
          "required_fields": ["effective_strategies", "success_factors", "application_plans"]  
        },  
        {  
          "id": "relapse_prevention",  
          "name": "预防复发计划",  
          "description": "制定预防问题复发的计划",  
          "prompt_template": "制定计划：\n1. 可能的风险情况\n2. 预防措施\n3. 应对策略",  
          "required_fields": ["risk_situations", "preventive_measures", "coping_strategies"]  
        }  
      ],  
      "process_steps": [  
        "总结有效策略",  
        "预防问题复发",  
        "建立长期支持系统"  
      ]  
    },  
    {  
      "id": "termination",  
      "name": "结束阶段",  
      "description": "总结咨询过程并规划未来",  
      "tasks": [  
        {  
          "id": "consultation_summary",  
          "name": "咨询总结报告",  
          "description": "总结整个咨询过程",  
          "prompt_template": "总结：\n1. 咨询过程的主要收获\n2. 达成的改变\n3. 未来可能的挑战",  
          "required_fields": ["achievements", "changes_made", "future_challenges"]  
        },  
        {  
          "id": "follow_up_plan",  
          "name": "后续计划制定表",  
          "description": "制定后续发展计划",  
          "prompt_template": "规划：\n1. 未来发展目标\n2. 可能需要的支持\n3. 具体行动计划",  
          "required_fields": ["future_goals", "support_needed", "action_plans"]  
        }  
      ],  
      "process_steps": [  
        "回顾整个咨询过程",  
        "确认取得的进展",  
        "规划未来发展方向"  
      ]  
    }  
  ]  
}

# 定义一些辅助函数  
def get_test_message():  
    """返回测试用的消息"""  
    return "这是一条测试消息"  

def get_test_response():  
    """返回测试用的回复"""  
    return {  
        "response": "这是一条测试回复",  
        "stage_changed": False  
    }