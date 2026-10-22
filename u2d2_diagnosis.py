"""
U2D2诊断和配置指南
"""

print("🔧 U2D2 + ORCA机械手诊断")
print("=" * 40)

print("\n📋 请确认以下U2D2设置:")
print("1. 🔌 连接方式:")
print("   PC → USB → U2D2 → PHB → ORCA机械手")
print("   ✓ 您已确认使用U2D2")

print("\n2. 🎛️ U2D2开关设置:")
print("   查看U2D2控制板上的开关:")
print("   • TTL/RS485开关应设置为 TTL")
print("   • 电压开关应设置为正确的电压(通常5V)")
print("   • 确认没有其他拨码开关设置错误")

print("\n3. 💡 指示灯状态:")
print("   U2D2上的LED指示灯:")
print("   • 电源LED应该亮起")
print("   • 通信LED在发送数据时应该闪烁")
print("   • 错误LED应该不亮或偶尔闪烁")

print("\n4. 🔍 Windows设备管理器检查:")
print("   • U2D2应该显示为 'USB Serial Port (COMx)'")
print("   • 不应该有黄色警告标志")
print("   • 驱动程序应该是最新的")

print("\n5. ⚡ 电源检查:")
print("   • PHB(Power Hub Board)是否有独立供电?")
print("   • 12V电源适配器是否连接?")
print("   • PHB上的电源指示灯是否亮起?")

print("\n🔧 故障排除步骤:")
print("1. 重新安装U2D2驱动程序")
print("2. 检查所有开关设置")
print("3. 确认电源供应")
print("4. 尝试不同的USB端口")
print("5. 检查连接线缆")

print("\n🎯 下一步测试:")
print("如果以上都正常，我们需要:")
print("• 使用Dynamixel Wizard直接测试U2D2")
print("• 检查电机是否已正确设置ID")
print("• 验证电机波特率设置")

input("\n按Enter继续进行具体的U2D2测试...")
