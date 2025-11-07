from datetime import datetime  
import json  
from typing import Dict, List, Optional  

class TaskTemplate:  
    def __init__(self, id: str, name: str, description: str, prompt_template: str,  
                 required_fields: List[str], stage: str, conditions: Dict = None,  
                 optional_fields: List[str] = None):  
        self.id = id  
        self.name = name  
        self.description = description  
        self.prompt_template = prompt_template  
        self.required_fields = required_fields  
        self.optional_fields = optional_fields or []  
        self.stage = stage  
        self.conditions = conditions or {}  
        
    def to_dict(self):  
        return {  
            'id': self.id,  
            'name': self.name,  
            'description': self.description,  
            'prompt_template': self.prompt_template,  
            'required_fields': self.required_fields,  
            'optional_fields': self.optional_fields,  
            'stage': self.stage,  
            'conditions': self.conditions  
        }  

class TaskInstance:  
    def __init__(self, id: str, template_id: str, content: str, client_id: str,  
                 assigned_date: datetime = None, due_date: datetime = None,  
                 status: str = "assigned", completion: float = 0.0,  
                 feedback: Dict = None):  
        self.id = id  
        self.template_id = template_id  
        self.content = content  
        self.client_id = client_id  
        self.assigned_date = assigned_date or datetime.now()  
        self.due_date = due_date  
        self.status = status  
        self.completion = completion  
        self.feedback = feedback or {}  
        
    def to_dict(self):  
        return {  
            'id': self.id,  
            'template_id': self.template_id,  
            'content': self.content,  
            'client_id': self.client_id,  
            'assigned_date': self.assigned_date.isoformat(),  
            'due_date': self.due_date.isoformat() if self.due_date else None,  
            'status': self.status,  
            'completion': self.completion,  
            'feedback': self.feedback  
        }  

class TaskManager:  
    def __init__(self, config_path: str):  
        self.templates = {}  
        self.tasks = {}  
        self.load_templates(config_path)  
    
    def load_templates(self, config_path: str):  
        """从配置文件加载任务模板"""  
        try:  
            with open(config_path, 'r', encoding='utf-8') as f:  
                config = json.load(f)  
                for template_data in config['task_templates']:  
                    template = TaskTemplate(  
                        id=template_data['id'],  
                        name=template_data['name'],  
                        description=template_data['description'],  
                        prompt_template=template_data['prompt_template'],  
                        required_fields=template_data['required_fields'],  
                        optional_fields=template_data.get('optional_fields', []),  
                        stage=template_data['stage'],  
                        conditions=template_data.get('conditions', {})  
                    )  
                    self.templates[template.id] = template  
        except Exception as e:  
            raise Exception(f"Failed to load task templates: {str(e)}")  

    def get_available_templates(self, stage: str, context: Dict) -> List[TaskTemplate]:  
        """获取当前阶段可用的任务模板"""  
        available = []  
        for template in self.templates.values():  
            if template.stage != stage:  
                continue  
                
            conditions_met = True  
            for field, condition in template.conditions.items():  
                if field not in context or str(context[field]) != condition:  
                    conditions_met = False  
                    break  
                    
            if conditions_met:  
                available.append(template)  
                
        return available  

    def create_task(self, template_id: str, client_id: str, context: Dict) -> TaskInstance:  
        """创建具体任务"""  
        template = self.templates.get(template_id)  
        if not template:  
            raise ValueError(f"Template {template_id} not found")  

        missing_fields = [  
            field for field in template.required_fields   
            if field not in context  
        ]  
        if missing_fields:  
            raise ValueError(f"Missing required fields: {missing_fields}")  

        task_content = template.prompt_template.format(**context)  

        task = TaskInstance(  
            id=f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",  
            template_id=template_id,  
            content=task_content,  
            client_id=client_id  
        )  

        self.tasks[task.id] = task  
        return task  

    def update_task_status(self, task_id: str, status: str, feedback: Dict) -> None:  
        """更新任务状态和反馈"""  
        task = self.tasks.get(task_id)  
        if not task:  
            raise ValueError(f"Task {task_id} not found")  

        task.status = status  
        task.feedback = feedback  
        if status == "completed":  
            task.completion = 1.0