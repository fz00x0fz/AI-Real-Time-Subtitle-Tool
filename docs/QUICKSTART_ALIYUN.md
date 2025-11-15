# 阿里云百炼快速启动指南

> 5分钟快速配置并运行AI实时字幕工具

## 🚀 快速开始

### 第一步：安装Python依赖

```bash
cd ai_subtitle_tool
pip install -r requirements.txt
```

### 第二步：获取阿里云API密钥

1. 访问 **[阿里云百炼平台](https://dashscope.aliyun.com/)**
2. 点击右上角**登录/注册**
3. 完成登录后，点击**立即开通**百炼服务
4. 进入**API-KEY管理**页面
5. 点击**创建新的API-KEY**
6. **复制生成的API Key**（格式：`sk-xxxxx...`）

### 第三步：配置环境变量

**方法1: 使用阿里云专用配置模板**

```bash
copy .env.aliyun.example .env
```

然后编辑 `.env` 文件，将你的API Key填入：

```env
ALIYUN_API_KEY=sk-your-actual-api-key-here
```

**方法2: 手动创建配置**

创建 `.env` 文件，内容如下：

```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-your-actual-api-key-here
ALIYUN_MODEL=paraformer-realtime-v2
SAMPLE_RATE=16000
CHUNK_DURATION=3
```

### 第四步：启用系统音频捕获

1. 右键点击任务栏的**音量图标**
2. 选择**声音设置** → **声音控制面板**
3. 切换到**录制**选项卡
4. 右键空白处，勾选**显示已禁用的设备**
5. 找到**立体声混音**，右键选择**启用**

### 第五步：测试配置（可选）

运行测试脚本验证配置：

```bash
python test_aliyun.py
```

如果看到 `✅ 测试通过！` 说明配置正确。

### 第六步：运行应用

```bash
python main.py
```

或者双击 `run.bat`

## 🎮 使用说明

1. **启动应用**后会显示浮动字幕窗口
2. 点击**▶ 开始**按钮开始捕获音频
3. 播放任何音频/视频，字幕会实时显示
4. 点击**■ 停止**按钮停止捕获
5. 可以拖动窗口到任意位置

## ⚙️ 常用配置调整

### 提高识别准确率

编辑 `.env` 文件：

```env
CHUNK_DURATION=4  # 增加音频块时长
ALIYUN_MODEL=paraformer-v2  # 使用高精度模型
```

### 降低延迟

```env
CHUNK_DURATION=2  # 减小音频块时长
ALIYUN_MODEL=paraformer-realtime-v2  # 使用实时模型
```

### 调整窗口样式

```env
WINDOW_WIDTH=1000  # 窗口宽度
WINDOW_HEIGHT=150  # 窗口高度
WINDOW_OPACITY=0.9  # 透明度
FONT_SIZE=28  # 字体大小
```

## 💰 费用说明

- **免费额度**: 新用户通常有免费试用额度
- **按量计费**: 约 ¥0.003-0.005/分钟
- **费用控制**: 在阿里云控制台设置费用预警

**示例**: 每天使用1小时，月费用约 ¥5-10

## ❓ 常见问题

### Q: 没有识别到任何文字？

**A**: 
- 确保已启用"立体声混音"
- 检查音频是否正常播放
- 增加 `CHUNK_DURATION` 到 4-5 秒

### Q: API调用失败？

**A**:
- 检查API Key是否正确
- 确认已开通百炼服务
- 运行 `python test_aliyun.py` 测试

### Q: 识别延迟太高？

**A**:
- 减小 `CHUNK_DURATION` 到 2 秒
- 检查网络连接
- 使用 `paraformer-realtime-v2` 模型

### Q: 中英文混合识别不准？

**A**:
- 使用 `paraformer-mtl-v2` 多语言模型
- 或者针对主要语言选择对应模型

## 📚 更多资源

- **详细配置指南**: [docs/aliyun_setup.md](docs/aliyun_setup.md)
- **完整文档**: [README.md](README.md)
- **阿里云官方文档**: https://help.aliyun.com/zh/dashscope/

## 🎉 完成！

现在你可以享受实时AI字幕了！

**小贴士**: 
- 拖动窗口到屏幕底部作为字幕显示
- 调整透明度以适应不同背景
- 使用快捷方式快速启动应用

---

**遇到问题？** 查看 [setup_guide.md](setup_guide.md) 获取详细故障排除指南。
