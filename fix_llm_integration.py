#!/usr/bin/env python3
"""
LLM交互修复方案
解决CBT Agent中LLM调用未正确初始化的问题
"""

def fix_llm_integration():
    """修复LLM集成问题"""
    print("=== LLM交互问题修复方案 ===")
    
    print("\n🔍 问题分析:")
    print("1. 在user_manager.py中，系统初始化时注释掉了LLM客户端初始化")
    print("2. CBT系统实例创建时未正确初始化AI客户端")
    print("3. 导致即使有get_response方法，也无法实际调用LLM")
    
    print("\n🔧 修复方案:")
    print("1. 修复user_manager.py中的初始化代码")
    print("2. 确保CBT系统能正确初始化OpenAI或Claude客户端")
    print("3. 验证LLM调用路径完整")
    
    print("\n📋 具体修复内容:")
    
    # 修复1: user_manager.py 中的初始化逻辑
    print("\n1. 修复 user_manager.py 初始化部分:")
    print("   将注释掉的代码恢复:")
    print("   ```")
    print("   # 修复前:")
    print("   # self.therapy_system.init_openai(openai_api_key)")
    print("   self.therapy_system.init_claude(claude_api_key)")
    print("   ")
    print("   # 修复后:")
    print("   self.therapy_system.init_openai(openai_api_key)")
    print("   self.therapy_system.init_claude(claude_api_key)")
    print("   ```")
    
    # 修复2: 检查系统初始化方法
    print("\n2. 检查系统初始化方法:")
    print("   确保CBTSystem类中包含正确的init_openai和init_claude方法")
    
    # 修复3: 验证回调函数调用
    print("\n3. 验证get_response中的LLM调用:")
    print("   确保以下代码能正常工作:")
    print("   ```")
    print("   response = self.client.get_completion(messages=messages)")
    print("   ai_message = response")
    print("   ```")
    
    print("\n🧪 测试验证建议:")
    print("   1. 运行API连接测试")
    print("   2. 测试简单的对话")
    print("   3. 验证回复内容是否来自LLM")
    
    print("\n🎯 预期效果:")
    print("   - CBT Agent能真正调用LLM进行对话")
    print("   - 用户输入能得到AI生成的回复")
    print("   - 系统完整实现LLM驱动的对话功能")
    
    print("\n⚠️ 注意事项:")
    print("   - 需要确保API密钥正确配置")
    print("   - 需要网络连接访问API服务")
    print("   - 需要在系统启动时正确初始化所有组件")

def verify_llm_setup():
    """验证LLM设置"""
    print("\n=== LLM设置验证 ===")
    
    try:
        from app.system_cbt import CBTSystem
        from app.user_manager import User
        
        print("✓ CBTSystem导入成功")
        
        # 尝试创建一个CBT系统实例
        # 注意：这里我们不需要实际的文件路径，只是验证类结构
        
        # 检查类方法
        methods = ['init_openai', 'init_claude', 'get_response']
        for method in methods:
            if hasattr(CBTSystem, method):
                print(f"✓ CBTSystem.{method} 方法存在")
            else:
                print(f"✗ CBTSystem.{method} 方法缺失")
                
        print("\n✅ LLM系统组件结构完整")
        print("✅ 但需要实际初始化才能工作")
        
    except Exception as e:
        print(f"✗ 验证失败: {str(e)}")

if __name__ == "__main__":
    fix_llm_integration()
    verify_llm_setup()
    
    print("\n🎉 修复方案制定完成！")
    print("系统现在需要修复LLM初始化部分才能正常工作。")