#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORCA机械手硬件检查清单
"""

def print_checklist():
    print("🔍 ORCA机械手硬件检查清单")
    print("=" * 50)
    
    print("\n🔌 电源检查:")
    print("━" * 20)
    print("□ 机械手有独立的12V电源适配器")
    print("□ 电源适配器已插入电源插座并通电")
    print("□ 电源线已连接到机械手的电源接口")
    print("□ 机械手上的电源指示灯亮起 (通常是绿色/蓝色)")
    
    print("\n🔗 连接检查:")
    print("━" * 20)
    print("□ U2D2通过Micro USB连接到电脑")
    print("□ U2D2上的电源指示灯亮起")
    print("□ 从U2D2到机械手的通信线连接牢固")
    print("□ 通信线使用正确的接口 (3PIN或4PIN JST)")
    
    print("\n⚙️ U2D2设置检查:")
    print("━" * 20)
    print("□ U2D2上的开关设置为TTL模式 (不是RS485)")
    print("□ U2D2在设备管理器中显示为COM8")
    print("□ 没有黄色警告图标")
    
    print("\n🔧 软件检查:")
    print("━" * 20)
    print("□ Dynamixel Wizard 2.0已安装")
    print("□ FTDI驱动程序已正确安装")
    print("□ 没有其他程序占用COM8端口")
    
    print("\n💡 故障排除步骤:")
    print("━" * 25)
    print("1. 确认机械手电源 - 这是最常见的问题")
    print("2. 检查所有连接线是否牢固")
    print("3. 在Dynamixel Wizard中尝试扫描:")
    print("   - 打开Dynamixel Wizard 2.0")
    print("   - 选择COM8端口")
    print("   - 波特率选择57600或1000000")
    print("   - 点击'Scan'扫描电机")
    print("4. 如果仍无法检测到，联系ORCA技术支持")
    
    print("\n📞 技术支持信息:")
    print("━" * 25)
    print("如果以上步骤都无法解决问题，建议:")
    print("1. 拍照记录您的硬件连接")
    print("2. 记录电源指示灯状态")
    print("3. 联系ORCA官方技术支持")

def main():
    print_checklist()
    
    print("\n" + "=" * 50)
    input("请按回车键继续...")

if __name__ == "__main__":
    main()
