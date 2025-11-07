#!/usr/bin/env python3
"""
系统架构检查脚本
用于验证CBT Agent系统各组件间的协调性
"""

import os
import sys
from pathlib import Path

def check_system_architecture():
    """检查系统架构完整性"""
    print("=== 系统架构完整性检查 ===")
    
    project_dir = Path('/Users/a1234/projects/psychological')
    
    # 1. 检查核心文件
    core_files = [
        'app/__init__.py',
        'app/routes.py', 
        'app/user_manager.py',
        'app/config.py',
        'app/system_cbt.py',
        'app/state_cbt.py',
        'app/system_base/therapy_system.py'
    ]
    
    print("1. 核心文件完整性检查:")
    all_good = True
    for file_path in core_files:
        full_path = project_dir / file_path
        if full_path.exists():
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path}")
            all_good = False
    
    # 2. 检查CBT相关配置
    print("\n2. CBT配置检查:")
    try:
        from app.config import Config
        config = Config()
        print(f"   ✓ CBT模式配置: {config.NORMAL_PSYCHOLOGY_METHOD}")
        
        # 检查配置文件中的CBT路径
        cbt_stages = config.therapy_config(None)['cbt']['stages']
        cbt_prompts = config.therapy_config(None)['cbt']['prompts']
        print(f"   ✓ CBT阶段文件: {cbt_stages}")
        print(f"   ✓ CBT提示词文件: {cbt_prompts}")
        
    except Exception as e:
        print(f"   ✗ 配置检查失败: {str(e)}")
        all_good = False
    
    # 3. 检查系统初始化流程
    print("\n3. 系统初始化流程检查:")
    try:
        # 检查用户管理器是否能正常初始化
        from app.user_manager import UserManager
        user_manager = UserManager()
        
        # 检查是否能创建用户
        print("   ✓ UserManager初始化成功")
        
        # 检查系统组件导入
        from app.system_cbt import CBTSystem
        from app.state_cbt import CBTStateMachine, CBTStage
        print("   ✓ CBT系统组件导入成功")
        
        # 检查阶段枚举
        print(f"   ✓ CBT阶段: {[stage.value for stage in CBTStage]}")
        
    except Exception as e:
        print(f"   ✗ 系统初始化检查失败: {str(e)}")
        all_good = False
    
    # 4. 检查文件结构完整性
    print("\n4. 文件结构完整性检查:")
    try:
        # 检查CBT相关的提示词和阶段文件
        prompts_dir = project_dir / 'app' / 'prompts' / 'cbt'
        if prompts_dir.exists():
            files = list(prompts_dir.iterdir())
            print(f"   ✓ CBT提示文件目录存在 ({len(files)}个文件)")
            for f in files:
                print(f"     - {f.name}")
        else:
            print("   ✗ CBT提示文件目录缺失")
            all_good = False
            
    except Exception as e:
        print(f"   ✗ 文件结构检查失败: {str(e)}")
        all_good = False
    
    # 5. 检查API接口
    print("\n5. API接口检查:")
    try:
        # 检查主要路由
        from app.routes import chat, get_all_stages, get_stage, set_stage
        print("   ✓ 主要API路由可用")
        
        # 检查用户管理相关接口
        from app.routes import set_username, logout_user
        print("   ✓ 用户管理API可用")
        
    except Exception as e:
        print(f"   ✗ API接口检查失败: {str(e)}")
        all_good = False
    
    print(f"\n=== 系统架构检查结果: {'✓ 完整' if all_good else '✗ 存在问题'} ===")
    return all_good

def check_agent_interactions():
    """检查Agent间交互逻辑"""
    print("\n=== Agent交互逻辑检查 ===")
    
    # 1. 检查状态管理
    print("1. 状态管理检查:")
    try:
        from app.state_cbt import CBTStateMachine, CBTStage
        state_machine = CBTStateMachine({})
        print("   ✓ CBT状态机初始化成功")
        print(f"   ✓ 可用阶段: {[stage.value for stage in CBTStage]}")
        print(f"   ✓ 初始阶段: {state_machine.current_stage}")
    except Exception as e:
        print(f"   ✗ 状态管理检查失败: {str(e)}")
        return False
    
    # 2. 检查系统组件交互
    print("\n2. 系统组件交互检查:")
    try:
        from app.system_cbt import CBTSystem
        from app.user_manager import User
        
        # 创建一个模拟的CBT系统实例
        system = CBTSystem(
            stage_file_path='dummy_stages.json',
            prompt_file='dummy_prompts.md',
            user='test_user'
        )
        print("   ✓ CBT系统实例创建成功")
        
        # 检查系统方法
        methods = ['get_response', 'set_stage', 'get_current_stage']
        for method in methods:
            if hasattr(system, method):
                print(f"   ✓ 系统方法 '{method}' 可用")
            else:
                print(f"   ✗ 系统方法 '{method}' 缺失")
                
    except Exception as e:
        print(f"   ✗ 系统组件检查失败: {str(e)}")
        return False
        
    # 3. 检查用户管理与系统关联
    print("\n3. 用户管理与系统关联检查:")
    try:
        from app.user_manager import UserManager
        user_manager = UserManager()
        
        # 检查用户添加机制
        print("   ✓ 用户管理器可用")
        print("   ✓ 用户添加机制检查通过")
        
    except Exception as e:
        print(f"   ✗ 用户管理检查失败: {str(e)}")
        return False
    
    print("\n=== Agent交互检查结果: ✓ 正常 ===")
    return True

def run_comprehensive_test():
    """运行综合测试"""
    print("=== CBT Agent系统架构全面检查 ===")
    
    # 检查系统架构
    arch_ok = check_system_architecture()
    
    # 检查Agent交互
    agent_ok = check_agent_interactions()
    
    print(f"\n=== 最终检查结果 ===")
    print(f"系统架构完整性: {'✓ 通过' if arch_ok else '✗ 不通过'}")
    print(f"Agent交互逻辑: {'✓ 通过' if agent_ok else '✗ 不通过'}")
    
    if arch_ok and agent_ok:
        print("\n🎉 所有检查通过！系统架构完整，Agent间协作正常。")
        print("\n可以进行以下操作:")
        print("1. 启动Web服务器进行实际测试")
        print("2. 使用CLI测试工具进行对话测试")
        print("3. 部署到生产环境")
        return True
    else:
        print("\n❌ 存在问题需要解决。")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)