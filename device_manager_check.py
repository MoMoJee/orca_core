#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备管理器详细检查脚本
检查USB设备和驱动程序状态
"""

import subprocess
import sys

def run_cmd(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def check_device_manager():
    """检查设备管理器中的设备状态"""
    print("🔍 检查设备管理器中的USB设备...")
    
    # 查看所有USB设备
    cmd = 'wmic path Win32_USBControllerDevice get Dependent | findstr "USB"'
    stdout, stderr, code = run_cmd(cmd)
    if stdout:
        print("📋 USB设备列表:")
        print(stdout)
    
    # 查看问题设备
    print("\n🚨 检查问题设备...")
    cmd = 'wmic path Win32_PnPEntity where "ConfigManagerErrorCode != 0" get Name, ConfigManagerErrorCode'
    stdout, stderr, code = run_cmd(cmd)
    if stdout:
        print("❌ 有问题的设备:")
        print(stdout)
    else:
        print("✅ 没有发现问题设备")
    
    # 查看USB串口设备
    print("\n📡 检查USB串口设备...")
    cmd = 'wmic path Win32_SerialPort get Name, DeviceID, PNPDeviceID'
    stdout, stderr, code = run_cmd(cmd)
    if stdout:
        print("📋 串口设备详情:")
        print(stdout)
    
    # 检查USB根集线器
    print("\n🔌 检查USB控制器...")
    cmd = 'wmic path Win32_USBController get Name, Status'
    stdout, stderr, code = run_cmd(cmd)
    if stdout:
        print("📋 USB控制器状态:")
        print(stdout)

def check_ftdi_devices():
    """检查FTDI设备 (U2D2使用FTDI芯片)"""
    print("\n🔧 检查FTDI设备...")
    
    # 查找FTDI设备
    cmd = 'wmic path Win32_PnPEntity where "DeviceID like \'%FTDI%\'" get Name, DeviceID, Status'
    stdout, stderr, code = run_cmd(cmd)
    if stdout and "FTDI" in stdout:
        print("📋 FTDI设备:")
        print(stdout)
    else:
        print("❌ 未找到FTDI设备")
        
    # 查找USB Serial设备
    cmd = 'wmic path Win32_PnPEntity where "Name like \'%USB Serial%\'" get Name, DeviceID, Status'
    stdout, stderr, code = run_cmd(cmd)
    if stdout and len(stdout.strip()) > 0:
        print("📋 USB Serial设备:")
        print(stdout)

def main():
    print("🔬 设备管理器详细检查")
    print("=" * 50)
    
    check_device_manager()
    check_ftdi_devices()
    
    print("\n💡 下一步建议:")
    print("=" * 30)
    print("1. 打开设备管理器 (devmgmt.msc)")
    print("2. 查看是否有带黄色警告图标的设备")
    print("3. 在'端口(COM和LPT)'分类下查看COM8")
    print("4. 如果COM8有问题，右键选择'更新驱动程序'")
    print("5. 或者尝试卸载设备并重新插拔USB")

if __name__ == "__main__":
    main()
