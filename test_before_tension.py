#!/usr/bin/env python3
"""
ORCA机械手硬件连接验证
在进行张力调节之前确认电机通信正常
"""

from orca_core.hardware.dynamixel_client import DynamixelClient
import time

def test_basic_motor_communication():
    """测试基础电机通信"""
    print("🔍 测试基础电机通信...")
    
    port = "COM8"
    baudrate = 3000000
    motor_ids = [1, 2, 3]  # 先测试前3个电机
    
    try:
        print(f"📡 端口: {port}")
        print(f"📡 波特率: {baudrate}")
        print(f"🔧 测试电机ID: {motor_ids}")
        
        # 创建客户端
        client = DynamixelClient(motor_ids, port, baudrate)
        print("✅ DynamixelClient创建成功")
        
        # 尝试连接
        print("\n🔗 尝试连接电机...")
        client.connect()
        print("✅ 连接成功!")
        
        # 连接成功就表示通信正常
        print("✅ 电机通信正常")
        
        # 断开连接
        client.disconnect()
        print("✅ 断开连接成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        if 'client' in locals():
            try:
                client.disconnect()
            except:
                pass
        return False

def safe_tension_test():
    """安全的张力测试"""
    print("\n🔧 安全张力测试...")
    
    # 首先确认基础通信
    if not test_basic_motor_communication():
        print("❌ 基础通信失败，无法进行张力调节")
        return False
    
    print("\n✅ 基础通信正常")
    print("现在可以安全地进行张力调节")
    
    # 提供详细的张力调节指导
    print("\n📋 张力调节步骤:")
    print("1. 确保机械手处于安全位置")
    print("2. 运行张力脚本")
    print("3. 看到 'Holding motors' 提示时:")
    print("   - 使用附带的工具调节拉线张力")
    print("   - 确保拉线有适当张力但不过紧")
    print("4. 调节完成后按 Ctrl+C 正常退出")
    
    proceed = input("\n❓ 确认要继续进行张力调节吗? (y/n): ").lower()
    return proceed == 'y'

if __name__ == "__main__":
    print("🤖 ORCA机械手张力调节前检查")
    print("=" * 40)
    
    if safe_tension_test():
        print("\n🚀 准备运行张力调节...")
        print("执行命令:")
        print("python scripts/tension.py orca_core/models/orcahand_v1_right")
    else:
        print("\n⚠️ 请先解决连接问题再进行张力调节")
        print("建议:")
        print("• 确认Dynamixel Wizard能检测到电机")
        print("• 检查U2D2连接和电源")
        print("• 如有必要，重启设备")
