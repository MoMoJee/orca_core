#!/usr/bin/env python3
"""
基础Dynamixel通信测试
用于验证ORCA机械手的基本连接
"""

import sys
import time
from dynamixel_sdk import *

def test_basic_communication():
    """测试基础的Dynamixel通信"""
    
    # 连接参数
    DEVICENAME = 'COM8'
    PROTOCOL_VERSION = 2.0
    BAUDRATES = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000]
    
    # 基本地址 (适用于大多数Dynamixel电机)
    ADDR_ID = 7
    ADDR_BAUDRATE = 8
    ADDR_MODEL_NUMBER = 0
    
    print("🔍 开始ORCA机械手基础通信测试...")
    print(f"端口: {DEVICENAME}")
    
    for baudrate in BAUDRATES:
        print(f"\n⚡ 测试波特率: {baudrate}")
        
        # 初始化端口
        portHandler = PortHandler(DEVICENAME)
        packetHandler = PacketHandler(PROTOCOL_VERSION)
        
        # 打开端口
        if not portHandler.openPort():
            print("❌ 无法打开端口")
            continue
            
        # 设置波特率
        if not portHandler.setBaudRate(baudrate):
            print("❌ 无法设置波特率")
            portHandler.closePort()
            continue
            
        print("✅ 端口连接成功")
        
        # 尝试ping所有可能的电机ID (1-17)
        found_motors = []
        
        for motor_id in range(1, 18):
            print(f"  🔍 Ping电机ID {motor_id}...", end=" ")
            
            # 使用ping来检测电机
            dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, motor_id)
            
            if dxl_comm_result == COMM_SUCCESS:
                print(f"✅ 找到! 型号: {dxl_model_number}")
                found_motors.append((motor_id, dxl_model_number))
            elif dxl_comm_result == COMM_RX_TIMEOUT:
                print("⏱️ 超时")
            else:
                print(f"❌ 错误: {packetHandler.getTxRxResult(dxl_comm_result)}")
                
            # 短暂延迟避免通信冲突
            time.sleep(0.01)
        
        portHandler.closePort()
        
        if found_motors:
            print(f"\n🎉 在波特率 {baudrate} 下找到 {len(found_motors)} 个电机:")
            for motor_id, model in found_motors:
                print(f"   ID {motor_id}: 型号 {model}")
            return baudrate, found_motors
        else:
            print(f"❌ 在波特率 {baudrate} 下未找到任何电机")
    
    print("\n❌ 未在任何波特率下找到电机")
    return None, []

def test_specific_motor(motor_id, baudrate):
    """测试特定电机的详细信息"""
    DEVICENAME = 'COM8'
    PROTOCOL_VERSION = 2.0
    
    print(f"\n🔧 详细测试电机 ID {motor_id} (波特率: {baudrate})")
    
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    
    if not portHandler.openPort():
        print("❌ 无法打开端口")
        return
        
    if not portHandler.setBaudRate(baudrate):
        print("❌ 无法设置波特率")
        portHandler.closePort()
        return
    
    try:
        # 读取型号号码
        model_number, result, error = packetHandler.read2ByteTxRx(portHandler, motor_id, 0)
        if result == COMM_SUCCESS:
            print(f"📋 型号号码: {model_number}")
        
        # 读取固件版本
        firmware, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 6)
        if result == COMM_SUCCESS:
            print(f"🔧 固件版本: {firmware}")
            
        # 读取当前位置
        position, result, error = packetHandler.read4ByteTxRx(portHandler, motor_id, 132)
        if result == COMM_SUCCESS:
            print(f"📍 当前位置: {position}")
            
        # 读取温度
        temp, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 146)
        if result == COMM_SUCCESS:
            print(f"🌡️ 温度: {temp}°C")
            
    except Exception as e:
        print(f"❌ 详细测试失败: {e}")
    
    portHandler.closePort()

if __name__ == "__main__":
    print("🤖 ORCA机械手通信诊断工具")
    print("=" * 40)
    
    baudrate, motors = test_basic_communication()
    
    if motors:
        print(f"\n✅ 成功！建议使用波特率: {baudrate}")
        print("📝 建议的配置:")
        print(f"   port: COM8")
        print(f"   baudrate: {baudrate}")
        
        # 测试第一个找到的电机的详细信息
        first_motor = motors[0][0]
        test_specific_motor(first_motor, baudrate)
        
    else:
        print("\n🛠️ 故障排除建议:")
        print("1. 确认机械手电源已开启")
        print("2. 检查USB连接")
        print("3. 确认COM8是正确的端口")
        print("4. 联系ORCA技术支持")
