#!/usr/bin/env python3
"""
简化版ORCA恢复工具
既然您成功运行过，问题应该是可恢复的状态问题
"""

import time
import subprocess

def simple_recovery():
    print("🔄 ORCA简化恢复流程")
    print("=" * 50)
    print("既然您曾经成功运行过，我们来快速恢复状态")
    print()
    
    # 步骤1: 基础清理
    print("步骤1: 清理进程...")
    try:
        subprocess.run('taskkill /f /im "DynamixelWizard2.exe" 2>nul', shell=True)
        print("✅ Dynamixel Wizard已关闭")
    except:
        pass
    
    # 步骤2: 测试当前状态
    print("\n步骤2: 测试当前连接状态...")
    try:
        import serial
        ser = serial.Serial("COM8", 9600, timeout=1)
        ser.close()
        print("✅ COM8端口可访问")
    except Exception as e:
        print(f"❌ COM8端口问题: {e}")
        return False
    
    # 步骤3: 快速Dynamixel测试
    print("\n步骤3: 快速Dynamixel测试...")
    
    # 尝试几个常用波特率
    baudrates = [57600, 115200, 1000000, 3000000]
    
    for baud in baudrates:
        print(f"尝试波特率: {baud}")
        if quick_ping_test(baud):
            print(f"✅ 在波特率 {baud} 下发现响应！")
            
            if baud == 3000000:
                print("🎉 目标波特率连接成功！")
                return True
            else:
                print(f"⚠️ 当前在 {baud} 波特率下工作，但配置要求 3000000")
                print("💡 这可能是问题原因 - 波特率不匹配")
                return "baudrate_mismatch"
    
    print("❌ 所有波特率都无响应")
    return False

def quick_ping_test(baudrate):
    """快速ping测试，短超时避免卡死"""
    try:
        from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
        
        port_handler = PortHandler("COM8")
        if not port_handler.openPort():
            return False
        
        if not port_handler.setBaudRate(baudrate):
            port_handler.closePort()
            return False
        
        packet_handler = PacketHandler(2.0)
        port_handler.setPacketTimeout(30)  # 30ms超时
        
        # 快速ping
        model, result, error = packet_handler.ping(port_handler, 1)
        
        port_handler.closePort()
        return result == COMM_SUCCESS
        
    except Exception:
        return False

def main():
    result = simple_recovery()
    
    print(f"\n📊 恢复结果: {result}")
    print("=" * 50)
    
    if result is True:
        print("🎉 连接已恢复！现在可以运行ORCA脚本了")
        print("\n💡 试试运行:")
        print("python scripts/main_demo.py")
        
    elif result == "baudrate_mismatch":
        print("🔧 发现波特率不匹配问题")
        print("解决方案:")
        print("1. 打开Dynamixel Wizard")
        print("2. 用当前工作的波特率连接电机")
        print("3. 将所有电机的波特率设置为 3000000")
        print("4. 保存设置后重新尝试Python脚本")
        
    else:
        print("❌ 快速恢复未成功")
        print("\n🔧 手动恢复建议:")
        print("1. 完全断电重启:")
        print("   • 拔掉机械手电源 30秒")
        print("   • 拔掉U2D2 USB线 30秒")
        print("   • 重新连接并等待5秒")
        print()
        print("2. 用Dynamixel Wizard验证:")
        print("   • 打开Wizard，扫描电机")
        print("   • 如果能扫描到，说明硬件正常")
        print("   • 检查电机的波特率设置")
        print()
        print("3. 告诉我更多信息:")
        print("   • 您最后一次成功运行是什么时候？")
        print("   • 成功运行的是哪个脚本？")
        print("   • 在Dynamixel Wizard中能扫描到电机吗？")

if __name__ == "__main__":
    main()
