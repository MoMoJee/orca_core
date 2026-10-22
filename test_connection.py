from orca_core import OrcaHand
import time

def test_connection():
    print("正在测试ORCA机械手连接...")
    
    # 创建手部实例
    hand = OrcaHand('orca_core/models/orcahand_v1_right')
    
    # 尝试连接
    status = hand.connect()
    print(f"连接状态: {status}")
    
    if status[0]:
        print("✅ 连接成功！")
        
        # 尝试启用扭矩
        try:
            print("正在启用扭矩...")
            hand.enable_torque()
            print("✅ 扭矩启用成功！")
            
            # 短暂等待
            time.sleep(1)
            
            # 禁用扭矩
            print("正在禁用扭矩...")
            hand.disable_torque()
            print("✅ 扭矩禁用成功！")
            
        except Exception as e:
            print(f"❌ 扭矩操作失败: {e}")
        
        # 断开连接
        hand.disconnect()
        print("✅ 已断开连接")
        
    else:
        print(f"❌ 连接失败: {status[1]}")

if __name__ == "__main__":
    test_connection()
