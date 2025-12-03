# 快速迁移到DashScope SDK

## 🚀 3步完成迁移

### 步骤1: 安装DashScope SDK

```bash
pip install dashscope
```

### 步骤2: 更新配置文件

编辑 `.env` 文件，**移除**以下配置项：
```env
# 删除这些（不再需要）
ALIYUN_APP_ID=...
ALIYUN_ENDPOINT=...
```

**保留**以下配置：
```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=your_aliyun_api_key_here
ALIYUN_MODEL=paraformer-realtime-v2
```

### 步骤3: 测试配置

```bash
python test_aliyun_dashscope.py
```

## ✅ 完成！

如果测试通过，你已经成功迁移到DashScope SDK。

## 📝 配置对比

### 旧配置
```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-xxxxx
ALIYUN_APP_ID=app-xxxxx
ALIYUN_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/audio/asr
ALIYUN_MODEL=paraformer-realtime-v2
```

### 新配置
```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-xxxxx
ALIYUN_MODEL=paraformer-realtime-v2
```

## 🎯 支持的模型

- `paraformer-realtime-v2` - 支持中英文混合（推荐）
- `fun-asr-realtime-2025-11-07` - 最新模型

## 💡 优势

- ✅ 更简洁的配置
- ✅ 更可靠的API调用
- ✅ 官方SDK支持
- ✅ 自动错误处理
- ✅ 性能指标输出

## 🔧 故障排除

### 问题: dashscope未安装

```bash
pip install dashscope
```

### 问题: API Key无效

检查 `.env` 文件中的 `ALIYUN_API_KEY` 是否正确。

### 问题: 无法识别语音

1. 确保音频时长足够（建议3秒以上）
2. 检查音频输入设备
3. 增加 `CHUNK_DURATION` 配置

## 📚 详细文档

查看完整文档：[docs/ALIYUN_DASHSCOPE_UPDATE.md](docs/ALIYUN_DASHSCOPE_UPDATE.md)
