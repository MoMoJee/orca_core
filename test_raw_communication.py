#!/usr/bin/env python3
"""
底层Dynamixel通信测试
直接发送原始字节进行通信诊断
"""

import serial
import time
import struct

def calculate_checksum_v1(data):
    """计算Protocol 1.0校验和"""
    return (~sum(data)) & 0xFF

def calculate_checksum_v2(data):
    """计算Protocol 2.0校验和"""
    crc = 0
    crc_table = [
        0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
        0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022
    ]
    
    for byte in data:
        tbl_idx = ((crc >> 12) ^ (byte >> 4)) & 0x0F
        crc = ((crc << 4) ^ crc_table[tbl_idx]) & 0xFFFF
        tbl_idx = ((crc >> 12) ^ (byte & 0x0F)) & 0x0F
        crc = ((crc << 4) ^ crc_table[tbl_idx]) & 0xFFFF
    
    return crc

def test_raw_communication():
    """测试原始串口通信"""
    print("🔍 开始底层通信测试...")
    
    try:
        # 打开串口
        ser = serial.Serial(
            port='COM8',
            baudrate=57600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1.0
        )
        
        print(f"✅ 串口连接成功: {ser.name}")
        print(f"📡 波特率: {ser.baudrate}")
        
        # 清空缓冲区
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # 测试基本连通性
        print("\n🔧 测试1: 发送简单数据...")
        test_data = b'\xFF\xFF\x01\x02\x01\xFB'  # Protocol 1.0 ping to ID 1
        ser.write(test_data)
        time.sleep(0.1)
        
        response = ser.read(100)
        if response:
            print(f"✅ 收到响应: {response.hex()}")
        else:
            print("❌ 无响应")
            
        # 测试Protocol 2.0 ping
        print("\n🔧 测试2: Protocol 2.0 Ping电机ID 1...")
        # Protocol 2.0 ping frame: [0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM..., CRC_L, CRC_H]
        ping_packet = bytearray([0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x03, 0x00, 0x01])
        crc = calculate_checksum_v2(ping_packet)
        ping_packet.extend(struct.pack('<H', crc))
        
        print(f"📤 发送: {ping_packet.hex()}")
        ser.write(ping_packet)
        time.sleep(0.1)
        
        response = ser.read(100)
        if response:
            print(f"✅ 收到响应: {response.hex()}")
            return True
        else:
            print("❌ 无响应")
            
        # 尝试广播ping
        print("\n🔧 测试3: 广播Ping...")
        broadcast_packet = bytearray([0xFF, 0xFF, 0xFD, 0x00, 0xFE, 0x03, 0x00, 0x01])
        crc = calculate_checksum_v2(broadcast_packet)
        broadcast_packet.extend(struct.pack('<H', crc))
        
        print(f"📤 发送广播: {broadcast_packet.hex()}")
        ser.write(broadcast_packet)
        time.sleep(0.5)  # 广播需要更长时间
        
        response = ser.read(100)
        if response:
            print(f"✅ 广播响应: {response.hex()}")
            return True
        else:
            print("❌ 无广播响应")
            
        return False
        
    except Exception as e:
        print(f"❌ 串口测试失败: {e}")
        return False
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def test_different_protocols():
    """测试不同协议和波特率组合"""
    print("\n🔄 测试多种协议组合...")
    
    baudrates = [9600, 57600, 115200, 1000000]
    
    for baudrate in baudrates:
        print(f"\n⚡ 测试波特率: {baudrate}")
        
        try:
            ser = serial.Serial('COM8', baudrate, timeout=0.5)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            
            # 发送简单的字节序列
            test_sequences = [
                b'\xFF\xFF\x01\x02\x01\xFB',  # Protocol 1.0 ping ID 1
                b'\xFF\xFF\x02\x02\x01\xFA',  # Protocol 1.0 ping ID 2  
                b'\xFF\xFF\xFE\x02\x01\xFF',  # Protocol 1.0 broadcast ping
            ]
            
            for i, seq in enumerate(test_sequences):
                print(f"  📤 序列{i+1}: {seq.hex()}", end=" ")
                ser.write(seq)
                time.sleep(0.1)
                
                response = ser.read(50)
                if response:
                    print(f"✅ 响应: {response.hex()}")
                    ser.close()
                    return baudrate, response
                else:
                    print("❌")
                    
            ser.close()
            
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            
    return None, None

def check_orca_specific():
    """检查ORCA特定的通信模式"""
    print("\n🤖 检查ORCA特定通信...")
    
    try:
        ser = serial.Serial('COM8', 57600, timeout=1.0)
        
        # ORCA可能使用的特殊序列
        orca_sequences = [
            b'\xFF\xFF\xFF\xFF',  # 可能的同步序列
            b'\x00\x00\x00\x00',  # 空序列
            b'\xAA\x55\xAA\x55',  # 交替模式
            b'ORCA',              # 文本命令
            b'\xFF\xFF\xFD\x00\xFE\x06\x00\x83\x00\x07\x00\x52\x1D',  # 可能的复位命令
        ]
        
        for i, seq in enumerate(orca_sequences):
            print(f"  🔍 ORCA序列{i+1}: {seq}", end=" ")
            ser.write(seq)
            time.sleep(0.2)
            
            response = ser.read(100)
            if response:
                print(f"✅ 响应: {response}")
                return True
            else:
                print("❌")
                
        ser.close()
        return False
        
    except Exception as e:
        print(f"❌ ORCA测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🔬 ORCA机械手底层通信诊断")
    print("=" * 50)
    
    # 基础测试
    basic_success = test_raw_communication()
    
    if not basic_success:
        # 尝试不同协议
        baudrate, response = test_different_protocols()
        
        if baudrate:
            print(f"\n🎉 在波特率 {baudrate} 下检测到响应!")
            print(f"响应数据: {response.hex()}")
        else:
            # ORCA特定测试
            orca_success = check_orca_specific()
            
            if not orca_success:
                print("\n📋 诊断结果:")
                print("1. ✅ 串口通信正常 (能发送数据)")
                print("2. ✅ 硬件接收正常 (绿光闪烁)")
                print("3. ❌ 无任何协议响应")
                print("\n💡 可能的问题:")
                print("• 电机可能处于保护模式")
                print("• 需要特殊的唤醒序列")
                print("• 硬件可能有故障")
                print("• 可能需要物理复位")
                
                print("\n🛠️ 建议尝试:")
                print("1. 重新上电机械手 (完全断电30秒)")
                print("2. 检查是否有物理复位按钮")
                print("3. 联系ORCA技术支持获取初始化序列")
                print("4. 检查保修和硬件状态")
    else:
        print("\n✅ 检测到基础通信!")
