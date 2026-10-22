#!/usr/bin/env python3
"""
测试Protocol 1.0通信
ORCA机械手可能使用旧版协议
"""

import sys
import time
from dynamixel_sdk import *

def test_protocol_1():
    """测试Protocol 1.0通信"""
    
    DEVICENAME = 'COM8'
    PROTOCOL_VERSION = 1.0  # 改为Protocol 1.0
    BAUDRATES = [9600, 57600, 115200, 1000000]  # Protocol 1.0常用波特率
    
    print("🔄 测试Protocol 1.0通信...")
    print(f"端口: {DEVICENAME}")
    
    for baudrate in BAUDRATES:
        print(f"\n⚡ 测试波特率: {baudrate} (Protocol 1.0)")
        
        portHandler = PortHandler(DEVICENAME)
        packetHandler = PacketHandler(PROTOCOL_VERSION)
        
        if not portHandler.openPort():
            print("❌ 无法打开端口")
            continue
            
        if not portHandler.setBaudRate(baudrate):
            print("❌ 无法设置波特率")
            portHandler.closePort()
            continue
            
        print("✅ 端口连接成功")
        
        found_motors = []
        
        # 在Protocol 1.0中，ping的实现略有不同
        for motor_id in range(1, 18):
            print(f"  🔍 Ping电机ID {motor_id}...", end=" ")
            
            # 使用ping检测
            dxl_comm_result, dxl_error = packetHandler.ping(portHandler, motor_id)
            
            if dxl_comm_result == COMM_SUCCESS:
                print("✅ 响应!")
                found_motors.append(motor_id)
            elif dxl_comm_result == COMM_RX_TIMEOUT:
                print("⏱️ 超时")
            else:
                print(f"❌ 错误: {packetHandler.getTxRxResult(dxl_comm_result)}")
                
            time.sleep(0.05)  # Protocol 1.0需要更长延迟
        
        portHandler.closePort()
        
        if found_motors:
            print(f"\n🎉 Protocol 1.0下找到 {len(found_motors)} 个电机: {found_motors}")
            return baudrate, found_motors
        else:
            print(f"❌ Protocol 1.0波特率 {baudrate} 下未找到电机")
    
    return None, []

def test_broadcast_scan():
    """尝试广播扫描"""
    print("\n📡 尝试广播扫描...")
    
    DEVICENAME = 'COM8'
    
    for protocol in [1.0, 2.0]:
        print(f"\nProtocol {protocol}:")
        
        portHandler = PortHandler(DEVICENAME)
        packetHandler = PacketHandler(protocol)
        
        if not portHandler.openPort():
            continue
            
        if not portHandler.setBaudRate(1000000):  # 常用波特率
            portHandler.closePort()
            continue
            
        # 尝试读取广播地址
        try:
            if protocol == 1.0:
                # Protocol 1.0广播ID是254
                result, error = packetHandler.ping(portHandler, 254)
                print(f"  广播ping结果: {packetHandler.getTxRxResult(result)}")
            else:
                # Protocol 2.0广播ID是254
                model, result, error = packetHandler.ping(portHandler, 254)
                print(f"  广播ping结果: {packetHandler.getTxRxResult(result)}")
        except Exception as e:
            print(f"  广播ping异常: {e}")
            
        portHandler.closePort()

if __name__ == "__main__":
    print("🔧 ORCA机械手协议版本测试")
    print("=" * 40)
    
    # 首先测试Protocol 1.0
    baudrate, motors = test_protocol_1()
    
    if motors:
        print(f"\n✅ 成功！Protocol 1.0，波特率: {baudrate}")
        print("📝 请更新配置文件使用Protocol 1.0")
    else:
        print("\n❌ Protocol 1.0测试失败")
        
    # 尝试广播扫描
    test_broadcast_scan()
    
    print("\n📊 测试总结:")
    print("1. 绿光闪烁表明硬件正在接收数据")
    print("2. 如果Protocol 1.0也失败，可能需要:")
    print("   - 检查是否需要特殊的初始化序列")
    print("   - 确认电机是否在bootloader模式")
    print("   - 联系ORCA技术支持获取具体的通信协议")
