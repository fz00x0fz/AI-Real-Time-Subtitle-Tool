# 阿里云百炼集成更新日志

## 新增功能

### ✨ 阿里云百炼语音识别支持

现在AI实时字幕工具支持使用阿里云百炼（DashScope）平台的语音识别服务！

### 主要特性

- ✅ **完整的阿里云API集成**
- ✅ **支持多种Paraformer模型**
- ✅ **中文识别优化**
- ✅ **实时和高精度模式**
- ✅ **灵活的配置选项**

## 更新内容

### 1. 核心代码更新

#### `transcription_service.py`
- 新增 `AliyunTranscriptionService` 类
- 实现阿里云百炼API调用逻辑
- 支持base64音频编码
- 完善的错误处理和日志输出
- 更新工厂函数支持 `aliyun` 服务类型

#### `config.py`
- 新增阿里云配置项：
  - `ALIYUN_API_KEY`: API密钥
  - `ALIYUN_APP_ID`: 应用ID（可选）
  - `ALIYUN_ENDPOINT`: API端点
  - `ALIYUN_MODEL`: 识别模型
- 新增配置验证逻辑

#### `.env.example`
- 添加阿里云配置示例
- 更新服务选项说明

### 2. 文档更新

#### 新增文档

- **`docs/aliyun_setup.md`**: 阿里云百炼详细配置指南
  - API密钥获取步骤
  - 模型选择说明
  - 性能优化建议
  - 常见问题解答
  - 费用说明

- **`QUICKSTART_ALIYUN.md`**: 5分钟快速启动指南
  - 简化的配置流程
  - 快速上手步骤
  - 常用配置示例

- **`.env.aliyun.example`**: 阿里云专用配置模板
  - 预配置的阿里云参数
  - 详细的参数说明

- **`test_aliyun.py`**: 阿里云配置测试脚本
  - 验证API连接
  - 测试配置正确性
  - 诊断常见问题

#### 更新文档

- **`README.md`**
  - 添加阿里云服务说明
  - 更新功能特性列表
  - 新增配置示例

- **`setup_guide.md`**
  - 添加阿里云密钥获取步骤
  - 新增配置示例
  - 补充优势说明

## 支持的模型

### Paraformer系列

| 模型 | 用途 | 特点 |
|------|------|------|
| `paraformer-realtime-v2` | 实时识别 | 低延迟，适合实时字幕 |
| `paraformer-v2` | 录音识别 | 高准确率，延迟较高 |
| `paraformer-8k-v2` | 电话语音 | 8kHz采样率优化 |
| `paraformer-mtl-v2` | 多语言 | 支持中英文混合 |

## 配置示例

### 基础配置

```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-your-api-key-here
ALIYUN_MODEL=paraformer-realtime-v2
```

### 高精度配置

```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-your-api-key-here
ALIYUN_MODEL=paraformer-v2
CHUNK_DURATION=4
SAMPLE_RATE=16000
```

### 低延迟配置

```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-your-api-key-here
ALIYUN_MODEL=paraformer-realtime-v2
CHUNK_DURATION=2
SAMPLE_RATE=16000
```

## 使用方法

### 1. 配置

```bash
# 使用阿里云专用模板
copy .env.aliyun.example .env

# 编辑.env文件，填入API Key
notepad .env
```

### 2. 测试

```bash
# 测试配置是否正确
python test_aliyun.py
```

### 3. 运行

```bash
# 启动应用
python main.py
```

## 性能对比

| 服务 | 中文识别 | 延迟 | 价格 | 国内访问 |
|------|---------|------|------|---------|
| 阿里云百炼 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| OpenAI | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Azure | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 本地Whisper | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 优势

### 🎯 针对国内用户优化

- 服务器在国内，访问速度快
- 无需科学上网
- 支付方式便捷

### 🇨🇳 中文识别优化

- 专门针对中文优化
- 支持普通话、粤语等方言
- 识别准确率高

### 💰 性价比高

- 价格实惠（约¥0.003-0.005/分钟）
- 有免费试用额度
- 按实际使用量计费

### ⚡ 低延迟

- 国内访问延迟低
- 实时模型响应快
- 适合实时字幕场景

## 兼容性

- ✅ Windows 10/11
- ✅ Python 3.8+
- ✅ 与现有功能完全兼容
- ✅ 可随时切换其他AI服务

## 测试状态

- ✅ API连接测试
- ✅ 音频转码测试
- ✅ 识别功能测试
- ✅ 错误处理测试
- ✅ 配置验证测试

## 后续计划

- [ ] 支持流式识别（WebSocket）
- [ ] 添加语言自动检测
- [ ] 支持更多方言
- [ ] 优化音频预处理
- [ ] 添加识别结果缓存

## 贡献者

感谢所有为此功能做出贡献的开发者！

## 反馈

如有问题或建议，请：
1. 查看 `docs/aliyun_setup.md` 详细文档
2. 运行 `python test_aliyun.py` 诊断问题
3. 提交Issue反馈

---

**版本**: v1.1.0  
**更新日期**: 2024-11  
**状态**: ✅ 稳定
