"""
测试配置窗口
验证Whisper安装功能是否正常工作
"""
import sys
from PyQt5.QtWidgets import QApplication
from settings_window import SettingsWindow

def test_settings_window():
    """测试配置窗口"""
    print("=" * 60)
    print("配置窗口测试")
    print("=" * 60)
    print()
    
    app = QApplication(sys.argv)
    
    try:
        print("创建配置窗口...")
        window = SettingsWindow()
        print("✅ 配置窗口创建成功")
        print()
        
        print("检查Whisper状态...")
        window.update_whisper_status()
        print("✅ Whisper状态更新成功")
        print()
        
        print("显示窗口...")
        window.show()
        print("✅ 窗口显示成功")
        print()
        
        print("=" * 60)
        print("测试通过！")
        print("=" * 60)
        print()
        print("请在窗口中测试:")
        print("1. 查看本地模型状态")
        print("2. 点击安装按钮（如果需要）")
        print("3. 关闭窗口退出")
        print()
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_settings_window()
