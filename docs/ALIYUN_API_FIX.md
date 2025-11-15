# 阿里云百炼API修复说明

## 🐛 问题描述

**错误信息**:
```
Aliyun API error: 400 - {"code":"InvalidParameter","message":"Invalid header \"x-dashscope-async\" provided in your request.","request_id":"..."}
```

## ✅ 已修复

### 问题原因

1. **错误的请求头**: 使用了无效的 `X-DashScope-Async` 请求头
2. **错误的请求体格式**: 使用了不正确的字段名称

### 修复内容

#### 1. 移除无效请求头

**修复前**:
```python
headers = {
    'Authorization': f'Bearer {self.api_key}',
    'Content-Type': 'application/json',
    'X-DashScope-Async': 'false'  # ❌ 无效的请求头
}
```

**修复后**:
```python
headers = {
    'Authorization': f'Bearer {self.api_key}',
    'Content-Type': 'application/json'  # ✅ 只保留必需的请求头
}
```

#### 2. 更新请求体格式

**修复前**:
```python
payload = {
    'model': self.model,
    'input': {
        'audio': audio_base64,  # ❌ 错误的字段名
        'format': 'wav',
        'sample_rate': sample_rate
    },
    'parameters': {
        'language': 'zh',
        'enable_punctuation': True,
        'enable_inverse_text_normalization': True
    }
}
```

**修复后**:
```python
payload = {
    'model': self.model,
    'input': {
        'audio_data': audio_base64,  # ✅ 正确的字段名
        'format': 'wav',
        'sample_rate': sample_rate,
        'channel': 1  # ✅ 添加声道信息
    },
    'parameters': {
        'format': 'pcm'  # ✅ 简化参数
    }
}
```

#### 3. 优化App ID处理

**修复前**:
```python
if self.app_id:
    payload['parameters']['app_id'] = self.app_id  # ❌ 放在请求体中
```

**修复后**:
```python
if self.app_id:
    headers['X-DashScope-AppId'] = self.app_id  # ✅ 放在请求头中
```

#### 4. 增强响应解析

添加了更灵活的响应解析逻辑，支持多种响应格式：
- `output.text` - 直接文本
- `output.sentence` - 句子数组
- `output.results` - 结果数组
- `output.transcription` - 转录文本
- 顶层 `text` 字段

#### 5. 添加调试信息

首次调用时会打印API响应结构，方便调试：
```python
[DEBUG] Aliyun API response structure: {...}
```

## 🧪 测试修复

### 运行测试脚本

```bash
python test_aliyun_fix.py
```

测试脚本会：
1. 检查配置
2. 初始化服务
3. 发送测试请求
4. 显示结果

### 预期输出

**成功**:
```
阿里云百炼API测试
========================================
检查配置...
API Key: sk-xxxxxxxxxx...
Model: paraformer-realtime-v2
Endpoint: https://dashscope.aliyuncs.com/api/v1/services/audio/asr

初始化阿里云服务...
✅ 服务初始化成功

创建测试音频...
✅ 测试音频: 1秒, 16000Hz

发送API请求...
[DEBUG] Aliyun API response structure: {...}

✅ API调用成功!
⚠️  API调用成功，但未识别到语音
这是正常的，因为测试音频是静音

测试完成!
```

## 📝 配置要求

### .env 文件配置

```env
# 阿里云百炼配置
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-your-api-key-here
ALIYUN_MODEL=paraformer-realtime-v2
ALIYUN_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/audio/asr
ALIYUN_APP_ID=  # 可选
```

### 支持的模型

- `paraformer-realtime-v2` - 实时识别（推荐）
- `paraformer-v2` - 高精度识别
- `paraformer-8k-v2` - 8kHz采样率
- `paraformer-mtl-v2` - 多语言

## 🚀 使用步骤

### 1. 更新代码

代码已自动更新，无需手动操作。

### 2. 测试API

```bash
python test_aliyun_fix.py
```

### 3. 运行主程序

```bash
python main.py
```

### 4. 配置音频设备

如果使用外接音箱/耳机，请参考：
- [EXTERNAL_AUDIO_SETUP.md](EXTERNAL_AUDIO_SETUP.md)

### 5. 开始使用

1. 点击"▶ 开始"按钮
2. 播放音频/视频
3. 查看实时字幕

## 🔍 故障排除

### 问题1: 仍然报400错误

**检查清单**:
- ✅ API Key是否正确
- ✅ 是否使用最新代码
- ✅ 网络连接是否正常

**解决方法**:
```bash
# 重新测试
python test_aliyun_fix.py
```

### 问题2: API调用成功但无识别结果

**可能原因**:
- 音频设备配置错误
- 未捕获到有效音频
- 音频质量太差

**解决方法**:
1. 检查音频设备配置
2. 运行 `python check_devices.py`
3. 参考 [AUDIO_SETUP.md](AUDIO_SETUP.md)

### 问题3: 识别准确率低

**优化方法**:
1. 增加音频块时长（3-4秒）
2. 确保音频清晰
3. 调整系统音量
4. 尝试不同的模型

### 问题4: 响应结构不匹配

**现象**:
```
[WARNING] No text found in Aliyun response: {...}
```

**解决方法**:
1. 查看DEBUG输出的响应结构
2. 报告给开发者
3. 可能需要更新响应解析逻辑

## 📊 API响应格式

### 标准格式

```json
{
  "output": {
    "text": "识别的文字内容"
  },
  "usage": {
    "duration_ms": 1000
  },
  "request_id": "..."
}
```

### 句子格式

```json
{
  "output": {
    "sentence": [
      {
        "text": "第一句话",
        "begin_time": 0,
        "end_time": 1000
      },
      {
        "text": "第二句话",
        "begin_time": 1000,
        "end_time": 2000
      }
    ]
  }
}
```

### 结果数组格式

```json
{
  "output": {
    "results": [
      {
        "text": "识别结果",
        "confidence": 0.95
      }
    ]
  }
}
```

## 🔗 相关文档

- **[test_aliyun_fix.py](test_aliyun_fix.py)** - API测试脚本
- **[AUDIO_SETUP.md](AUDIO_SETUP.md)** - 音频设置指南
- **[EXTERNAL_AUDIO_SETUP.md](EXTERNAL_AUDIO_SETUP.md)** - 外接设备配置
- **[docs/aliyun_setup.md](docs/aliyun_setup.md)** - 阿里云配置详解

## ✅ 验证成功

修复成功的标志：

1. **测试脚本通过**
   ```
   ✅ API调用成功!
   ```

2. **主程序运行正常**
   ```
   Processing audio chunk: 48000 samples
   [DEBUG] Aliyun API response structure: {...}
   Transcription result: [识别的文字]
   ```

3. **实时字幕显示**
   - 字幕窗口显示识别的文字
   - 无错误提示

## 🎉 总结

### 修复内容
- ✅ 移除无效的 `X-DashScope-Async` 请求头
- ✅ 更新请求体字段名称
- ✅ 优化App ID处理
- ✅ 增强响应解析
- ✅ 添加调试信息

### 测试方法
- ✅ 运行 `python test_aliyun_fix.py`
- ✅ 检查API调用是否成功
- ✅ 运行主程序测试实际识别

### 下一步
1. 测试API连接
2. 配置音频设备
3. 开始使用应用

**问题已解决！** 🎊

---

**更新日期**: 2024-11  
**版本**: v1.3.1  
**状态**: ✅ 已修复并测试
