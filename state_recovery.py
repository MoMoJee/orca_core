#!/usr/bin/env python3
"""
ORCA状态恢复工具
专门解决"曾经能用，现在用不了"的问题

既然您成功运行过，说明硬件连接基本正常
问题可能是：状态变化、配置漂移、或临时性故障
"""

import time
import subprocess
import sys
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def restore_working_state():
    """尝试恢复到之前工作的状态"""
    print("🔄 ORCA状态恢复工具")
    print("=" * 50)
    print("既然您曾经成功运行过，我们来恢复到那个状态")
    print()
    
    log("🎯 开始状态恢复流程...")
    
    # 步骤1: 完全重置USB设备
    log("1️⃣ 完全重置USB设备...")
    try:
        # 禁用并重新启用USB设备
        subprocess.run('devcon disable "USB\\VID_0403*"', shell=True, capture_output=True)
        time.sleep(2)
        subprocess.run('devcon enable "USB\\VID_0403*"', shell=True, capture_output=True)
        time.sleep(3)
        log("✅ USB设备重置完成")
    except:
        log("⚠️ USB设备重置需要管理员权限，跳过...")
    
    # 步骤2: 清理所有可能的冲突进程
    log("2️⃣ 清理所有潜在冲突进程...")
    processes_to_kill = [
        "DynamixelWizard2.exe",
        "python.exe"
    ]
    
    for proc in processes_to_kill:
        try:
            subprocess.run(f'taskkill /f /im "{proc}" 2>nul', shell=True)
            log(f"   清理进程: {proc}")
        except:
            pass
    
    time.sleep(3)
    
    # 步骤3: 测试多个波特率恢复连接
    log("3️⃣ 尝试多波特率恢复连接...")
    
    baudrates_to_try = [
        57600,    # 最安全的波特率
        115200,   # 常用波特率
        1000000,  # 高速波特率
        3000000   # 目标波特率
    ]
    
    for baudrate in baudrates_to_try:
        log(f"   🔍 尝试波特率: {baudrate}")
        
        if test_baudrate_connection(baudrate):
            log(f"   ✅ 在波特率 {baudrate} 下连接成功！")
            
            # 如果成功了但不是目标波特率，尝试切换
            if baudrate != 3000000:
                log(f"   🔧 尝试切换到目标波特率 3000000...")
                if switch_baudrate(baudrate, 3000000):
                    log("   ✅ 波特率切换成功！")
                else:
                    log("   ⚠️ 波特率切换失败，但当前波特率可用")
            
            return True
        
        time.sleep(1)
    
    log("❌ 所有波特率尝试都失败")
    return False

def test_baudrate_connection(baudrate):
    """测试指定波特率的连接"""
    try:
        from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
        
        port_handler = PortHandler("COM8")
        packet_handler = PacketHandler(2.0)
        
        if not port_handler.openPort():
            return False
        
        if not port_handler.setBaudRate(baudrate):
            port_handler.closePort()
            return False
        
        # 短超时快速测试
        port_handler.setPacketTimeout(50)  # 50ms超时
        
        # 尝试ping电机ID 1
        model, result, error = packet_handler.ping(port_handler, 1)
        
        port_handler.closePort()
        
        return result == COMM_SUCCESS
        
    except Exception:
        return False

def switch_baudrate(current_baud, target_baud):
    """切换电机波特率"""
    try:
        from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
        
        port_handler = PortHandler("COM8")
        packet_handler = PacketHandler(2.0)
        
        # 用当前波特率连接
        port_handler.openPort()
        port_handler.setBaudRate(current_baud)
        
        # 写入新的波特率设置（地址8是波特率寄存器）
        ADDR_BAUDRATE = 8
        baudrate_value = get_baudrate_value(target_baud)
        
        if baudrate_value is not None:
            result, error = packet_handler.write1ByteTxRx(port_handler, 1, ADDR_BAUDRATE, baudrate_value)
            
            if result == COMM_SUCCESS:
                port_handler.closePort()
                time.sleep(1)
                
                # 用新波特率测试连接
                return test_baudrate_connection(target_baud)
        
        port_handler.closePort()
        return False
        
    except Exception:
        return False

