#!/usr/bin/env python3
"""
ORCA间歇性连接问题解决方案
专门处理"用过一会儿就连不上"和"重启后连不上"的问题
"""

import time
import subprocess
import sys
import os
from datetime import datetime

class ORCAReconnectionHelper:
    def __init__(self):
        self.port = "COM8"
        self.baudrate = 3000000
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def check_processes_using_com8(self):
        """检查占用COM8的进程"""
        self.log("🔍 检查占用COM8的进程...")
        
        try:
            # 使用handle.exe或tasklist查找占用串口的进程
            cmd = 'tasklist /v | findstr /i "python\\|dynamixel\\|wizard"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.stdout:
                self.log("发现可能相关的进程:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        print(f"  {line}")
                return True
            else:
                self.log("✅ 未发现明显占用COM8的进程")
                return False
                
        except Exception as e:
            self.log(f"⚠️ 进程检查失败: {e}")
            return False
    
    def kill_related_processes(self):
        """终止可能冲突的进程"""
        self.log("🔪 终止可能冲突的进程...")
        
        processes_to_kill = [
            "DynamixelWizard2.exe",
            "python.exe"  # 注意：这会终止其他Python进程
        ]
        
        for process in processes_to_kill:
            try:
                cmd = f'taskkill /f /im "{process}" 2>nul'
                subprocess.run(cmd, shell=True, capture_output=True)
                self.log(f"✅ 已尝试终止: {process}")
            except:
                pass
        
        time.sleep(2)
    
    def reset_usb_device(self):
        """重置USB设备"""
        self.log("🔄 重置U2D2 USB设备...")
        
        try:
            # 方法1: 使用devcon重启设备
            cmd = 'devcon restart "USB\\VID_0403*"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ USB设备重置成功")
                time.sleep(3)  # 等待设备重新枚举
                return True
            else:
                # 方法2: 使用pnputil
                self.log("⚠️ devcon失败，尝试其他方法...")
                return False
                
        except Exception as e:
            self.log(f"⚠️ USB设备重置失败: {e}")
            return False
    
    def create_connection_helper_script(self):
        """创建连接助手脚本"""
        self.log("📝 创建ORCA连接助手脚本...")
        
        helper_content = '''#!/usr/bin/env python3
"""
ORCA连接助手 - 解决间歇性连接问题
使用方法: 在运行任何ORCA脚本之前先运行此助手
"""

import subprocess
import time
import sys

def prepare_orca_connection():
    """准备ORCA连接环境"""
    print("🔧 ORCA连接助手启动...")
    
    # 步骤1: 终止可能冲突的进程
    print("1️⃣ 清理冲突进程...")
    try:
        subprocess.run('taskkill /f /im "DynamixelWizard2.exe" 2>nul', shell=True)
        print("   ✅ Dynamixel Wizard已关闭")
    except:
        pass
    
    # 步骤2: 短暂等待
    print("2️⃣ 等待资源释放...")
    time.sleep(2)
    
    # 步骤3: 测试基础连接
    print("3️⃣ 测试基础连接...")
    try:
        import serial
        ser = serial.Serial("COM8", 9600, timeout=1)
        ser.close()
        print("   ✅ COM8端口可访问")
    except Exception as e:
        print(f"   ❌ COM8端口问题: {e}")
        print("   💡 建议: 重新插拔U2D2 USB线")
        return False
    
    print("✅ 连接环境已准备就绪!")
    print("💡 现在可以运行您的ORCA脚本了")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果提供了参数，准备环境后运行指定脚本
        script_to_run = sys.argv[1]
        if prepare_orca_connection():
            print(f"🚀 运行脚本: {script_to_run}")
            subprocess.run([sys.executable, script_to_run] + sys.argv[2:])
    else:
        # 只准备环境
        prepare_orca_connection()
'''
        
        with open("orca_helper.py", "w", encoding="utf-8") as f:
            f.write(helper_content)
        
        self.log("✅ 连接助手已创建: orca_helper.py")
    
    def create_batch_scripts(self):
        """创建批处理脚本"""
        self.log("📝 创建批处理脚本...")
        
        # Windows批处理脚本
        batch_content = '''@echo off
echo 🔧 ORCA快速重置工具
echo ==================

echo 1. 关闭可能冲突的程序...
taskkill /f /im "DynamixelWizard2.exe" 2>nul
taskkill /f /im "python.exe" 2>nul

echo 2. 等待资源释放...
timeout /t 3 /nobreak >nul

echo 3. 重新插拔提示...
echo 💡 请重新插拔U2D2的USB线
echo 💡 等待3秒后按任意键继续...
pause

echo ✅ 重置完成！现在可以运行ORCA脚本了
'''
        
        with open("orca_reset.bat", "w", encoding="utf-8") as f:
            f.write(batch_content)
        
        self.log("✅ 批处理脚本已创建: orca_reset.bat")

def main():
    print("🔧 ORCA间歇性连接问题解决工具")
    print("=" * 50)
    print("专门解决'用过一会儿连不上'和'重启后连不上'的问题")
    print()
    
    helper = ORCAReconnectionHelper()
    
    # 诊断当前状态
    print("📊 当前状态诊断:")
    helper.check_processes_using_com8()
    print()
    
    # 创建工具
    helper.create_connection_helper_script()
    helper.create_batch_scripts()
    
    print("\n🎯 解决方案已创建!")
    print("=" * 50)
    
    print("\n方案1: 使用连接助手 (推荐)")
    print("• 每次运行ORCA脚本前先运行: python orca_helper.py")
    print("• 或者直接运行: python orca_helper.py your_script.py")
    
    print("\n方案2: 使用快速重置")
    print("• 双击运行: orca_reset.bat")
    print("• 按提示重新插拔USB线")
    
    print("\n方案3: 手动步骤")
    print("• 关闭Dynamixel Wizard")
    print("• 重新插拔U2D2 USB线")
    print("• 等待3秒后运行ORCA脚本")
    
    print("\n💡 根本原因:")
    print("间歇性连接问题通常是由于:")
    print("• 软件资源未完全释放")
    print("• USB驱动状态不稳定") 
    print("• 多个程序竞争同一COM端口")
    
    print("\n🚀 现在试试运行: python orca_helper.py")

if __name__ == "__main__":
    main()
