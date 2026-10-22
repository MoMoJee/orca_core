#!/usr/bin/env python3
"""
确认ORCA机械手连接状态
"""

from orca_core import OrcaHand
import time

def test_connection_status():
    print("🔍 确认ORCA机械手连接状态...")
    print("=" * 40)
    
    try:
        hand = OrcaHand('orca_core/models/orcahand_v1_right')
        print("✅ OrcaHand对象创建成功")
        
        print(f"📡 配置的端口: {hand.port}")
        print(f"📡 配置的波特率: {hand.baudrate}")
        print(f"🔧 电机IDs: {hand.motor_ids}")
        
        print("\n🔗 尝试连接...")
        status = hand.connect()
        print(f"连接结果: {status}")
        
        if status[0]:
            print("🎉 连接成功!")
            
            # 尝试简单的电机状态读取
            print("\n📊 尝试读取电机状态...")
            try:
                # 这里我们只尝试连接，不进行扭矩操作
                print("✅ 连接建立，准备进行后续操作")
                hand.disconnect()
                return True
                
            except Exception as e:
                print(f"❌ 电机操作失败: {e}")
                hand.disconnect()
                return False
        else:
            print(f"❌ 连接失败: {status[1]}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def verify_dynamixel_wizard():
    print("\n🔧 Dynamixel Wizard验证建议:")
    print("=" * 40)
    print("请在Dynamixel Wizard 2.0中确认:")
    print("1. 📡 端口: COM8")
    print("2. 📡 波特率: 3000000 (3Mbps)")
    print("3. 📋 协议: 2.0")
    print("4. 🔍 扫描范围: ID 1-17")
    print("5. 🔍 点击扫描，确认能看到所有17个电机")
    
    result = input("\n❓ 在Dynamixel Wizard中能看到所有电机吗? (y/n): ").lower()
    return result == 'y'

if __name__ == "__main__":
    print("🤖 ORCA机械手连接状态确认")
    print("=" * 50)
    
    # 首先确认Dynamixel Wizard状态
    wizard_ok = verify_dynamixel_wizard()
    
    if wizard_ok:
        print("\n✅ Dynamixel Wizard确认电机可见")
        print("继续测试ORCA Core连接...")
        
        success = test_connection_status()
        
        if success:
            print("\n🎉 连接测试成功!")
            print("可以继续进行张力调节和校准")
        else:
            print("\n❌ ORCA Core连接失败")
            print("可能的原因:")
            print("• 端口配置不匹配")
            print("• 波特率设置不正确")
            print("• 电机ID配置问题")
    else:
        print("\n❌ 请先在Dynamixel Wizard中确认电机连接")
        print("如果在Wizard中也看不到电机，请检查:")
        print("• U2D2连接")
        print("• 电源供应")
        print("• 电机菊花链连接")
