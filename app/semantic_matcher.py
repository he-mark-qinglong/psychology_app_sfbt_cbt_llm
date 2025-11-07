import requests  

class SemanticMatcherClient:  
    def __init__(self, base_url='http://localhost:5002'):  
        self.base_url = base_url.rstrip('/')  
    
    #参数说明，目前用模型发现“方案构建”和“方案构建完成”的相似度是0.8764000535011292
    #而另一个目前忘记的情况是0.85但是不应该归为一类的意思的请，所以调整这里为0.87
    def get_similarity(self, text1, text2, threshold=0.87):  
        """  
        获取两个文本的相似度  
        
        Args:  
            text1 (str): 第一个文本  
            text2 (str): 第二个文本  
            threshold (float): 相似度阈值  
            
        Returns:  
            tuple: (is_similar, similarity)  
        """  
        response = requests.post(f'{self.base_url}/similarity', json={  
            'text1': text1,  
            'text2': text2,  
            'threshold': threshold  
        })  
        
        if response.status_code == 200:  
            result = response.json()  
            return result['is_similar'], result['similarity']  
        else:  
            raise Exception(f"Error: {response.status_code}, {response.text}")  
    
    def find_similar_phrases(self, target_phrase, phrase_list, threshold=0.87):  
        """  
        查找与目标短语相似的短语列表  
        
        Args:  
            target_phrase (str): 目标短语  
            phrase_list (list): 待比较的短语列表  
            threshold (float): 相似度阈值  
            
        Returns:  
            list: [(phrase, similarity), ...]  
        """  
        response = requests.post(f'{self.base_url}/find_similar', json={  
            'target_phrase': target_phrase,  
            'phrase_list': phrase_list,  
            'threshold': threshold  
        })  
        
        if response.status_code == 200:  
            result = response.json()  
            return [(item['phrase'], item['similarity']) for item in result['results']]  
        else:  
            raise Exception(f"Error: {response.status_code}, {response.text}")  

# 使用示例  
def main():  
    client = SemanticMatcherClient()  
    
    # 测试相似度计算  
    text1 = "目标设定"  
    text2 = "设定目标"  
    try:  
        is_similar, similarity = client.get_similarity(text1, text2)  
        print(f"Similarity between '{text1}' and '{text2}':")  
        print(f"Is similar: {is_similar}")  
        print(f"Similarity score: {similarity}")  
    except Exception as e:  
        print(f"Error getting similarity: {e}")  
    
    # 测试相似短语查找  
    target = "目标设定"  
    phrases = ["设定目标", "确定目标", "目标确定", "制定计划", "设置目标"]  
    try:  
        results = client.find_similar_phrases(target, phrases)  
        print(f"\nSimilar phrases to '{target}':")  
        for phrase, score in results:  
            print(f"- {phrase}: {score}")  
    except Exception as e:  
        print(f"Error finding similar phrases: {e}")  

if __name__ == '__main__':  
    main()