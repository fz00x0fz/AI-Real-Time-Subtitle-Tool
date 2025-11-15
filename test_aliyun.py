"""
测试阿里云百炼API连接和配置
"""
import sys
import numpy as np
from config import Config
from transcription_service import AliyunTranscriptionService


def test_aliyun_connection():
    """测试阿里云API连接"""
    print("=" * 50)
    print("阿里云百炼API连接测试")
    print("=" * 50)
    
    # 检查配置
    print("\n1. 检查配置...")
    print(f"   AI_SERVICE: {Config.AI_SERVICE}")
    print(f"   ALIYUN_API_KEY: {'已设置' if Config.ALIYUN_API_KEY else '未设置'}")
    print(f"   ALIYUN_MODEL: {Config.ALIYUN_MODEL}")
    print(f"   ALIYUN_ENDPOINT: {Config.ALIYUN_ENDPOINT}")
    
    if not Config.ALIYUN_API_KEY:
        print("\n❌ 错误: 未设置ALIYUN_API_KEY")
        print("请在.env文件中配置ALIYUN_API_KEY")
        return False
    
    # 初始化服务
    print("\n2. 初始化阿里云服务...")
    try:
        service = AliyunTranscriptionService()
        print("   ✓ 服务初始化成功")
    except Exception as e:
        print(f"   ❌ 服务初始化失败: {e}")
        return False
    
    # 生成测试音频（1秒的静音）
    print("\n3. 生成测试音频...")
    sample_rate = 16000
    duration = 1  # 1秒
    test_audio = np.zeros(sample_rate * duration, dtype=np.float32)
    print(f"   ✓ 生成 {duration}秒 测试音频 (采样率: {sample_rate}Hz)")
    
    # 测试API调用
    print("\n4. 测试API调用...")
    print("   (注意: 静音音频可能返回空结果，这是正常的)")
    try:
        result = service.transcribe(test_audio, sample_rate)
        print(f"   ✓ API调用成功")
        print(f"   识别结果: '{result}' (空结果是正常的)")
        return True
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n请确保已在.env文件中配置以下参数:")
    print("  AI_SERVICE=aliyun")
    print("  ALIYUN_API_KEY=your_api_key_here")
    print("\n开始测试...\n")
    
    success = test_aliyun_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 测试通过！阿里云百炼配置正确")
        print("\n可以运行主程序了:")
        print("  python main.py")
    else:
        print("❌ 测试失败，请检查配置")
        print("\n常见问题:")
        print("  1. 检查API Key是否正确")
        print("  2. 确认已开通阿里云百炼服务")
        print("  3. 检查网络连接")
        print("  4. 查看详细配置指南: docs/aliyun_setup.md")
    print("=" * 50)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
