"""
音频设备检测工具
帮助用户找到正确的音频设备索引
"""
import sounddevice as sd

def check_audio_devices():
    """检查并显示所有可用的音频设备"""
    print("=" * 60)
    print("音频设备检测工具")
    print("=" * 60)
    print()
    
    try:
        devices = sd.query_devices()
        
        print("📋 所有可用设备:")
        print("-" * 60)
        for i, device in enumerate(devices):
            print(f"\n设备 [{i}]:")
            print(f"  名称: {device['name']}")
            print(f"  输入通道: {device['max_input_channels']}")
            print(f"  输出通道: {device['max_output_channels']}")
            print(f"  默认采样率: {device['default_samplerate']}")
            
            # 标记特殊设备
            if 'stereo mix' in device['name'].lower() or '立体声混音' in device['name'].lower():
                print("  ⭐ 这是立体声混音设备！（推荐用于捕获系统音频）")
            elif device['max_input_channels'] > 0:
                print("  🎤 这是输入设备")
            elif device['max_output_channels'] > 0:
                print("  🔊 这是输出设备")
        
        print("\n" + "=" * 60)
        print("🎯 推荐配置:")
        print("=" * 60)
        
        # 查找立体声混音设备
        stereo_mix_found = False
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                if 'stereo mix' in device['name'].lower() or '立体声混音' in device['name'].lower():
                    print(f"\n✅ 找到立体声混音设备: [{i}] {device['name']}")
                    print(f"\n在.env文件中设置:")
                    print(f"AUDIO_DEVICE_INDEX={i}")
                    print(f"\n或在图形化配置界面中:")
                    print(f"音频设置 → 音频设备索引 → {i}")
                    stereo_mix_found = True
                    break
        
        if not stereo_mix_found:
            print("\n⚠️  未找到立体声混音设备！")
            print("\n请按以下步骤启用:")
            print("1. 右键点击任务栏音量图标")
            print("2. 选择'声音设置' → '声音控制面板'")
            print("3. 切换到'录制'选项卡")
            print("4. 右键空白处，勾选'显示已禁用的设备'")
            print("5. 找到'立体声混音'，右键启用")
            print("6. 右键设置为默认设备")
            print("7. 重新运行此脚本确认")
            
            print("\n📋 可用的输入设备:")
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    print(f"  [{i}] {device['name']}")
        
        print("\n" + "=" * 60)
        print("💡 提示:")
        print("=" * 60)
        print("• 立体声混音用于捕获系统播放的音频")
        print("• 麦克风用于捕获外部声音")
        print("• 如果要实时转录视频/音乐，请使用立体声混音")
        print("• 如果要转录语音输入，请使用麦克风")
        print()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n请确保已安装sounddevice:")
        print("pip install sounddevice")

if __name__ == "__main__":
    check_audio_devices()
    input("\n按Enter键退出...")
