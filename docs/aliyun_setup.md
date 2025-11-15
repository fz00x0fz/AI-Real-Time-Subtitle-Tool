# 阿里云百炼平台配置指南

## 简介

阿里云百炼（DashScope）是阿里云提供的AI模型服务平台，提供语音识别、文本生成等多种AI能力。本工具支持使用阿里云百炼的语音识别服务进行实时字幕转录。

## 优势

- ✅ **中文优化**: 针对中文语音识别进行优化，识别准确率高
- ✅ **低延迟**: 国内访问速度快，延迟低
- ✅ **性价比高**: 相比国外服务，价格更优惠
- ✅ **免费额度**: 新用户有免费试用额度
- ✅ **支持多种模型**: Paraformer等先进语音识别模型

## 获取API密钥

### 1. 注册阿里云账号

访问 [阿里云官网](https://www.aliyun.com/) 注册账号。

### 2. 开通百炼服务

1. 访问 [阿里云百炼平台](https://dashscope.aliyun.com/)
2. 点击"立即开通"
3. 完成实名认证（如需要）

### 3. 创建API Key

1. 登录百炼控制台
2. 进入"API-KEY管理"页面
3. 点击"创建新的API-KEY"
4. 复制生成的API Key（格式类似：`sk-xxxxxxxxxxxxxxxxxxxxxxxx`）

### 4. （可选）创建应用

如果需要更精细的管理和统计，可以创建应用：

1. 在控制台点击"应用管理"
2. 创建新应用
3. 记录应用ID（App ID）

## 配置步骤

### 1. 编辑配置文件

复制 `.env.example` 为 `.env`（如果还没有）：

```bash
copy .env.example .env
```

### 2. 配置阿里云参数

编辑 `.env` 文件，设置以下参数：

```env
# 选择阿里云服务
AI_SERVICE=aliyun

# 阿里云百炼配置
ALIYUN_API_KEY=sk-your-api-key-here
ALIYUN_APP_ID=your-app-id-here  # 可选，如果创建了应用
ALIYUN_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/audio/asr
ALIYUN_MODEL=paraformer-realtime-v2
```

### 3. 参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `ALIYUN_API_KEY` | ✅ | 百炼平台API密钥 | - |
| `ALIYUN_APP_ID` | ❌ | 应用ID（可选） | - |
| `ALIYUN_ENDPOINT` | ❌ | API端点地址 | https://dashscope.aliyuncs.com/api/v1/services/audio/asr |
| `ALIYUN_MODEL` | ❌ | 语音识别模型 | paraformer-realtime-v2 |

### 4. 可用模型

阿里云百炼支持多种语音识别模型：

- **paraformer-realtime-v2**: 实时语音识别，推荐用于实时字幕
- **paraformer-v2**: 录音文件识别，准确率更高但延迟较大
- **paraformer-8k-v2**: 8kHz采样率模型，适合电话语音
- **paraformer-mtl-v2**: 多语言模型

## 运行应用

配置完成后，运行应用：

```bash
python main.py
```

或双击 `run.bat`

## 费用说明

### 计费方式

阿里云百炼语音识别按识别时长计费：

- **免费额度**: 新用户通常有一定的免费试用额度
- **按量付费**: 超出免费额度后按实际使用时长计费
- **价格**: 约 ¥0.003-0.005/分钟（具体以官网为准）

### 费用控制建议

1. **设置费用预警**: 在阿里云控制台设置费用预警
2. **调整音频块时长**: 增加 `CHUNK_DURATION` 减少API调用频率
3. **按需使用**: 不使用时及时停止录音

## 性能优化

### 降低延迟

```env
# 减小音频块时长
CHUNK_DURATION=2

# 使用实时模型
ALIYUN_MODEL=paraformer-realtime-v2
```

### 提高准确率

```env
# 增加音频块时长
CHUNK_DURATION=4

# 使用高精度模型
ALIYUN_MODEL=paraformer-v2
```

### 优化采样率

```env
# 标准采样率（推荐）
SAMPLE_RATE=16000

# 低采样率（节省带宽）
SAMPLE_RATE=8000
ALIYUN_MODEL=paraformer-8k-v2
```

## 常见问题

### Q1: API调用失败，返回401错误

**原因**: API Key错误或已过期

**解决方案**:
- 检查 `.env` 中的 `ALIYUN_API_KEY` 是否正确
- 确认API Key没有被删除或禁用
- 在百炼控制台重新生成API Key

### Q2: 识别结果为空

**原因**: 
- 音频质量差
- 音频时长太短
- 没有检测到语音

**解决方案**:
- 确保音频输入正常
- 增加 `CHUNK_DURATION` 提供更多音频数据
- 检查音频设备设置

### Q3: 识别延迟较高

**原因**: 网络延迟或音频块太大

**解决方案**:
- 减小 `CHUNK_DURATION` 到 2-3 秒
- 检查网络连接
- 使用 `paraformer-realtime-v2` 实时模型

### Q4: 中英文混合识别不准

**原因**: 模型针对单一语言优化

**解决方案**:
- 使用 `paraformer-mtl-v2` 多语言模型
- 在 `.env` 中调整语言参数

### Q5: 费用消耗过快

**解决方案**:
- 增加 `CHUNK_DURATION` 减少API调用次数
- 设置阿里云费用预警
- 考虑使用本地Whisper模型（完全免费）

## 高级配置

### 自定义语言和参数

如需更精细的控制，可以修改 `transcription_service.py` 中的 `AliyunTranscriptionService` 类：

```python
# 在 transcribe 方法中修改 parameters
'parameters': {
    'language': 'zh',  # 语言: zh, en, ja, ko等
    'enable_punctuation': True,  # 启用标点符号
    'enable_inverse_text_normalization': True,  # 数字转换
    'enable_words': False,  # 是否返回词级别时间戳
    'disfluency_removal': True,  # 去除口语化表达
}
```

### 支持的语言代码

- `zh`: 中文（普通话）
- `en`: 英语
- `ja`: 日语
- `ko`: 韩语
- `yue`: 粤语
- `auto`: 自动检测

## 技术支持

- **官方文档**: https://help.aliyun.com/zh/dashscope/
- **API文档**: https://help.aliyun.com/zh/dashscope/developer-reference/api-details
- **控制台**: https://dashscope.console.aliyun.com/

## 对比其他服务

| 特性 | 阿里云百炼 | OpenAI Whisper | Azure Speech | 本地Whisper |
|------|-----------|----------------|--------------|-------------|
| 中文识别 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 延迟 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 价格 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 国内访问 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

**推荐**: 对于国内用户，特别是需要中文识别的场景，阿里云百炼是性价比最高的选择！
