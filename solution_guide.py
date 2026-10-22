#!/usr/bin/env python3
"""
🎯 ORCA机械手间歇性连接问题 - 完整解决方案

您遇到的问题：
✅ 硬件正常，曾经成功运行过脚本
❌ 过了一会儿就连不上
❌ 重启后可能连不上

根本原因：
这是典型的软件资源管理问题，主要由以下原因造成：
1. Dynamixel Wizard和Python脚本资源冲突
2. USB驱动状态在使用后变得不稳定
3. 串口资源没有完全释放

解决方案（按推荐顺序）：
"""

import subprocess
import sys

def show_solutions():
    print(__doc__)
    
    print("方案1: 🚀 使用ORCA连接助手（最推荐）")
    print("=" * 50)
    print("命令: python orca_helper.py")
    print("说明: 自动清理冲突进程，测试连接，准备环境")
    print("优点: 自动化，安全，快速")
    print()
    
    print("方案2: 🔧 使用快速重置脚本")
    print("=" * 50)  
    print("命令: 双击 orca_reset.bat")
    print("说明: 批处理脚本，会提示重新插拔USB")
    print("优点: 简单直观，Windows原生")
    print()
    
    print("方案3: 🖐️ 手动操作步骤")
    print("=" * 50)
    print("1. 关闭所有Dynamixel Wizard窗口")
    print("2. 重新插拔U2D2的USB线")
    print("3. 等待3秒让驱动重新加载")
    print("4. 运行您的ORCA脚本")
    print()
    
    print("🎯 使用建议:")
    print("=" * 50)
    print("• 每次使用ORCA前运行一次连接助手")
    print("• 如果脚本运行一段时间后出问题，重新运行助手")
    print("• 避免同时开启Dynamixel Wizard和Python脚本")
    print("• 脚本结束后确保正确调用 client.disconnect()")
    print()
    
    print("🔍 故障排除:")
    print("=" * 50)
    print("如果助手显示'COM8端口问题':")
    print("• 检查U2D2 USB线是否松动")
    print("• 在设备管理器中查看COM8是否存在")
    print("• 尝试重新插拔USB线")
    print("• 重启计算机（最后选择）")
    print()
    
    print("📝 示例用法:")
    print("=" * 50)
    print("# 方法1: 先准备环境，再运行脚本")
    print("python orca_helper.py")
    print("python scripts/main_demo.py")
    print()
    print("# 方法2: 直接运行（助手会自动准备环境）")
    print("python orca_helper.py scripts/main_demo.py")
    print()
    
    # 检查当前可用的脚本
    print("📂 可用的ORCA脚本:")
    print("=" * 50)
    try:
        import os
        scripts_dir = "scripts"
        if os.path.exists(scripts_dir):
            scripts = [f for f in os.listdir(scripts_dir) if f.endswith('.py')]
            for script in sorted(scripts):
                print(f"• {script}")
        else:
            print("未找到scripts目录")
    except:
        print("无法列出脚本")
    
    print()
    print("🎉 现在试试运行:")
    print("python orca_helper.py scripts/main_demo.py")

def quick_test():
    """快速测试连接"""
    print("\n🧪 快速连接测试")
    print("=" * 30)
    
    try:
        # 运行连接助手
        result = subprocess.run([sys.executable, "orca_helper.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 连接助手运行成功")
            print("💡 您的ORCA现在应该可以正常连接了")
        else:
            print("❌ 连接助手遇到问题")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    show_solutions()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        quick_test()
