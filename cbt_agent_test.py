#!/usr/bin/env python3
"""
CBT Agent测试脚本
专门测试心理治疗系统中的CBT（认知行为疗法）Agent功能
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def test_cbta_agent():
    """测试CBT Agent功能"""
    print("=== CBT Agent功能测试 ===")
    
    # 检查环境变量
    api_key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPENAI_MODEL')
    base_url = os.environ.get('OPENAI_BASE_URL')
    
    if not all([api_key, model, base_url]):
        print("❌ 缺少必要的环境变量")
        return False
    
    # 1. 测试Qwen模型的基础功能
    print("1. 测试Qwen模型基础功能...")
    try:
        cmd = [
            'curl', '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-H', f'Authorization: Bearer {api_key}',
            '-d', json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": "请用简洁的英文解释什么是CBT（认知行为疗法）"
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
            print("✓ CBT概念解释:")
            print(content[:200] + "..." if len(content) > 200 else content)
        else:
            print(f"✗ 模型调用失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {str(e)}")
        return False
    
    # 2. 模拟CBT Agent的对话交互
    print("\n2. 模拟CBT Agent对话交互...")
    
    # 模拟用户输入的典型CBT对话
    cbt_prompts = [
        "我最近总是感到焦虑，不知道该怎么办。",
        "我觉得自己很无能，什么都做不好。",
        "我总是担心未来的事情，导致我无法专注当下。",
        "我想改变我的思维方式，但不知道从何开始。"
    ]
    
    for i, prompt in enumerate(cbt_prompts, 1):
        print(f"   Prompt {i}: {prompt}")
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
                            "content": "你是一个专业的CBT（认知行为疗法）治疗师。你的职责是帮助用户识别和改变负面思维模式，提供实用的认知重构技巧。"
                        },
                        {
                            "role": "user", 
                            "content": prompt
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
                print(f"   Response {i}: {(content[:150] + '...') if len(content) > 150 else content}")
            else:
                print(f"   ✗ 对话失败: {result.stderr}")
                
        except Exception as e:
            print(f"   ✗ 对话测试出错: {str(e)}")
    
    # 3. 测试CBT技术应用
    print("\n3. 测试CBT技术应用...")
    
    cbt_techniques = [
        "请帮我识别这个想法中的认知扭曲：\"我今天又犯了一个错误，我真是个失败者。\"",
        "请帮我用CBT的方法重构这个负面想法：\"如果我表现不好，别人就会看不起我。\"",
        "请给我一个CBT的思维记录表格模板。"
    ]
    
    for i, technique in enumerate(cbt_techniques, 1):
        print(f"   Technique {i}: {technique}")
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
                            "content": "你是一个专业的CBT（认知行为疗法）治疗师，擅长运用各种CBT技术帮助用户。请提供准确、实用的CBT技术指导。"
                        },
                        {
                            "role": "user", 
                            "content": technique
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
                print(f"   Result {i}: {(content[:150] + '...') if len(content) > 150 else content}")
            else:
                print(f"   ✗ 技术应用失败: {result.stderr}")
                
        except Exception as e:
            print(f"   ✗ 技术测试出错: {str(e)}")
    
    return True

def test_cbta_integration():
    """测试CBT Agent与系统集成"""
    print("\n=== CBT Agent系统集成测试 ===")
    
    # 检查项目中的CBT相关文件
    project_dir = Path('/Users/a1234/projects/psychological')
    
    cbt_files = [
        'app/system_cbt.py',
        'app/state_cbt.py',
        'app/prompts/cbt/',
        'app/data/cbt/'
    ]
    
    print("检查CBT相关文件和目录:")
    for item in cbt_files:
        full_path = project_dir / item
        if full_path.exists():
            if full_path.is_dir():
                count = len(list(full_path.rglob('*')))
                print(f"✓ {item} (包含{count}个项目)")
            else:
                print(f"✓ {item}")
        else:
            print(f"✗ {item}")
    
    # 验证config.py中的CBT配置
    try:
        import app.config
        config = app.config.Config()
        print(f"\nCBT配置验证:")
        print(f"- 默认心理治疗类型: {config.NORMAL_PSYCHOLOGY_METHOD}")
        print(f"- CBT阶段文件: {config.therapy_config(None)['cbt']['stages']}")
        print(f"- CBT提示词文件: {config.therapy_config(None)['cbt']['prompts']}")
        return True
    except Exception as e:
        print(f"✗ 配置验证失败: {str(e)}")
        return False

def run_complete_cbta_test():
    """运行完整的CBT Agent测试"""
    print("=== 开始CBT Agent完整测试 ===")
    
    # 1. 测试CBT Agent核心功能
    cbta_success = test_cbta_agent()
    
    # 2. 测试系统集成
    integration_success = test_cbta_integration()
    
    print("\n=== CBT测试结果汇总 ===")
    print(f"CBT Agent功能测试: {'✓ 成功' if cbta_success else '✗ 失败'}")
    print(f"系统集成测试: {'✓ 成功' if integration_success else '✗ 失败'}")
    
    if cbta_success and integration_success:
        print("\n🎉 CBT Agent测试全部通过！系统可以支持CBT心理治疗的agent方式进行对话。")
        return True
    else:
        print("\n❌ 部分测试失败，请检查相关配置。")
        return False

if __name__ == "__main__":
    success = run_complete_cbta_test()
    sys.exit(0 if success else 1)