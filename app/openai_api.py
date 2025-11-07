from openai import OpenAI  

class OpenAIClient:  
    def __init__(self, api_key):  
        self.client = OpenAI(api_key=api_key)  
    
    def get_completion(self, messages, temp=0.7):  
        messages[0] = {'content':messages[0]['content'], 'role':'developer'}
        try:  
            # OpenAI的消息格式不需要转换，直接使用  
            response = self.client.chat.completions.create(  
                model="gpt-4o-2024-11-20",  # 或者其他GPT模型版本  
                # temperature=temp,  
                messages=messages  
            )  
            
            return response.choices[0].message.content  
            
        except Exception as e:  
            print(f"OpenAI API调用错误: {str(e)}")  
            raise  

    def _format_messages(self, messages):  
        # OpenAI已经使用正确的格式，不需要转换  
        return messages  

def test_api_connection(api_key):  
        try:  
            client = OpenAI(api_key=api_key)  
            response = client.chat.completions.create(  
                model="gpt-4-turbo-preview",  
                messages=[{  
                    "role": "user",  
                    "content": "Hello, testing connection"  
                }]  
            )  
            print("API连接成功")  
            return True  
        except Exception as e:  
            print(f"API连接测试失败: {str(e)}")  
            return False  

if __name__ == "__main__":  
        test_api_connection("your-api-key-here")