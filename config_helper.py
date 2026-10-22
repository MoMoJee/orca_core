#!/usr/bin/env python3
"""
根据Dynamixel Wizard扫描结果调整ORCA配置
"""

def generate_config_from_wizard():
    print("🔧 ORCA配置调整助手")
    print("=" * 40)
    
    print("\n📋 请根据Dynamixel Wizard的扫描结果回答以下问题:")
    
    # 获取检测到的电机ID
    print("\n1. 在Dynamixel Wizard中检测到了哪些电机ID？")
    print("   (例如: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)")
    detected_ids = input("   请输入检测到的ID (用逗号分隔): ")
    
    # 获取波特率
    print("\n2. 这些电机的波特率是多少？")
    print("   (常见值: 57600, 1000000, 3000000)")
    baudrate = input("   请输入波特率: ")
    
    # 获取协议版本
    print("\n3. 协议版本是多少？")
    print("   (1.0 或 2.0)")
    protocol = input("   请输入协议版本: ")
    
    # 生成建议的配置
    print("\n🎯 建议的配置修改:")
    print("=" * 40)
    
    try:
        ids = [int(x.strip()) for x in detected_ids.split(',')]
        print(f"motor_ids: {ids}")
        print(f"baudrate: {int(baudrate)}")
        print(f"protocol: {protocol}")
        
        # 检查是否需要调整ORCA配置
        expected_ids = list(range(1, 18))  # ORCA期望的ID 1-17
        
        if set(ids) != set(expected_ids):
            print("\n⚠️ 警告: 检测到的电机ID与ORCA期望的不匹配")
            print(f"ORCA期望: {expected_ids}")
            print(f"实际检测: {ids}")
            print("\n可能的解决方案:")
            print("1. 在Dynamixel Wizard中重新设置电机ID为1-17")
            print("2. 修改ORCA配置文件以匹配检测到的ID")
        
        if int(baudrate) != 3000000:
            print(f"\n⚠️ 警告: 波特率 {baudrate} 与ORCA默认值3000000不匹配")
            print("建议在Dynamixel Wizard中将所有电机波特率设置为3000000")
        
        return {
            'motor_ids': ids,
            'baudrate': int(baudrate),
            'protocol': float(protocol)
        }
        
    except Exception as e:
        print(f"❌ 配置解析失败: {e}")
        return None

if __name__ == "__main__":
    # 首先提醒检查Dynamixel Wizard
    print("📢 请确保:")
    print("1. 已运行端口清理工具")
    print("2. 在Dynamixel Wizard中成功扫描到电机")
    print("3. 记录下检测到的电机信息")
    
    proceed = input("\n❓ 是否已在Dynamixel Wizard中看到电机? (y/n): ")
    
    if proceed.lower() == 'y':
        config = generate_config_from_wizard()
        if config:
            print("\n✅ 配置分析完成!")
            print("我将帮您调整ORCA配置文件")
    else:
        print("\n📋 请先:")
        print("1. 打开Dynamixel Wizard 2.0")
        print("2. 设置端口COM8")
        print("3. 设置协议2.0")
        print("4. 尝试不同波特率扫描")
        print("5. 记录扫描结果")
        print("6. 然后重新运行此脚本")
