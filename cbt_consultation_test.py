#!/usr/bin/env python3
"""
CBT Agent实时咨询测试脚本
用于模拟真实用户咨询场景并获取Qwen模型的回复
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def simulate_consultation():
    """模拟真实的CBT咨询对话"""
    print("=== CBT Agent实时咨询测试 ===")
    print("欢迎使用CBT Agent咨询系统！")
    print("您可以输入任何关于心理困扰的问题，我会以CBT治疗师的身份为您提供帮助。")
    print("输入 'quit' 或 'exit' 退出测试。")
    print("-" * 50)
    
    # 获取环境变量
    api_key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPENAI_MODEL')
    base_url = os.environ.get('OPENAI_BASE_URL')
    
    if not all([api_key, model, base_url]):
        print("错误：缺少必要的环境变量配置")
        return
    
    # 咨询场景示例
    examples = [
        "我最近总是失眠，因为总是在担心明天的工作。",
        "我觉得自己很没用，每天都提不起精神。",
        "我总是害怕在公众场合说话，觉得会被别人嘲笑。",
        "我经常对自己要求很高，达不到标准就觉得自己很失败。",
        "我对未来感到很焦虑，不知道会发生什么。"
    ]
    
    print("示例问题：")
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    print("-" * 50)
    
    # 主循环
    while True:
        user_input = input("\n请输入您的问题（或输入示例编号查看示例）: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("感谢使用CBT Agent咨询系统！再见！")
            break
            
        # 处理示例编号
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(examples):
                user_input = examples[idx]
                print(f"您选择了示例: {user_input}")
            else:
                print("无效的示例编号，请重新输入。")
                continue
        
        if not user_input:
            print("请输入有效的问题。")
            continue
            
        print(f"\n用户问题: {user_input}")
        print("CBT Agent正在分析并回复...")
        
        try:
            # 构建API请求
            cmd = [
                'curl', '-X', 'POST',
                '-H', 'Content-Type: application/json',
                '-H', f'Authorization: Bearer {api_key}',
                '-d', json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个专业的CBT（认知行为疗法）治疗师，具备丰富的CBT理论知识和实践经验。请以温暖、专业、有同理心的方式回应用户，帮助他们识别和改变负面思维模式，提供实用的认知重构技巧。"
                        },
                        {
                            "role": "user", 
                            "content": user_input
                        }
                    ],
                    "stream": False
                }),
                f"{base_url}/chat/completions"
            ]
            
            # 发送请求
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                content = response['choices'][0]['message']['content']
                print("\n" + "=" * 60)
                print("CBT Agent回复:")
                print(content)
                print("=" * 60)
                
                # 提供下一步建议
                print("\n💡 建议:")
                print("1. 回想一下这个回复中提到的要点")
                print("2. 思考是否可以应用其中的CBT技术")
                print("3. 可以继续提出更多问题来深入探讨")
                print("-" * 60)
                
            else:
                print(f"❌ 请求失败: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("❌ 请求超时，请稍后重试。")
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")

def run_quick_test():
    """快速测试几个典型问题"""
    print("=== 快速CBT Agent测试 ===")
    
    api_key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPENAI_MODEL')
    base_url = os.environ.get('OPENAI_BASE_URL')
    
    if not all([api_key, model, base_url]):
        print("错误：缺少必要的环境变量配置")
        return
    
    test_questions = [
        "我总是担心自己会犯错误，怎么办？",
        "我对未来感到很焦虑，不知道该怎么办。",
        "我觉得自己什么都不行，怎么改变这种想法？"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- 测试问题 {i} ---")
        print(f"问题: {question}")
        
        try:
            cmd = [
                'curl', '-X', 'POST',
                '-H', 'Content-Type: application/json',
                '-H', f'Authorization: Bearer {api_key}',
                '-d', json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是专业的CBT治疗师，请以温暖、专业的方式提供CBT指导。"
                        },
                        {
                            "role": "user", 
                            "content": question
                        }
                    ],
                    "stream": False
                }),
                f"{base_url}/chat/completions"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                content = response['choices'][0]['message']['content']
                print("CBT回复:")
                print(content[:300] + "..." if len(content) > 300 else content)
            else:
                print(f"请求失败: {result.stderr}")
                
        except Exception as e:
            print(f"测试出错: {str(e)}")
    
    print("\n" + "=" * 50)
    print("快速测试完成！")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        run_quick_test()
    else:
        simulate_consultation()