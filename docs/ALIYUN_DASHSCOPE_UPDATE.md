# 阿里云DashScope SDK更新说明

## 更新概述

项目已更新为使用阿里云官方的 **DashScope SDK** 进行语音识别，替代之前的REST API方式。

## 主要变化

### 1. 使用官方SDK

**之前**: 使用 `requests` 库直接调用REST API  
**现在**: 使用 `dashscope.audio.asr.Recognition` 官方SDK

### 2. 更简洁的代码

官方SDK封装了底层细节，代码更简洁可靠：

```python
from dashscope.audio.asr import Recognition

recognition = Recognition(
    model='paraformer-realtime-v2',
    format='wav',
    sample_rate=16000,
    language_hints=['zh', 'en']
)
result = recognition.call('audio.wav')
```

### 3. 支持更多模型

- **paraformer-realtime-v2**: 支持中英文混合识别
- **fun-asr-realtime-2025-11-07**: 最新的语音识别模型

### 4. 更好的性能指标

SDK提供了详细的性能指标：
- `get_last_request_id()`: 请求ID
- `get_first_package_delay()`: 首包延迟
- `get_last_package_delay()`: 尾包延迟

## 安装步骤

### 1. 安装DashScope SDK

```bash
pip install dashscope
```

或更新所有依赖：

```bash
pip install -r requirements.txt
```

### 2. 配置API Key

在 `.env` 文件中配置：

```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=your_aliyun_api_key_here
ALIYUN_MODEL=paraformer-realtime-v2
```

### 3. 测试配置

运行测试脚本验证配置：

```bash
python test_aliyun_dashscope.py
```

## 配置说明

### 环境变量

```env
# 选择AI服务
AI_SERVICE=aliyun

# 阿里云API Key（必需）
ALIYUN_API_KEY=sk-xxxxxxxxxxxxx

# 模型选择（可选，默认为paraformer-realtime-v2）
ALIYUN_MODEL=paraformer-realtime-v2
```

### 支持的模型

#### paraformer-realtime-v2
- 支持中英文混合识别
- 支持 `language_hints` 参数
- 推荐用于中文场景

#### fun-asr-realtime-2025-11-07
- 最新的语音识别模型
- 不支持 `language_hints` 参数
- 性能更优

## 代码变化

### transcription_service.py

**主要改进**:
1. 使用 `dashscope.audio.asr.Recognition` 替代REST API
2. 根据模型自动选择是否使用 `language_hints`
3. 使用临时文件传递音频数据
4. 添加性能指标输出

**关键代码**:

```python
class AliyunTranscriptionService(TranscriptionService):
    def __init__(self):
        import dashscope
        from dashscope.audio.asr import Recognition
        
        dashscope.api_key = Config.ALIYUN_API_KEY
        self.Recognition = Recognition
        self.model = Config.ALIYUN_MODEL
    
    def transcribe(self, audio_data, sample_rate):
        # 创建临时WAV文件
        wav_bytes = self.audio_to_wav_bytes(audio_data, sample_rate)
        
        # 使用SDK识别
        recognition = self.Recognition(
            model=self.model,
            format='wav',
            sample_rate=sample_rate
        )
        result = recognition.call(temp_file_path)
        
        if result.status_code == HTTPStatus.OK:
            return result.get_sentence()
```

### config.py

**移除的配置**:
- `ALIYUN_APP_ID` (不再需要)
- `ALIYUN_ENDPOINT` (SDK内置)

**保留的配置**:
- `ALIYUN_API_KEY` (必需)
- `ALIYUN_MODEL` (可选)

## 迁移指南

### 从旧版本迁移

如果你之前使用的是REST API版本：

1. **安装新依赖**:
   ```bash
   pip install dashscope
   ```

2. **更新配置文件**:
   - 移除 `ALIYUN_APP_ID`
   - 移除 `ALIYUN_ENDPOINT`
   - 保留 `ALIYUN_API_KEY`

3. **测试新配置**:
   ```bash
   python test_aliyun_dashscope.py
   ```

### 配置示例

**旧配置** (.env):
```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-xxxxx
ALIYUN_APP_ID=app-xxxxx
ALIYUN_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/audio/asr
ALIYUN_MODEL=paraformer-realtime-v2
```

**新配置** (.env):
```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-xxxxx
ALIYUN_MODEL=paraformer-realtime-v2
```

## 优势

### 1. 更可靠
- 官方SDK，经过充分测试
- 自动处理API版本更新
- 更好的错误处理

### 2. 更简洁
- 减少了约100行代码
- 不需要手动构造请求
- 不需要解析复杂的响应结构

### 3. 更强大
- 支持更多模型
- 提供性能指标
- 更好的文档支持

### 4. 更易维护
- 跟随官方更新
- 减少兼容性问题
- 更好的社区支持

## 故障排除

### 问题1: dashscope未安装

**错误信息**:
```
[ERROR] dashscope SDK未安装
```

**解决方案**:
```bash
pip install dashscope
```

### 问题2: API Key无效

**错误信息**:
```
[Aliyun Error] 401: Invalid API Key
```

**解决方案**:
1. 检查 `.env` 文件中的 `ALIYUN_API_KEY`
2. 确认API Key格式正确（以 `sk-` 开头）
3. 在阿里云控制台验证API Key是否有效

### 问题3: 模型不支持

**错误信息**:
```
[Aliyun Error] 400: Model not found
```

**解决方案**:
1. 检查模型名称是否正确
2. 使用支持的模型:
   - `paraformer-realtime-v2`
   - `fun-asr-realtime-2025-11-07`

### 问题4: 无法识别语音

**可能原因**:
1. 音频质量太差
2. 音频时长太短（建议3秒以上）
3. 没有语音内容

**解决方案**:
1. 增加 `CHUNK_DURATION` 配置
2. 检查音频输入设备
3. 测试时使用清晰的语音

## 性能对比

### REST API方式
- 代码行数: ~120行
- 依赖: requests
- 维护成本: 高
- 错误处理: 手动

### DashScope SDK方式
- 代码行数: ~70行
- 依赖: dashscope
- 维护成本: 低
- 错误处理: 自动

## 参考资料

- [DashScope官方文档](https://help.aliyun.com/zh/dashscope/)
- [语音识别API文档](https://help.aliyun.com/zh/dashscope/developer-reference/api-details-9)
- [Python SDK文档](https://help.aliyun.com/zh/dashscope/developer-reference/python-sdk)

## 更新日志

### 2024-12-04 v2 - 基于官方示例优化
- ✅ 完全参考官方示例 `call_dashscope_paraformer-realtime-v2.md`
- ✅ 改进错误处理和日志输出
- ✅ 添加统计信息功能 (`get_stats()`)
- ✅ 优化性能指标输出（仅首次调用）
- ✅ 改进代码注释和文档
- ✅ 更好的资源清理机制

### 2024-12-04 v1 - 初始集成
- ✅ 集成DashScope官方SDK
- ✅ 支持 `paraformer-realtime-v2` 模型
- ✅ 支持 `fun-asr-realtime-2025-11-07` 模型
- ✅ 添加性能指标输出
- ✅ 简化配置项
- ✅ 添加测试脚本
- ✅ 更新文档

## 联系支持

如果遇到问题：
1. 查看本文档的故障排除部分
2. 运行 `test_aliyun_dashscope.py` 诊断
3. 查看阿里云DashScope官方文档
4. 提交Issue到项目仓库