def get_baudrate_value(baudrate):
    """获取波特率对应的寄存器值"""
    baudrate_map = {
        9600: 0,
        57600: 1,
        115200: 2,
        1000000: 3,
        2000000: 4,
        3000000: 5,
        4000000: 6
    }
    return baudrate_map.get(baudrate)

def suggest_recovery_steps():
    """建议恢复步骤"""
    print("\n💡 其他恢复尝试")
    print("=" * 50)
    
    print("如果自动恢复失败，请手动尝试：")
    print()
    print("🔧 方法1: 物理重置")
    print("• 关闭所有程序")
    print("• 拔掉机械手电源适配器 30秒")
    print("• 拔掉U2D2 USB线 30秒") 
    print("• 重新插入电源适配器")
    print("• 等待5秒后插入USB线")
    print("• 再次尝试连接")
    print()
    
    print("🔧 方法2: Wizard重置")
    print("• 打开Dynamixel Wizard")
    print("• 尝试较低波特率扫描（57600）")
    print("• 如果找到电机，重新设置为3000000波特率")
    print("• 保存设置后关闭Wizard")
    print("• 运行Python脚本")
    print()
    
    print("🔧 方法3: 配置重置")
    print("• 检查config.yaml是否被意外修改")
    print("• 对比之前成功时的配置")
    print("• 恢复到工作时的配置")
    print()
    
    print("🔍 调试信息收集")
    print("如果仍然无法恢复，请告诉我：")
    print("• 最后一次成功运行是什么时候？")
    print("• 成功运行的是哪个脚本？")
    print("• 之后做了什么操作？（重启、断电等）")
    print("• 在Dynamixel Wizard中能否扫描到电机？")

def create_recovery_script():
    """创建一键恢复脚本"""
    recovery_content = '''@echo off
echo 🔄 ORCA一键恢复脚本
echo ==================

echo 步骤1: 关闭冲突程序...
taskkill /f /im "DynamixelWizard2.exe" 2>nul
taskkill /f /im "python.exe" 2>nul

echo 步骤2: 等待资源释放...
timeout /t 5 /nobreak >nul

echo 步骤3: 提示物理重置...
echo.
echo 💡 请按以下步骤操作：
echo 1. 拔掉机械手电源适配器
echo 2. 拔掉U2D2 USB线
echo 3. 等待30秒
echo 4. 重新插入电源适配器
echo 5. 等待5秒后插入USB线
echo.
pause

echo 步骤4: 测试连接...
python -c "
import serial
try:
    ser = serial.Serial('COM8', 9600, timeout=1)
    ser.close()
    print('✅ COM8连接正常')
except Exception as e:
    print(f'❌ COM8连接失败: {e}')
"

echo.
echo ✅ 恢复流程完成！
echo 💡 现在尝试运行您的ORCA脚本
pause
'''
    
    with open("orca_recovery.bat", "w", encoding="utf-8") as f:
        f.write(recovery_content)
    
    log("✅ 一键恢复脚本已创建: orca_recovery.bat")

def main():
    print("🔄 ORCA状态恢复工具")
    print("=" * 50)
    print("专门解决'曾经能用，现在用不了'的问题")
    print()
    
    # 尝试自动恢复
    success = restore_working_state()
    
    if success:
        print("\n🎉 状态恢复成功！")
        print("现在试试运行您之前成功的脚本")
    else:
        print("\n⚠️ 自动恢复未成功")
        suggest_recovery_steps()
        create_recovery_script()
    
    print("\n📝 记录建议")
    print("为了避免今后出现同样问题，建议：")
    print("• 每次使用后正确关闭ORCA脚本")
    print("• 避免在脚本运行时强制关闭")
    print("• 定期保存工作配置的备份")

if __name__ == "__main__":
    main()
