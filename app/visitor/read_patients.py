import pandas as pd  
import random  

def load_character_traits():  
    # 加载CSV文件  
    df = pd.read_csv('character_traits.csv')  
    return df  

def generate_random_trait(df, category):  
    """  
    从指定类别中随机生成一个特征  
    category: 主类别名称（如'家庭状况', '当前困扰'等）  
    """  
    # 获取该类别的所有行  
    category_rows = df[df['类别'] == category]  
    if category_rows.empty:  
        return None  
    
    # 随机选择一行  
    random_row = category_rows.sample(n=1).iloc[0]  
    return {  
        '子类别': random_row['子类别'],  
        '描述': random_row['描述'],  
        '示例': random_row['示例']  
    }  

# 使用示例  
if __name__ == "__main__":  
    # 加载特征表  
    traits_df = load_character_traits()  
    
    # 示例：随机生成一个家庭状况特征  
    family_trait = generate_random_trait(traits_df, '家庭状况')  
    if family_trait:  
        print("随机生成的家庭状况特征：")  
        print(f"子类别: {family_trait['子类别']}")  
        print(f"描述: {family_trait['描述']}")  
        print(f"示例: {family_trait['示例']}")  
    
    # 示例：随机生成一个情绪表现特征  
    emotion_trait = generate_random_trait(traits_df, '情绪表现')  
    if emotion_trait:  
        print("\n随机生成的情绪表现特征：")  
        print(f"子类别: {emotion_trait['子类别']}")  
        print(f"描述: {emotion_trait['描述']}")  
        print(f"示例: {emotion_trait['示例']}")