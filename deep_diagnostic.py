#!/usr/bin/env python3
"""
深度连接诊断工具
专门解决连接助手显示正常但实际脚本仍然失败的问题
"""

import time
import sys
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_serial_basic():
    """测试基础串口连接"""
    log("🔍 测试1: 基础串口连接")
    try:
        import serial
        ser = serial.Serial("COM8", 9600, timeout=1)
        log("✅ 低速连接成功")
        ser.close()
        
        # 测试高速连接
        ser = serial.Serial("COM8", 3000000, timeout=1)
        log("✅ 高速连接成功")
        ser.close()
        return True
    except Exception as e:
        log(f"❌ 串口连接失败: {e}")
        return False

def test_dynamixel_sdk():
    """测试Dynamixel SDK基础功能"""
    log("🔍 测试2: Dynamixel SDK基础功能")
    try:
        from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
        
        port_handler = PortHandler("COM8")
        packet_handler = PacketHandler(2.0)
        
        if not port_handler.openPort():
            log("❌ Dynamixel端口打开失败")
            return False
        
        if not port_handler.setBaudRate(3000000):
            log("❌ 波特率设置失败")
            port_handler.closePort()
            return False
        
        log("✅ Dynamixel SDK初始化成功")
        
        # 测试ping - 使用更短的超时
        port_handler.setPacketTimeout(100)  # 100ms超时
        
        log("🔍 尝试ping电机ID 1...")
        model, result, error = packet_handler.ping(port_handler, 1)
        
        if result == COMM_SUCCESS:
            log(f"✅ 电机ID 1响应成功，型号: {model}")
            success = True
        else:
            log(f"❌ 电机ID 1无响应: {packet_handler.getTxRxResult(result)}")
            success = False
        
        port_handler.closePort()
        return success
        
    except Exception as e:
        log(f"❌ Dynamixel SDK测试失败: {e}")
        return False

def test_orca_minimal():
    """测试ORCA最小化连接"""
    log("🔍 测试3: ORCA最小化连接")
    try:
        from orca_core.hardware.dynamixel_client import DynamixelClient
        
        # 只测试单个电机
        client = DynamixelClient([1], "COM8", 3000000)
        
        log("🔍 尝试ORCA连接...")
        client.connect()
        log("✅ ORCA连接成功")
        
        client.disconnect()
        log("✅ ORCA断开成功")
        return True
        
    except Exception as e:
        log(f"❌ ORCA连接失败: {e}")
        return False

def test_wizard_conflict():
    """测试Wizard冲突"""
    log("🔍 测试4: 检查Wizard进程冲突")
    try:
        import subprocess
        
        # 检查是否有Wizard进程
        cmd = 'tasklist | findstr /i "dynamixel"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            log("⚠️ 发现Dynamixel相关进程:")
            print(result.stdout)
            return False
        else:
            log("✅ 无Dynamixel冲突进程")
            return True
            
    except Exception as e:
        log(f"❌ 进程检查失败: {e}")
        return False

def diagnose_hardware_state():
    """诊断硬件状态"""
    log("🔍 测试5: 硬件状态诊断")
    
    # 检查设备管理器中的COM8
    import subprocess
    try:
        cmd = 'wmic path Win32_SerialPort where "DeviceID=\'COM8\'" get Description,PNPDeviceID'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if "FTDI" in result.stdout or "USB" in result.stdout:
            log("✅ COM8设备正常识别")
            print(result.stdout)
            return True
        else:
            log("❌ COM8设备识别异常")
            print(result.stdout)
            return False
            
    except Exception as e:
        log(f"❌ 设备检查失败: {e}")
        return False

def suggest_solutions(results):
    """根据测试结果给出建议"""
    log("\n📊 诊断结果分析")
    print("=" * 50)
    
    serial_ok = results.get('serial', False)
    dynamixel_ok = results.get('dynamixel', False)
    orca_ok = results.get('orca', False)
    wizard_ok = results.get('wizard', False)
    hardware_ok = results.get('hardware', False)
    
    if not serial_ok:
        log("🚨 串口层面问题")
        print("建议:")
        print("• 重新插拔U2D2 USB线")
        print("• 检查设备管理器中COM8状态")
        print("• 重启计算机")
        
    elif not dynamixel_ok:
        log("🚨 Dynamixel通信问题") 
        print("建议:")
        print("• 检查机械手电源是否稳定")
        print("• 检查U2D2到机械手的数据线")
        print("• 尝试在Dynamixel Wizard中重新扫描")
        
    elif not orca_ok:
        log("🚨 ORCA软件层问题")
        print("建议:")
        print("• 检查ORCA配置文件")
        print("• 尝试降低波特率")
        print("• 检查电机ID配置")
        
    else:
        log("🤔 所有测试都通过但脚本仍失败")
        print("可能原因:")
        print("• 特定脚本的问题")
        print("• 配置文件问题")
        print("• 多电机初始化问题")

def main():
    print("🔬 ORCA深度连接诊断")
    print("=" * 50)
    print("专门解决连接助手正常但脚本仍失败的问题")
    print()
    
    results = {}
    
    # 执行所有测试
    results['serial'] = test_serial_basic()
    time.sleep(1)
    
    results['dynamixel'] = test_dynamixel_sdk()
    time.sleep(1)
    
    results['orca'] = test_orca_minimal()
    time.sleep(1)
    
    results['wizard'] = test_wizard_conflict()
    time.sleep(1)
    
    results['hardware'] = diagnose_hardware_state()
    
    # 分析结果
    suggest_solutions(results)
    
    print(f"\n🎯 测试完成时间: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
