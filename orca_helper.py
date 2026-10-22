#!/usr/bin/env python3
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
