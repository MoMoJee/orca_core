#!/usr/bin/env python3
"""
ORCA手部跳齿问题解决方案
基于对校准重要性的分析和安全替代方案
"""

# 校准的重要作用分析
CALIBRATION_IMPORTANCE = """
🎯 校准的核心作用:

1. 建立电机位置与关节角度的映射关系
   - 确定每个关节的零点位置
   - 计算电机位置到关节角度的转换比例
   - 为精确控制提供基准

2. 检测和记录机械限位
   - 找到每个关节的最大/最小角度
   - 防止关节超出安全范围
   - 保护机械结构不受损

3. 张力校准和优化
   - 通过电流反馈检测拉线张力
   - 确保拉线在合适的预紧状态
   - 消除拉线松弛或过紧的问题

4. 生成校准数据文件
   - motor_limits: 每个电机的位置极限
   - joint_to_motor_ratios: 关节角度到电机位置的比例系数
   - 这些数据对精确控制至关重要
"""

SKIP_CALIBRATION_RISKS = """
❌ 跳过校准的风险:

1. 控制精度问题
   - 关节角度不准确
   - 无法实现精确抓取
   - 重复性差

2. 安全隐患
   - 可能超出机械限位
   - 关节可能过度伸展
   - 增加机械损坏风险

3. 功能受限
   - 无法使用高级控制功能
   - 预设手势可能不可用
   - 自动化程序可能失效
"""

SAFER_ALTERNATIVES = """
🛡️ 安全的替代方案:

方案1: 降低校准电流
- 将 calib_current 从 350mA 降至 150-200mA
- 减少57%的力矩输出
- 降低跳齿风险

方案2: 手动校准
- 手动记录每个关节的极限位置
- 逐步测试安全的运动范围
- 避免强制性机械接触

方案3: 渐进式校准
- 分批校准关节（拇指->食指->中指...）
- 每个关节校准后检查机械状态
- 发现异常立即停止

方案4: 检查和调整拉线张力
- 确保拉线张力适中
- 检查传动机构的齿轮啮合
- 润滑必要的机械部件
"""

def print_analysis():
    """打印详细的校准分析"""
    print("🤖 ORCA手部校准重要性分析")
    print("=" * 60)
    
    print(CALIBRATION_IMPORTANCE)
    print(SKIP_CALIBRATION_RISKS)
    print(SAFER_ALTERNATIVES)
    
    print("\n🔧 具体建议:")
    print("1. 不建议完全跳过校准 - 这会严重影响手部功能")
    print("2. 建议采用方案1或方案3进行安全校准")
    print("3. 如果再次跳齿，停止校准并检查机械装配")
    print("4. 考虑联系ORCA技术支持获取专业建议")

def create_low_current_config():
    """创建低电流版本的配置文件"""
    import shutil
    
    config_path = "d:\\PROJECTS\\orca_core\\orca_core\\models\\orcahand_v1_right\\config.yaml"
    safe_config_path = config_path.replace(".yaml", "_safe.yaml")
    
    try:
        # 复制原配置文件
        shutil.copy2(config_path, safe_config_path)
        
        # 读取并修改
        with open(safe_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 降低电流设置
        modifications = [
            ('calib_current: 350', 'calib_current: 150'),
            ('wrist_calib_current: 100', 'wrist_calib_current: 80'),
            ('max_current: 300', 'max_current: 200')
        ]
        
        for old, new in modifications:
            if old in content:
                content = content.replace(old, new)
                print(f"✅ 修改: {old} -> {new}")
        
        # 保存安全配置
        with open(safe_config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ 安全配置文件已创建: {safe_config_path}")
        print("📝 使用方法:")
        print("   1. 将原config.yaml重命名为config_original.yaml")
        print("   2. 将config_safe.yaml重命名为config.yaml")
        print("   3. 重新尝试校准")
        
    except Exception as e:
        print(f"❌ 创建安全配置失败: {e}")

def step_by_step_guide():
    """提供步骤指导"""
    print("\n📋 跳齿问题解决步骤:")
    print("=" * 40)
    
    steps = [
        "🔍 检查机械状态",
        "   - 确认所有齿轮正确啮合",
        "   - 检查拉线张力是否适中",
        "   - 观察是否有明显的机械阻力",
        "",
        "⚙️ 降低校准参数",
        "   - 运行此脚本选择选项2创建安全配置",
        "   - 或手动修改config.yaml中的电流设置",
        "",
        "🧪 渐进式测试",
        "   - 先测试单个关节小幅运动",
        "   - 确认无异常后再进行校准",
        "   - 发现跳齿立即停止",
        "",
        "📞 寻求技术支持",
        "   - 如果问题持续，联系ORCA官方技术支持",
        "   - 提供跳齿的具体关节和情况描述"
    ]
    
    for step in steps:
        print(step)

if __name__ == "__main__":
    print("🔧 ORCA手部跳齿问题分析和解决")
    print("=" * 50)
    print("选择操作:")
    print("1. 查看校准重要性分析")
    print("2. 创建安全的低电流配置文件")
    print("3. 查看解决步骤指导")
    print("4. 退出")
    
    choice = input("\n请选择 (1-4): ")
    
    if choice == "1":
        print_analysis()
    elif choice == "2":
        create_low_current_config()
    elif choice == "3":
        step_by_step_guide()
    elif choice == "4":
        print("👋 再见！")
    else:
        print("❌ 无效选择")
        
    print("\n" + "=" * 60)
    print("🚨 重要提醒: 机械损坏会影响整个手部功能")
    print("💡 建议: 优先保护硬件，采用安全的校准参数")
    print("📞 如有疑问，请联系ORCA技术支持")
