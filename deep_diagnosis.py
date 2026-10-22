#!/usr/bin/env python3
"""
深度硬件诊断工具
检查U2D2和电机连接的各个层面
"""

import serial
import serial.tools.list_ports
import time
import subprocess

def check_system_com_ports():
    """检查系统COM端口状态"""
    print("🔍 检查系统COM端口...")
    
    # 列出所有可用端口
    ports = serial.tools.list_ports.comports()
    
    print("📋 系统中的所有串口:")
    for port in ports:
        print(f"  {port.device}: {port.description}")
        if 'COM8' in port.device:
            print(f"    ✅ 找到COM8: {port.description}")
            print(f"    📍 硬件ID: {port.hwid}")
            return True
    
    print("❌ 未找到COM8端口")
    return False

def check_u2d2_device():
    """检查U2D2设备状态"""
    print("\n🔧 检查U2D2设备状态...")
    
    try:
        # 在Windows中查看设备管理器信息
        result = subprocess.run(['wmic', 'path', 'Win32_SerialPort', 'get', 
                               'DeviceID,Description,Name'], 
                              capture_output=True, text=True)
        
        print("📋 串口设备详情:")
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # 跳过标题行
                if line.strip():
                    print(f"  {line.strip()}")
        
        # 特别检查COM8
        if 'COM8' in result.stdout:
            print("✅ COM8在设备管理器中可见")
            return True
        else:
            print("❌ COM8不在设备管理器中")
            return False
            
    except Exception as e:
        print(f"❌ 设备检查失败: {e}")
        return False

def test_raw_serial_communication():
    """测试原始串口通信"""
    print("\n📡 测试原始串口通信...")
    
    baudrates = [9600, 57600, 115200, 1000000, 3000000]
    
    for baudrate in baudrates:
        print(f"  🔍 测试波特率: {baudrate}")
        
        try:
            # 尝试打开端口
            ser = serial.Serial('COM8', baudrate, timeout=0.5)
            print(f"    ✅ 端口打开成功")
            
            # 发送简单的测试数据
            test_data = b'\xFF\xFF\x01\x02\x01\xFB'  # Dynamixel ping命令
            ser.write(test_data)
            time.sleep(0.1)
            
            # 尝试读取响应
            response = ser.read(100)
            ser.close()
            
            if response:
                print(f"    🎉 收到响应: {response.hex()}")
                return baudrate
            else:
                print(f"    ❌ 无响应")
                
        except Exception as e:
            print(f"    ❌ 错误: {e}")
    
    return None

def check_power_and_connections():
    """检查电源和连接状态"""
    print("\n⚡ 电源和连接检查指南:")
    print("=" * 40)
    
    checks = [
        "🔌 U2D2的USB连接是否牢固？",
        "💡 U2D2上是否有电源指示灯亮起？",
        "🔗 机械手到U2D2的连接线是否正确连接？",
        "⚡ 机械手的外部电源是否已连接并开启？",
        "🔴 机械手控制板上是否有电源指示灯？",
        "📱 是否尝试过重新插拔U2D2设备？"
    ]
    
    results = {}
    for check in checks:
        answer = input(f"{check} (y/n): ").lower().strip()
        results[check] = answer == 'y'
    
    return results

def suggest_solutions(port_exists, device_ok, comm_ok, power_checks):
    """根据检查结果建议解决方案"""
    print("\n🎯 诊断结果和建议:")
    print("=" * 40)
    
    if not port_exists:
        print("❌ COM8端口不存在")
        print("📋 建议:")
        print("  1. 重新插拔U2D2设备")
        print("  2. 检查USB线缆")
        print("  3. 尝试不同的USB端口")
        print("  4. 安装/更新U2D2驱动程序")
        
    elif not device_ok:
        print("❌ 设备管理器问题")
        print("📋 建议:")
        print("  1. 在设备管理器中查看是否有未知设备")
        print("  2. 右键点击COM8端口，选择'更新驱动程序'")
        print("  3. 卸载并重新安装设备")
        
    elif comm_ok:
        print("✅ 原始通信正常")
        print("📋 这说明硬件连接正常，问题可能在于:")
        print("  1. Dynamixel协议配置")
        print("  2. 电机ID设置")
        print("  3. Dynamixel Wizard设置")
        
    else:
        print("❌ 通信完全失败")
        
        # 分析电源检查结果
        power_issues = [k for k, v in power_checks.items() if not v]
        if power_issues:
            print("⚡ 发现电源相关问题:")
            for issue in power_issues:
                print(f"  - {issue}")
        
        print("📋 建议按优先级依次尝试:")
        print("  1. 【硬件】检查所有电源连接")
        print("  2. 【硬件】确保机械手主电源开启")
        print("  3. 【硬件】检查U2D2到机械手的连接线")
        print("  4. 【软件】重新安装U2D2驱动")
        print("  5. 【系统】重启电脑")

if __name__ == "__main__":
    print("🔬 ORCA机械手深度硬件诊断")
    print("=" * 50)
    
    # 系统级检查
    port_exists = check_system_com_ports()
    device_ok = check_u2d2_device()
    
    # 通信测试
    comm_baudrate = test_raw_serial_communication() if port_exists else None
    comm_ok = comm_baudrate is not None
    
    # 人工检查
    power_checks = check_power_and_connections()
    
    # 综合建议
    suggest_solutions(port_exists, device_ok, comm_ok, power_checks)
