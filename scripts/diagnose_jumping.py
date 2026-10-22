#!/usr/bin/env python3
"""
ORCA手部跳齿问题分析和解决方案
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from orca_core.core import OrcaHand
import time

def check_current_motor_status():
    """检查电机当前状态和电流"""
    hand = OrcaHand()
    
    if not hand.connect():
        print("❌ 连接失败！")
        return
    
    print("✅ 连接成功！")
    print("\n📊 检查电机状态...")
    
    try:
        # 获取所有电机的当前位置和电流
        positions = hand.get_motor_pos()
        currents = hand.get_motor_current()
        
        print("\n📍 当前电机状态:")
        print("电机ID | 位置(度) | 电流(mA)")
        print("-" * 35)
        
        for motor_id in hand.motor_ids:
            pos = positions.get(motor_id, "未知")
            current = currents.get(motor_id, "未知")
            joint = hand.motor_to_joint_dict.get(motor_id, "未知关节")
            print(f"{motor_id:6d} | {pos:8.1f} | {current:8.1f} | {joint}")
        
        # 检查是否有电机电流异常高
        high_current_motors = []
        for motor_id, current in currents.items():
            if current > 200:  # 超过200mA认为是高电流
                high_current_motors.append((motor_id, current))
        
        if high_current_motors:
            print(f"\n⚠️  检测到高电流电机:")
            for motor_id, current in high_current_motors:
                joint = hand.motor_to_joint_dict.get(motor_id, "未知")
                print(f"  电机 {motor_id} ({joint}): {current:.1f} mA")
            print("  可能原因: 拉线过紧、机械阻力、或传动卡滞")
        else:
            print("\n✅ 所有电机电流正常")
            
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")
    finally:
        hand.disconnect()

def gentle_movement_test():
    """温和的运动测试 - 避免跳齿"""
    hand = OrcaHand()
    
    if not hand.connect():
        print("❌ 连接失败！")
        return
    
    print("✅ 连接成功！")
    print("\n🐢 温和运动测试 (避免跳齿)")
    
    try:
        # 先设置低最大电流
        print("🔧 设置低最大电流 (100mA) 以避免跳齿...")
        hand.set_max_current(100)  # 设置很低的电流限制
        time.sleep(1)
        
        # 获取当前位置
        current_pos = hand.get_joint_pos()
        print(f"📍 当前关节位置: {current_pos}")
        
        # 选择一个关节进行小幅测试
        test_joint = 'thumb_mcp'
        if test_joint in current_pos:
            current_angle = current_pos[test_joint]
            print(f"\n🔄 测试关节: {test_joint}")
            print(f"   当前角度: {current_angle:.1f}°")
            
            # 小幅度移动 (+5度)
            target_angle = current_angle + 5
            print(f"   目标角度: {target_angle:.1f}° (+5°)")
            
            test_pos = {test_joint: target_angle}
            hand.set_joint_pos(test_pos, num_steps=10, step_size=0.5)  # 慢速移动
            time.sleep(3)
            
            # 检查是否到达目标
            new_pos = hand.get_joint_pos()
            actual_angle = new_pos.get(test_joint, current_angle)
            print(f"   实际角度: {actual_angle:.1f}°")
            
            if abs(actual_angle - target_angle) < 2:
                print("✅ 移动成功，无异常")
            else:
                print("⚠️  移动不到位，可能有阻力")
            
            # 返回原位置
            print("🔄 返回原位置...")
            return_pos = {test_joint: current_angle}
            hand.set_joint_pos(return_pos, num_steps=10, step_size=0.5)
            time.sleep(3)
            
        print("\n📋 测试结论:")
        print("  如果移动顺畅 ✅ - 硬件正常，可以尝试校准")
        print("  如果有卡滞 ⚠️  - 检查拉线张力或机械装配")
        print("  如果有异响 🚨 - 立即停止，检查齿轮系统")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    finally:
        # 恢复正常电流
        hand.set_max_current(300)  # 恢复默认值
        hand.disconnect()
        print("\n🔌 断开连接")

def modify_calibration_current():
    """修改校准配置文件的电流设置"""
    config_path = "d:\\PROJECTS\\orca_core\\orca_core\\models\\orcahand_v1_right\\config.yaml"
    
    print("🛠️  修改校准电流设置")
    print("当前校准电流设置:")
    
    # 读取当前配置
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找当前设置
    if 'calib_current: 350' in content:
        print("  calib_current: 350 mA (默认值)")
        new_current = input("输入新的校准电流 (建议 150-200): ")
        
        try:
            new_current_int = int(new_current)
            if 50 <= new_current_int <= 300:
                # 创建备份
                backup_path = config_path + ".backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 配置文件已备份到: {backup_path}")
                
                # 修改配置
                new_content = content.replace('calib_current: 350', f'calib_current: {new_current_int}')
                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ 校准电流已修改为: {new_current_int} mA")
                print("⚠️  请重新加载 OrcaHand 对象以生效")
            else:
                print("❌ 电流值应在 50-300 mA 范围内")
        except ValueError:
            print("❌ 请输入有效的数字")
    else:
        print("⚠️  未找到 calib_current 设置或已修改")

if __name__ == "__main__":
    print("🔧 ORCA手部跳齿问题诊断工具")
    print("=" * 50)
    print("选择操作:")
    print("1. 检查电机状态和电流")
    print("2. 温和运动测试")  
    print("3. 修改校准电流设置")
    print("4. 退出")
    
    choice = input("\n请选择 (1-4): ")
    
    if choice == "1":
        check_current_motor_status()
    elif choice == "2":
        gentle_movement_test()
    elif choice == "3":
        modify_calibration_current()
    elif choice == "4":
        print("👋 再见！")
    else:
        print("❌ 无效选择")
