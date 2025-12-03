"""
测试阿里云DashScope SDK语音识别功能
"""
import os
import sys
import numpy as np
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_dashscope_import():
    """测试dashscope SDK是否已安装"""
    print("=" * 60)
    print("测试1: 检查dashscope SDK")
    print("=" * 60)
    try:
        import dashscope
        from dashscope.audio.asr import Recognition
        from http import HTTPStatus
        print("✓ dashscope SDK已安装")
        print(f"  版本: {dashscope.__version__ if hasattr(dashscope, '__version__') else '未知'}")
        return True
    except ImportError as e:
        print("✗ dashscope SDK未安装")
        print(f"  错误: {e}")
        print("\n请安装: pip install dashscope")
        return False

def test_api_key():
    """测试API Key配置"""
    print("\n" + "=" * 60)
    print("测试2: 检查API Key配置")
    print("=" * 60)
    
    api_key = os.getenv('ALIYUN_API_KEY', '')
    if api_key and api_key != 'your_aliyun_api_key_here':
        print("✓ API Key已配置")
        print(f"  Key前缀: {api_key[:8]}...")
        return True
    else:
        print("✗ API Key未配置")
        print("  请在.env文件中设置ALIYUN_API_KEY")
        return False

def test_transcription_service():
    """测试转录服务初始化"""
    print("\n" + "=" * 60)
    print("测试3: 初始化转录服务")
    print("=" * 60)
    
    try:
        from config import Config
        from transcription_service import AliyunTranscriptionService
        
        # 设置为使用阿里云服务
        Config.AI_SERVICE = 'aliyun'
        
        service = AliyunTranscriptionService()
        print("✓ 转录服务初始化成功")
        print(f"  模型: {service.model}")
        print(f"  采样率: {service.sample_rate}")
        return service
    except Exception as e:
        print(f"✗ 转录服务初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_audio_transcription(service):
    """测试音频转录功能"""
    print("\n" + "=" * 60)
    print("测试4: 测试音频转录")
    print("=" * 60)
    
    if service is None:
        print("✗ 跳过测试（服务未初始化）")
        return False
    
    try:
        # 生成测试音频（1秒的440Hz正弦波）
        sample_rate = 16000
        duration = 1.0
        frequency = 440.0
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t).astype(np.float32)
        
        print(f"生成测试音频: {len(audio_data)} 采样点")
        print("注意: 这是纯音测试，可能无法识别出文字")
        print("正在调用API...")
        
        # 调用转录服务
        result = service.transcribe(audio_data, sample_rate)
        
        if result:
            print(f"✓ API调用成功")
            print(f"  识别结果: {result}")
        else:
            print("✓ API调用成功（无识别结果，这是正常的，因为是纯音测试）")
        
        # 显示统计信息
        stats = service.get_stats()
        if stats:
            print(f"\n统计信息:")
            print(f"  总调用次数: {stats['total_calls']}")
            print(f"  成功次数: {stats['success_calls']}")
            print(f"  成功率: {stats['success_rate']}")
        
        return True
        
    except Exception as e:
        print(f"✗ 音频转录失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("阿里云DashScope SDK 语音识别测试")
    print("=" * 60)
    
    # 测试1: SDK安装
    if not test_dashscope_import():
        print("\n" + "=" * 60)
        print("测试终止: 请先安装dashscope SDK")
        print("=" * 60)
        return
    
    # 测试2: API Key
    if not test_api_key():
        print("\n" + "=" * 60)
        print("测试终止: 请先配置API Key")
        print("=" * 60)
        return
    
    # 测试3: 服务初始化
    service = test_transcription_service()
    
    # 测试4: 音频转录
    test_audio_transcription(service)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n提示:")
    print("1. 如果所有测试通过，说明配置正确")
    print("2. 纯音测试可能无法识别出文字，这是正常的")
    print("3. 实际使用时，请用真实的语音音频进行测试")
    print("4. 支持的模型:")
    print("   - paraformer-realtime-v2 (支持中英文混合)")
    print("   - fun-asr-realtime-2025-11-07 (最新模型)")

if __name__ == "__main__":
    main()
