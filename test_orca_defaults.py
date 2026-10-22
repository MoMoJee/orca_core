#!/usr/bin/env python3
"""
根据ORCA官方文档进行正确的通信测试
默认波特率: 57600, Protocol 2.0
"""

import time
from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS, COMM_RX_TIMEOUT

def test_orca_defaults():
    """使用ORCA默认设置测试"""
    
    DEVICENAME = 'COM8'
    PROTOCOL_VERSION = 2.0
    DEFAULT_BAUDRATE = 57600  # ORCA默认波特率
    TARGET_BAUDRATE = 3000000  # ORCA目标波特率
    
    print("🤖 ORCA机械手官方设置测试")
    print("=" * 40)
    print(f"端口: {DEVICENAME}")
    print(f"协议: {PROTOCOL_VERSION}")
    
    # 首先尝试默认波特率57600
    print(f"\n📡 步骤1: 测试默认波特率 {DEFAULT_BAUDRATE}")
    
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    
    if not portHandler.openPort():
        print("❌ 无法打开端口")
        return False
        
    if not portHandler.setBaudRate(DEFAULT_BAUDRATE):
        print("❌ 无法设置波特率")
        portHandler.closePort()
        return False
        
    print("✅ 端口连接成功")
    
    found_motors = []
    
    # 扫描ID 1-17 (ORCA配置范围)
    for motor_id in range(1, 18):
        print(f"  🔍 扫描电机ID {motor_id}...", end=" ")
        
        try:
            # 使用ping检测电机
            dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, motor_id)
            
            if dxl_comm_result == COMM_SUCCESS:
                print(f"✅ 找到! 型号: {dxl_model_number}")
                found_motors.append((motor_id, dxl_model_number))
            elif dxl_comm_result == COMM_RX_TIMEOUT:
                print("⏱️ 超时")
            else:
                print(f"❌ 错误代码: {dxl_comm_result}")
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            
        # 重要: ORCA文档建议的延迟
        time.sleep(0.1)
    
    portHandler.closePort()
    
    if found_motors:
        print(f"\n🎉 成功找到 {len(found_motors)} 个电机!")
        for motor_id, model in found_motors:
            print(f"   电机ID {motor_id}: 型号 {model}")
            
        print(f"\n📝 配置建议:")
        print(f"   port: COM8")
        print(f"   baudrate: {DEFAULT_BAUDRATE}")
        print(f"   protocol: 2.0")
        
        return True
    else:
        print(f"\n❌ 在默认波特率 {DEFAULT_BAUDRATE} 下未找到电机")
        
        # 尝试目标波特率
        print(f"\n📡 步骤2: 测试目标波特率 {TARGET_BAUDRATE}")
        
        if not portHandler.openPort():
            print("❌ 无法重新打开端口")
            return False
            
        if not portHandler.setBaudRate(TARGET_BAUDRATE):
            print("❌ 无法设置高波特率")
            portHandler.closePort()
            return False
            
        found_high = []
        for motor_id in range(1, 18):
            print(f"  🔍 高速扫描ID {motor_id}...", end=" ")
            
            try:
                dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, motor_id)
                
                if dxl_comm_result == COMM_SUCCESS:
                    print(f"✅ 找到! 型号: {dxl_model_number}")
                    found_high.append((motor_id, dxl_model_number))
                else:
                    print("❌")
                    
            except Exception:
                print("❌")
                
            time.sleep(0.05)
        
        portHandler.closePort()
        
        if found_high:
            print(f"\n🎉 在高波特率下找到 {len(found_high)} 个电机!")
            return True
            
        return False

def check_single_motor_details(motor_id=1, baudrate=57600):
    """检查单个电机的详细信息"""
    print(f"\n🔧 检查电机ID {motor_id} 的详细信息")
    
    DEVICENAME = 'COM8'
    PROTOCOL_VERSION = 2.0
    
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    
    if not portHandler.openPort() or not portHandler.setBaudRate(baudrate):
        print("❌ 连接失败")
        return
    
    try:
        # 检查基本信息
        print(f"📋 读取电机 {motor_id} 的信息:")
        
        # 型号号码 (地址 0)
        model, result, error = packetHandler.read2ByteTxRx(portHandler, motor_id, 0)
        if result == COMM_SUCCESS:
            print(f"   型号: {model}")
        else:
            print(f"   型号读取失败: {result}")
            
        # 固件版本 (地址 6) 
        firmware, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 6)
        if result == COMM_SUCCESS:
            print(f"   固件: {firmware}")
            
        # ID (地址 7)
        id_val, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 7)
        if result == COMM_SUCCESS:
            print(f"   当前ID: {id_val}")
            
        # 波特率 (地址 8)
        baud, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 8)
        if result == COMM_SUCCESS:
            baud_rates = {1: 9600, 2: 57600, 3: 115200, 4: 1000000, 5: 2000000, 6: 3000000, 7: 4000000}
            actual_baud = baud_rates.get(baud, f"未知({baud})")
            print(f"   波特率: {actual_baud}")
            
    except Exception as e:
        print(f"❌ 详细检查失败: {e}")
        
    portHandler.closePort()

if __name__ == "__main__":
    # 主测试
    success = test_orca_defaults()
    
    if success:
        print("\n✅ 基础连接成功!")
        # 检查第一个电机的详细信息
        check_single_motor_details(1, 57600)
    else:
        print("\n🔍 故障排除建议:")
        print("1. 确认机械手电源开启且指示灯正常")
        print("2. 确认USB连接稳定")
        print("3. 可能需要使用Dynamixel Wizard 2.0进行初始设置")
        print("4. 检查是否需要先设置电机ID (可能都是默认ID 1)")
        print("5. 联系ORCA技术支持")
        
        print("\n📞 ORCA支持联系方式:")
        print("   Discord: https://discord.com/invite/hk9PGKShPK")
        print("   网站: https://orcahand.com")
