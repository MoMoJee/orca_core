from orca_core.hardware.dynamixel_client import DynamixelClient
import time

def scan_motors():
    """扫描可用的电机"""
    port = "COM8"
    baudrates = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000]
    motor_ids = range(1, 18)  # 扫描ID 1-17
    
    print(f"正在扫描端口 {port} 上的电机...")
    
    for baudrate in baudrates:
        print(f"\n尝试波特率: {baudrate}")
        
        for motor_id in motor_ids:
            try:
                # 创建客户端，只连接一个电机
                client = DynamixelClient([motor_id], port, baudrate)
                
                # 尝试连接
                try:
                    client.connect()
                    print(f"✅ 找到电机! ID: {motor_id}, 波特率: {baudrate}")
                    client.disconnect()
                    return motor_id, baudrate
                except:
                    client.disconnect()
                    continue
                    
            except Exception as e:
                continue
    
    print("❌ 未找到任何响应的电机")
    return None, None

if __name__ == "__main__":
    motor_id, baudrate = scan_motors()
    if motor_id:
        print(f"\n建议配置: 电机ID {motor_id}, 波特率 {baudrate}")
    else:
        print("\n请检查:")
        print("1. 机械手是否已通电")
        print("2. USB连接是否正常")
        print("3. COM端口是否正确")
        print("4. 电机是否损坏")
