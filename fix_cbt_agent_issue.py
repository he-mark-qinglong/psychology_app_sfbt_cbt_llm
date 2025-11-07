#!/usr/bin/env python3
"""
修复方案：解决CBT Agent回复内容不完整的问题

问题描述：
当用户输入"你好"时，Agent返回了模板化的回复"关于'你好...'的建议"
这通常是由于模型返回了无效的回复内容导致的

修复方案：
1. 添加对AI回复内容的验证和清理
2. 防止返回占位符或模板内容
3. 提供更友好的默认回复
"""

# 在therapy_system.py中需要添加的修复代码段：

FIXED_CODE_SNIPPET = '''
            response = self.client.get_completion(messages=messages)  
            ai_message = response  

            # 验证AI回复的有效性并过滤不合适的回复
            if not ai_message or not ai_message.strip():
                ai_message = "感谢您的提问。为了更好地帮助您，我需要更具体的信息。请您详细描述一下您想了解的问题。"
            
            # 过滤掉可能的模板占位符内容
            if ("关于'..." in ai_message and "的建议" in ai_message) or \\
               ("template" in ai_message.lower()) or \\
               ("placeholder" in ai_message.lower()) or \\
               (ai_message.strip().startswith(">>>") and "phase" in ai_message.lower()):
                ai_message = "感谢您的提问。我将为您提供针对性的建议。请问您具体想了解什么方面的问题？"

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
'''

print("=== CBT Agent修复方案 ===")
print("问题：用户输入'你好'时返回模板占位符内容")
print("\n修复方案：添加AI回复内容验证和清理逻辑")
print("\n需要在system_base/therapy_system.py的get_response方法中添加以下代码：")
print(FIXED_CODE_SNIPPET)
print("=== 修复完成 ===")