"""
测试Micro USB的特殊模式
"""

import time

print("🔍 Micro USB特殊模式测试指南")
print("=" * 40)

print("\n📋 请按以下步骤测试:")

print("\n方法1: 启动序列测试")
print("1. 断开USB和电源")
print("2. 按住控制板上的任何按钮（如果有）")
print("3. 先连接电源，保持按钮按下3秒")
print("4. 释放按钮，然后连接USB")
print("5. 运行Dynamixel Wizard扫描")

print("\n方法2: 不同上电序列")
print("1. 先连接USB（电源关闭）")
print("2. 再开启电源")
print("3. 观察指示灯变化")
print("4. 尝试扫描")

print("\n方法3: 重置序列") 
print("1. 连接USB和电源")
print("2. 快速按压复位按钮3次（如果有）")
print("3. 等待10秒观察指示灯")
print("4. 尝试扫描")

print("\n🔍 观察要点:")
print("• 指示灯颜色和闪烁模式的变化")
print("• 是否有新的设备出现在设备管理器中")
print("• 是否有系统提示音的变化")

print("\n📝 记录结果:")
input("完成测试后按Enter继续...")

print("\n📞 如果仍无效，请联系ORCA技术支持询问:")
print("• 正确的连接方式")
print("• 是否需要特殊的初始化序列")
print("• Micro USB与UART接口的区别")

print("\n💡 很可能需要使用UART接口进行通信！")
