from anthropic import Anthropic  

class ClaudeClient:  
    def __init__(self, api_key):  
        self.client = Anthropic(api_key=api_key)  
    
    def get_completion(self, messages, temp=0.5):  
        try:  
            # 将消息历史转换为Claude格式  
            formatted_messages = self._format_messages(messages)  
            
            response = self.client.messages.create(  
                model="claude-3-5-sonnet-20241022",  # 或者其他Claude模型版本  
                max_tokens=1024,  
                temperature=temp,  
                messages=formatted_messages  
            )  
            
            return response.content[0].text  
            
        except Exception as e:  
            print(f"Claude API调用错误: {str(e)}")  
            raise  

    def _format_messages(self, messages):  
        # 将OpenAI格式的消息转换为Claude格式  
        formatted = []  
        for msg in messages:  
            role = msg["role"]  
            content = msg["content"]  
            
            if role == "user":  
                formatted.append({  
                    "role": "user",  
                    "content": content  
                })  
            elif role == "assistant":  
                formatted.append({  
                    "role": "assistant",  
                    "content": content  
                })  
            elif role == "system":  
                # Claude的system prompt需要放在第一条user message中  
                if formatted and formatted[0]["role"] == "user":  
                    formatted[0]["content"] = content + "\n\n" + formatted[0]["content"]  
                else:  
                    formatted.insert(0, {  
                        "role": "user",  
                        "content": content  
                    })  
                    
        return formatted
    
def test_api_connection(api_key):  
    try:  
        client = Anthropic(api_key=api_key)  
        response = client.messages.create(  
            model="claude-3-sonnet-20240229",  
            max_tokens=100,  
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
    test_api_connection("a key to replace this line")