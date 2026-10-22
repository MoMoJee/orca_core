#!/usr/bin/env python3
"""
ORCA机械手端口清理和资源释放工具
解决端口锁定问题
"""

import serial
import time
import psutil
import os

def find_port_processes():
    """查找占用COM8端口的进程"""
    print("🔍 查找占用COM8端口的进程...")
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # 检查进程是否可能在使用串口
            cmdline = proc.info['cmdline']
            if cmdline and any('COM8' in str(arg) for arg in cmdline):
                print(f"找到进程: PID={proc.info['pid']}, 名称={proc.info['name']}")
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print("未找到明显占用COM8的进程")
    return None

def force_close_port():
    """强制关闭COM8端口"""
    print("🔧 尝试强制关闭COM8端口...")
    
    try:
        # 尝试打开并立即关闭端口来清理状态
        ser = serial.Serial('COM8', timeout=0.1)
        ser.close()
        print("✅ 端口状态重置成功")
        return True
    except Exception as e:
        print(f"❌ 端口重置失败: {e}")
        return False

def release_dynamixel_resources():
    """释放Dynamixel相关资源"""
    print("🔄 释放Dynamixel资源...")
    
    try:
        # 导入dynamixel相关模块并尝试清理
        from dynamixel_sdk import PortHandler, PacketHandler
        
        # 创建处理器实例
        port_handler = PortHandler('COM8')
        
        # 如果端口已打开，强制关闭
        if port_handler.is_open:
            port_handler.closePort()
            print("✅ Dynamixel端口已关闭")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Dynamixel资源清理警告: {e}")
        return False

def safe_port_reset():
    """安全的端口重置流程"""
    print("🔄 执行安全端口重置...")
    
    steps = [
        ("查找占用进程", find_port_processes),
        ("释放Dynamixel资源", release_dynamixel_resources), 
        ("强制关闭端口", force_close_port)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        try:
            result = step_func()
            if result:
                print(f"✅ {step_name}完成")
            else:
                print(f"⚠️ {step_name}部分成功")
        except Exception as e:
            print(f"❌ {step_name}失败: {e}")
    
    print("\n⏰ 等待端口稳定...")
    time.sleep(2)

def verify_port_available():
    """验证端口是否可用"""
    print("\n🔍 验证端口可用性...")
    
    try:
        ser = serial.Serial('COM8', 9600, timeout=1)
        ser.close()
        print("✅ COM8端口可用")
        return True
    except Exception as e:
        print(f"❌ COM8端口仍不可用: {e}")
        return False

if __name__ == "__main__":
    print("🛠️ ORCA机械手端口清理工具")
    print("=" * 40)
    
    # 执行清理流程
    safe_port_reset()
    
    # 验证结果
    if verify_port_available():
        print("\n🎉 端口清理成功！")
        print("现在可以重新在Dynamixel Wizard中扫描电机")
    else:
        print("\n⚠️ 端口可能仍被占用")
        print("建议:")
        print("1. 重启电脑（最可靠的方法）")
        print("2. 在设备管理器中禁用/启用COM8")
        print("3. 拔插U2D2设备")
    
    print("\n📋 防止问题再次发生的建议:")
    print("• 确保ORCA脚本能正常连接电机再运行")
    print("• 避免使用Ctrl+C强制退出")
    print("• 如需退出，使用脚本的正常退出机制")
