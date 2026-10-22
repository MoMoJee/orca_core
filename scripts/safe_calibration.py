#!/usr/bin/env python3
"""
安全校准脚本 - 降低电流避免跳齿
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from orca_core.core import OrcaHand
import time

def safe_calibrate():
    """使用较低电流进行安全校准"""
    hand = OrcaHand()
    
    # 连接手部
    print("🔌 连接ORCA手部...")
    if not hand.connect():
        print("❌ 连接失败！")
        return False
    
    print("✅ 连接成功！")
    
    # 获取原始校准电流
    original_current = hand.calib_current
    print(f"📊 原始校准电流: {original_current} mA")
    
    # 使用更安全的低电流
    safe_current = 150  # 降低到150mA，减少57%的力矩
    print(f"🛡️ 使用安全电流: {safe_current} mA")
    
    # 临时修改校准电流
    hand.calib_current = safe_current
    
    print("\n🔧 开始安全校准...")
    print("⚠️  如果发现任何异常声音或阻力，请立即按 Ctrl+C 停止！")
    print("⚠️  校准过程中请观察是否有跳齿或异响")
    
    try:
        # 执行完整校准，但使用低电流
        result = hand.calibrate()
        
        if result:
            print("✅ 校准成功完成！")
            print("📝 校准数据已保存到 calibration.yaml")
        else:
            print("❌ 校准失败")
            
    except KeyboardInterrupt:
        print("\n🛑 用户中断校准")
    except Exception as e:
        print(f"\n❌ 校准过程中出错: {e}")
    finally:
        # 恢复原始配置
        hand.calib_current = original_current
        hand.disconnect()
        print("\n🔌 断开连接")

def manual_position_test():
    """手动位置测试 - 无校准方式"""
    hand = OrcaHand()
    
    if not hand.connect():
        print("❌ 连接失败！")
        return
    
    print("✅ 连接成功！")
    print("\n🧪 手动位置测试模式")
    print("这种模式不需要校准，直接设置目标角度")
    
    try:
        # 设置到中性位置
        print("📐 设置到中性位置...")
        neutral_angles = hand.neutral_position
        
        # 使用set_joint_pos方法
        print("设置关节到中性位置...")
        hand.set_joint_pos(neutral_angles)
        time.sleep(2)
        
        print("\n✅ 已设置到中性位置")
        print("🎯 现在您可以手动测试各个关节的运动")
        
        # 简单的关节测试
        test_joints = {
            'thumb_mcp': [-10, 10],
            'index_mcp': [-10, 10], 
            'middle_mcp': [-10, 10]
        }
        
        for joint, range_val in test_joints.items():
            print(f"\n🔄 测试关节: {joint}")
            
            # 获取当前中性位置
            neutral_pos = neutral_angles.get(joint, 0)
            
            print("向正方向移动...")
            test_pos = {joint: neutral_pos + range_val[1]}
            hand.set_joint_pos(test_pos)
            time.sleep(2)
            
            print("向负方向移动...")
            test_pos = {joint: neutral_pos + range_val[0]}
            hand.set_joint_pos(test_pos)
            time.sleep(2)
            
            print("返回中性位置...")
            test_pos = {joint: neutral_pos}
            hand.set_joint_pos(test_pos)
            time.sleep(2)
            
            response = input("关节运动是否正常？ (y/n): ")
            if response.lower() != 'y':
                print("⚠️ 检测到异常，停止测试")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 用户中断测试")
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
    finally:
        hand.disconnect()
        print("\n🔌 断开连接")

if __name__ == "__main__":
    print("🤖 ORCA手部安全校准工具")
    print("="*50)
    print("选择模式:")
    print("1. 安全校准 (降低电流)")
    print("2. 手动位置测试 (无校准)")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ")
    
    if choice == "1":
        safe_calibrate()
    elif choice == "2":
        manual_position_test()
    elif choice == "3":
        print("👋 再见！")
    else:
        print("❌ 无效选择")
