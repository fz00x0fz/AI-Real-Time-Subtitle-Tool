"""
测试阿里云百炼API修复
"""
import numpy as np
from config import Config
from transcription_service import AliyunTranscriptionService

def test_aliyun_api():
    """测试阿里云API"""
    print("=" * 60)
    print("阿里云百炼API测试")
    print("=" * 60)
    print()
    
    # 检查配置
    print("检查配置...")
    print(f"API Key: {Config.ALIYUN_API_KEY[:20]}..." if Config.ALIYUN_API_KEY else "未配置")
    print(f"Model: {Config.ALIYUN_MODEL}")
    print(f"Endpoint: {Config.ALIYUN_ENDPOINT}")
    print()
    
    if not Config.ALIYUN_API_KEY:
        print("❌ 错误: 未配置ALIYUN_API_KEY")
        print("请在.env文件中配置:")
        print("ALIYUN_API_KEY=sk-your-key-here")
        return
    
    try:
        # 创建服务
        print("初始化阿里云服务...")
        service = AliyunTranscriptionService()
        print("✅ 服务初始化成功")
        print()
        
        # 创建测试音频（1秒的静音）
        print("创建测试音频...")
        sample_rate = 16000
        duration = 1.0
        audio_data = np.zeros(int(sample_rate * duration), dtype=np.float32)
        print(f"✅ 测试音频: {duration}秒, {sample_rate}Hz")
        print()
        
        # 测试转录
        print("发送API请求...")
        print("(这可能需要几秒钟)")
        result = service.transcribe(audio_data, sample_rate)
        print()
        
        if result:
            print("✅ API调用成功!")
            print(f"识别结果: {result}")
        else:
            print("⚠️  API调用成功，但未识别到语音")
            print("这是正常的，因为测试音频是静音")
        
        print()
        print("=" * 60)
        print("测试完成!")
        print("=" * 60)
        print()
        print("下一步:")
        print("1. 如果看到API调用成功，说明配置正确")
        print("2. 运行主程序: python main.py")
        print("3. 播放音频测试实际识别")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("常见问题:")
        print("1. API Key错误 - 检查.env中的ALIYUN_API_KEY")
        print("2. 网络问题 - 检查网络连接")
        print("3. 模型不支持 - 尝试使用 paraformer-realtime-v2")

if __name__ == "__main__":
    test_aliyun_api()
    input("\n按Enter键退出...")
