from orca_core.hardware.mock_dynamixel_client import MockDynamixelClient
from orca_core import OrcaHand
import tempfile
import os
import shutil

def test_with_mock():
    """使用模拟客户端测试软件功能"""
    print("正在使用模拟模式测试软件...")
    
    # 创建临时配置目录
    temp_dir = tempfile.mkdtemp()
    model_dir = os.path.join(temp_dir, "test_model")
    os.makedirs(model_dir)
    
    # 复制配置文件并修改为模拟模式
    original_config = "orca_core/models/orcahand_v1_right/config.yaml"
    original_calib = "orca_core/models/orcahand_v1_right/calibration.yaml"
    
    test_config = os.path.join(model_dir, "config.yaml")
    test_calib = os.path.join(model_dir, "calibration.yaml")
    
    shutil.copy(original_config, test_config)
    shutil.copy(original_calib, test_calib)
    
    try:
        # 创建ORCA手部实例
        hand = OrcaHand(model_dir)
        
        # 使用模拟客户端替换真实客户端
        hand._dxl_client = MockDynamixelClient(hand.motor_ids, hand.port, hand.baudrate)
        
        print("✅ 模拟客户端创建成功")
        
        # 测试连接
        status = hand.connect()
        print(f"连接状态: {status}")
        
        if status[0]:
            print("✅ 模拟连接成功！")
            
            # 测试扭矩操作
            hand.enable_torque()
            print("✅ 模拟扭矩启用成功")
            
            # 测试关节控制
            joint_dict = {"index_mcp": 45, "middle_pip": 30}
            hand.set_joint_pos(joint_dict, num_steps=5, step_size=0.1)
            print("✅ 模拟关节控制成功")
            
            hand.disable_torque()
            print("✅ 模拟扭矩禁用成功")
            
            hand.disconnect()
            print("✅ 模拟断开连接成功")
            
            print("\n🎉 软件功能测试通过！问题出在硬件连接上。")
            
        else:
            print(f"❌ 即使在模拟模式下也连接失败: {status[1]}")
            
    except Exception as e:
        print(f"❌ 模拟测试失败: {e}")
        
    finally:
        # 清理临时文件
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    test_with_mock()
