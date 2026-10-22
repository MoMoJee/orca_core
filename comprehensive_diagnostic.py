#!/usr/bin/env python3
"""
ORCA机械手问题根源诊断工具
基于用户观察到的现象进行系统性分析
"""

import time
import serial
import subprocess
import sys
from datetime import datetime

class ORCADiagnostic:
    def __init__(self):
        self.port = "COM8"
        self.baudrate = 3000000
        self.test_results = {}
        
    def log(self, message):
        """带时间戳的日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def test_1_basic_port_access(self):
        """测试1：基础端口访问"""
        self.log("🔍 测试1: 基础端口访问")
        
        try:
            ser = serial.Serial(self.port, 9600, timeout=1)
            ser.close()
            self.test_results['basic_port'] = True
            self.log("✅ COM8端口基础访问正常")
            return True
        except Exception as e:
            self.test_results['basic_port'] = False
            self.log(f"❌ COM8端口访问失败: {e}")
            return False
    
    def test_2_port_exclusive_access(self):
        """测试2：端口独占访问测试"""
        self.log("🔍 测试2: 端口独占访问")
        
        try:
            # 第一个连接
            ser1 = serial.Serial(self.port, 9600, timeout=1)
            self.log("✅ 第一个连接建立成功")
            
            try:
                # 尝试第二个连接（应该失败）
                ser2 = serial.Serial(self.port, 9600, timeout=1)
                ser2.close()
                self.log("⚠️ 警告: 端口允许多重访问（不正常）")
                self.test_results['exclusive_access'] = False
            except Exception:
                self.log("✅ 端口正确拒绝多重访问")
                self.test_results['exclusive_access'] = True
            
            ser1.close()
            return True
            
        except Exception as e:
            self.log(f"❌ 独占访问测试失败: {e}")
            self.test_results['exclusive_access'] = False
            return False
    
    def test_3_dynamixel_basic_ping(self):
        """测试3：基础Dynamixel Ping"""
        self.log("🔍 测试3: Dynamixel基础通信")
        
        try:
            from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
            
            port_handler = PortHandler(self.port)
            packet_handler = PacketHandler(2.0)
            
            if not port_handler.openPort():
                self.log("❌ 无法打开Dynamixel端口")
                self.test_results['dynamixel_ping'] = False
                return False
                
            if not port_handler.setBaudRate(self.baudrate):
                self.log("❌ 无法设置波特率")
                port_handler.closePort()
                self.test_results['dynamixel_ping'] = False
                return False
            
            self.log(f"✅ Dynamixel端口已打开，波特率: {self.baudrate}")
            
            # 尝试ping电机ID 1
            dxl_model_number, dxl_comm_result, dxl_error = packet_handler.ping(port_handler, 1)
            
            if dxl_comm_result == COMM_SUCCESS:
                self.log(f"✅ 电机ID 1响应正常，型号: {dxl_model_number}")
                self.test_results['dynamixel_ping'] = True
                result = True
            else:
                self.log(f"❌ 电机ID 1无响应，错误: {packet_handler.getTxRxResult(dxl_comm_result)}")
                self.test_results['dynamixel_ping'] = False
                result = False
            
            port_handler.closePort()
            return result
            
        except Exception as e:
            self.log(f"❌ Dynamixel测试异常: {e}")
            self.test_results['dynamixel_ping'] = False
            return False
    
    def test_4_resource_cleanup(self):
        """测试4：资源清理测试"""
        self.log("🔍 测试4: 资源清理验证")
        
        try:
            from dynamixel_sdk import PortHandler
            
            # 创建连接
            port_handler = PortHandler(self.port)
            port_handler.openPort()
            port_handler.setBaudRate(self.baudrate)
            self.log("✅ 创建Dynamixel连接")
            
            # 正确关闭
            port_handler.closePort()
            self.log("✅ 正确关闭连接")
            
            # 等待短暂时间
            time.sleep(0.5)
            
            # 尝试重新连接
            port_handler2 = PortHandler(self.port)
            if port_handler2.openPort():
                self.log("✅ 资源正确释放，可重新连接")
                port_handler2.closePort()
                self.test_results['resource_cleanup'] = True
                return True
            else:
                self.log("❌ 资源未正确释放")
                self.test_results['resource_cleanup'] = False
                return False
                
        except Exception as e:
            self.log(f"❌ 资源清理测试失败: {e}")
            self.test_results['resource_cleanup'] = False
            return False
    
    def test_5_orca_connection_simulation(self):
        """测试5：模拟ORCA连接过程"""
        self.log("🔍 测试5: 模拟ORCA连接过程")
        
        try:
            from orca_core.hardware.dynamixel_client import DynamixelClient
            
            # 只测试前3个电机以减少错误输出
            motor_ids = [1, 2, 3]
            client = DynamixelClient(motor_ids, self.port, self.baudrate)
            
            self.log("✅ DynamixelClient创建成功")
            
            # 尝试连接
            try:
                client.connect()
                self.log("✅ ORCA客户端连接成功")
                
                # 立即断开
                client.disconnect()
                self.log("✅ ORCA客户端断开成功")
                
                self.test_results['orca_simulation'] = True
                return True
                
            except Exception as e:
                self.log(f"❌ ORCA客户端连接失败: {e}")
                self.test_results['orca_simulation'] = False
                return False
                
        except Exception as e:
            self.log(f"❌ ORCA连接模拟失败: {e}")
            self.test_results['orca_simulation'] = False
            return False
    
    def analyze_results(self):
        """分析测试结果并给出诊断"""
        self.log("\n📊 诊断结果分析")
        self.log("=" * 50)
        
        for test, result in self.test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            self.log(f"{test}: {status}")
        
        # 根据结果模式判断问题类型
        if not self.test_results.get('basic_port', False):
            self.log("\n🚨 诊断: USB驱动程序问题")
            self.log("建议: 重新安装FTDI驱动程序")
            
        elif not self.test_results.get('dynamixel_ping', False):
            if self.test_results.get('basic_port', False):
                self.log("\n🚨 诊断: 硬件连接或电源问题")
                self.log("建议:")
                self.log("• 检查机械手独立电源是否连接")
                self.log("• 检查U2D2到机械手的连接线")
                self.log("• 检查U2D2的TTL/RS485开关设置")
                
        elif not self.test_results.get('resource_cleanup', False):
            self.log("\n🚨 诊断: 软件资源管理问题")
            self.log("建议:")
            self.log("• 问题主要在软件层面")
            self.log("• 需要改进ORCA脚本的资源清理")
            
        else:
            if all(self.test_results.values()):
                self.log("\n✅ 诊断: 所有测试通过")
                self.log("建议: 硬件和基础软件正常，可能是具体使用方式问题")
            else:
                self.log("\n⚠️ 诊断: 部分测试失败，需要进一步调查")

def main():
    print("🔬 ORCA机械手问题根源诊断")
    print("=" * 50)
    print("基于观察到的现象进行系统性测试...")
    
    diagnostic = ORCADiagnostic()
    
    # 按顺序执行所有测试
    tests = [
        diagnostic.test_1_basic_port_access,
        diagnostic.test_2_port_exclusive_access,
        diagnostic.test_3_dynamixel_basic_ping,
        diagnostic.test_4_resource_cleanup,
        diagnostic.test_5_orca_connection_simulation
    ]
    
    for test in tests:
        test()
        print()  # 空行分隔
        time.sleep(1)  # 短暂延迟确保资源释放
    
    # 分析结果
    diagnostic.analyze_results()
    
    print("\n🎯 根据您的观察补充建议:")
    print("• 现象3(Python脚本后连不上) = 软件资源管理问题")
    print("• 现象4(断电后连不上) = 硬件初始化问题") 
    print("• 现象5&6(重启/等待解决) = 驱动程序状态问题")

if __name__ == "__main__":
    main()
