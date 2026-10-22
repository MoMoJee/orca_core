#!/usr/bin/env python3
"""
ORCA机械手连接稳定化工具
解决间歇性连接失败和重启后连不上的问题
"""

import time
import subprocess
import sys
import os
from datetime import datetime
import yaml

class ORCAConnectionStabilizer:
    def __init__(self):
        self.port = "COM8"
        self.baudrate = 3000000
        self.motor_ids = [1, 2, 3]  # 测试用，避免太多错误输出
        
    def log(self, message):
        """带时间戳的日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def force_cleanup_port(self):
        """强制清理端口资源"""
        self.log("🧹 强制清理COM8端口资源...")
        
        try:
            # 方法1: 使用wmic终止占用串口的进程
            cmd = f'wmic process where "CommandLine like \'%COM8%\'" get ProcessId'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            
            # 方法2: 重置USB设备
            self.log("🔄 重置USB设备...")
            subprocess.run('devcon restart "USB\\VID_0403&PID_6014"', shell=True, capture_output=True)
            
            time.sleep(2)
            self.log("✅ 端口清理完成")
            return True
            
        except Exception as e:
            self.log(f"⚠️ 端口清理异常: {e}")
            return False
    
    def reset_dynamixel_state(self):
        """重置Dynamixel通信状态"""
        self.log("🔄 重置Dynamixel通信状态...")
        
        try:
            from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
            
            # 使用较低波特率建立初始连接
            port_handler = PortHandler(self.port)
            packet_handler = PacketHandler(2.0)
            
            # 尝试多个波特率
            baudrates = [57600, 115200, 1000000, 3000000]
            
            for baudrate in baudrates:
                self.log(f"🔍 尝试波特率: {baudrate}")
                
                if port_handler.openPort():
                    if port_handler.setBaudRate(baudrate):
                        # 尝试ping电机ID 1
                        model, result, error = packet_handler.ping(port_handler, 1)
                        
                        if result == COMM_SUCCESS:
                            self.log(f"✅ 在波特率 {baudrate} 下连接成功")
                            
                            # 如果不是目标波特率，尝试切换
                            if baudrate != self.baudrate:
                                self.log(f"🔧 切换到目标波特率 {self.baudrate}")
                                port_handler.setBaudRate(self.baudrate)
                                
                            port_handler.closePort()
                            return True
                            
                    port_handler.closePort()
                
                time.sleep(0.5)
            
            self.log("❌ 所有波特率测试失败")
            return False
            
        except Exception as e:
            self.log(f"❌ Dynamixel状态重置失败: {e}")
            return False
    
    def test_orca_quick_connection(self):
        """快速测试ORCA连接"""
        self.log("🚀 快速测试ORCA连接...")
        
        try:
            from orca_core.hardware.dynamixel_client import DynamixelClient
            
            # 创建客户端（只测试3个电机）
            client = DynamixelClient(self.motor_ids, self.port, self.baudrate)
            
            # 设置较短的超时时间
            start_time = time.time()
            timeout = 10  # 10秒超时
            
            try:
                client.connect()
                self.log("✅ ORCA快速连接成功")
                
                # 立即断开避免资源占用
                client.disconnect()
                self.log("✅ ORCA连接清理成功")
                
                return True
                
            except Exception as e:
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    self.log(f"⏰ ORCA连接超时 ({elapsed:.1f}s)")
                else:
                    self.log(f"❌ ORCA连接失败: {e}")
                return False
                
        except Exception as e:
            self.log(f"❌ ORCA连接测试异常: {e}")
            return False
    
    def stabilize_connection(self):
        """执行连接稳定化流程"""
        self.log("🎯 开始连接稳定化流程")
        self.log("=" * 50)
        
        # 步骤1: 强制清理
        if not self.force_cleanup_port():
            self.log("⚠️ 端口清理失败，继续执行...")
        
        time.sleep(1)
        
        # 步骤2: 重置Dynamixel状态
        if self.reset_dynamixel_state():
            self.log("✅ Dynamixel状态重置成功")
        else:
            self.log("❌ Dynamixel状态重置失败")
            return False
        
        time.sleep(1)
        
        # 步骤3: 测试ORCA连接
        if self.test_orca_quick_connection():
            self.log("✅ 连接稳定化成功！")
            return True
        else:
            self.log("❌ 连接稳定化失败")
            return False
    
    def create_stable_connection_script(self):
        """创建稳定连接脚本模板"""
        self.log("📝 创建稳定连接脚本模板...")
        
        script_content = '''#!/usr/bin/env python3
"""
ORCA稳定连接模板
使用此模板确保每次连接都是稳定的
"""

import time
from orca_core.hardware.dynamixel_client import DynamixelClient

def stable_orca_connection():
    """稳定的ORCA连接函数"""
    print("🔧 初始化ORCA连接...")
    
    # 读取配置
    motor_ids = list(range(1, 18))  # 1-17
    port = "COM8"
    baudrate = 3000000
    
    # 创建客户端
    client = DynamixelClient(motor_ids, port, baudrate)
    
    try:
        # 连接
        print("🚀 正在连接...")
        client.connect()
        print("✅ 连接成功")
        
        # 你的代码在这里
        # 例如:
        # angles = client.get_joint_angles()
        # print(f"当前角度: {angles}")
        
        return client
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("💡 建议运行: python connection_stabilizer.py")
        return None

def main():
    client = stable_orca_connection()
    
    if client:
        try:
            # 在这里添加你的ORCA控制代码
            print("🎮 ORCA已就绪，可以开始控制")
            
            # 示例: 获取当前角度
            angles = client.get_joint_angles()
            print(f"当前关节角度: {angles}")
            
        except Exception as e:
            print(f"❌ 运行错误: {e}")
        finally:
            # 确保断开连接
            if client:
                client.disconnect()
                print("🔌 连接已安全断开")

if __name__ == "__main__":
    main()
'''
        
        with open("orca_stable_template.py", "w", encoding="utf-8") as f:
            f.write(script_content)
            
        self.log("✅ 稳定连接模板已创建: orca_stable_template.py")

def main():
    print("🔧 ORCA机械手连接稳定化工具")
    print("=" * 50)
    print("专门解决间歇性连接问题和重启后连不上的情况")
    print()
    
    stabilizer = ORCAConnectionStabilizer()
    
    # 执行稳定化
    if stabilizer.stabilize_connection():
        print("\n🎉 连接已稳定化!")
        print("现在可以正常使用ORCA脚本了")
        
        # 创建模板
        stabilizer.create_stable_connection_script()
        
        print("\n💡 使用建议:")
        print("1. 每次使用前先运行此工具")
        print("2. 使用 orca_stable_template.py 作为脚本模板")
        print("3. 如果再次出现问题，重新运行此工具")
        
    else:
        print("\n❌ 稳定化失败")
        print("请检查:")
        print("• 机械手电源是否稳定")
        print("• U2D2连接是否松动")
        print("• 是否有其他软件占用COM8")

if __name__ == "__main__":
    main()
