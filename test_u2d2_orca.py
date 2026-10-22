"""
专门针对U2D2的ORCA机械手测试
基于您使用U2D2硬件的情况
"""

import time
from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS, COMM_RX_TIMEOUT

def test_u2d2_connection():
    """测试U2D2连接和通信"""
    
    print("🔧 U2D2 + ORCA机械手专项测试")
    print("=" * 50)
    
    DEVICENAME = 'COM8'
    PROTOCOL_VERSION = 2.0
    
    # U2D2 + ORCA推荐的波特率序列
    baudrates = [57600, 1000000, 2000000, 3000000]
    
    print(f"📡 目标设备: {DEVICENAME}")
    print(f"🔌 硬件: U2D2 → PHB → ORCA机械手")
    
    for baudrate in baudrates:
        print(f"\n⚡ 测试波特率: {baudrate}")
        
        try:
            # 创建端口和包处理器
            portHandler = PortHandler(DEVICENAME)
            packetHandler = PacketHandler(PROTOCOL_VERSION)
            
            # 打开端口
            if not portHandler.openPort():
                print(f"❌ 无法打开端口 {DEVICENAME}")
                continue
                
            # 设置波特率
            if not portHandler.setBaudRate(baudrate):
                print(f"❌ 无法设置波特率 {baudrate}")
                portHandler.closePort()
                continue
                
            print("✅ 端口连接成功")
            
            # 测试ping所有可能的电机ID
            found_motors = []
            total_tests = 17
            
            for motor_id in range(1, 18):
                print(f"  🔍 Ping电机ID {motor_id:2d}... ", end="")
                
                try:
                    # Protocol 2.0 ping
                    dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, motor_id)
                    
                    if dxl_comm_result == COMM_SUCCESS:
                        print(f"✅ 型号: {dxl_model_number}")
                        found_motors.append((motor_id, dxl_model_number))
                    elif dxl_comm_result == COMM_RX_TIMEOUT:
                        print("⏱️")
                    else:
                        print(f"❌ 错误: {dxl_comm_result}")
                        
                except Exception as e:
                    print(f"❌ 异常: {e}")
                    
                # 重要：给U2D2足够的处理时间
                time.sleep(0.05)
            
            portHandler.closePort()
            
            if found_motors:
                print(f"\n🎉 成功！在波特率 {baudrate} 下找到 {len(found_motors)} 个电机:")
                for motor_id, model in found_motors:
                    print(f"   📍 电机ID {motor_id}: 型号 {model}")
                    
                print(f"\n📝 配置文件更新建议:")
                print(f"   baudrate: {baudrate}")
                print(f"   port: {DEVICENAME}")
                
                return True, baudrate, found_motors
            else:
                print(f"❌ 波特率 {baudrate} 下未找到电机")
                
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            
    return False, None, []

def test_motor_details(motor_id, baudrate):
    """测试特定电机的详细信息"""
    
    print(f"\n🔬 详细测试电机ID {motor_id}")
    
    DEVICENAME = 'COM8'
    PROTOCOL_VERSION = 2.0
    
    try:
        portHandler = PortHandler(DEVICENAME)
        packetHandler = PacketHandler(PROTOCOL_VERSION)
        
        if not portHandler.openPort() or not portHandler.setBaudRate(baudrate):
            print("❌ 连接失败")
            return
            
        print("📋 读取电机详细信息:")
        
        # 型号号码
        model, result, error = packetHandler.read2ByteTxRx(portHandler, motor_id, 0)
        if result == COMM_SUCCESS:
            print(f"   型号: {model}")
            
        # 固件版本
        firmware, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 6)
        if result == COMM_SUCCESS:
            print(f"   固件: {firmware}")
            
        # 当前ID
        current_id, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 7)
        if result == COMM_SUCCESS:
            print(f"   ID: {current_id}")
            
        # 波特率设置
        baud_setting, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 8)
        if result == COMM_SUCCESS:
            baud_map = {1: 9600, 2: 57600, 3: 115200, 4: 1000000, 5: 2000000, 6: 3000000, 7: 4000000}
            actual_baud = baud_map.get(baud_setting, f"未知({baud_setting})")
            print(f"   配置波特率: {actual_baud}")
            
        # 扭矩状态
        torque, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, 64)
        if result == COMM_SUCCESS:
            print(f"   扭矩启用: {'是' if torque else '否'}")
            
        portHandler.closePort()
        
    except Exception as e:
        print(f"❌ 详细测试失败: {e}")

def check_u2d2_specific_issues():
    """检查U2D2特有的问题"""
    
    print("\n🔍 U2D2特有问题检查:")
    print("1. 确认U2D2上的TTL/RS485开关设置为TTL")
    print("2. 确认电压开关设置正确(通常5V)")
    print("3. 检查PHB是否有独立12V供电")
    print("4. 确认所有连接线缆完好")
    print("5. 检查是否有松动的连接")

if __name__ == "__main__":
    print("🤖 ORCA + U2D2 专项通信测试")
    print("=" * 50)
    
    # 主要测试
    success, working_baudrate, motors = test_u2d2_connection()
    
    if success:
        print(f"\n✅ 通信测试成功!")
        print(f"工作波特率: {working_baudrate}")
        print(f"检测到电机数量: {len(motors)}")
        
        # 测试第一个电机的详细信息
        if motors:
            first_motor_id = motors[0][0]
            test_motor_details(first_motor_id, working_baudrate)
            
        print("\n🎯 下一步: 更新配置文件并运行ORCA脚本")
        
    else:
        print("\n❌ 未检测到任何电机")
        check_u2d2_specific_issues()
        
        print("\n📞 建议联系ORCA技术支持:")
        print("• 确认U2D2设置是否正确")
        print("• 确认电机是否已正确配置ID和波特率")
        print("• 检查硬件连接")
        
        print("\n💡 可能的原因:")
        print("• U2D2开关设置错误")
        print("• 电机波特率与测试不匹配")
        print("• 电源供应问题")
        print("• 电机可能都是默认ID(需要先设置)")
        print("• 硬件故障")
