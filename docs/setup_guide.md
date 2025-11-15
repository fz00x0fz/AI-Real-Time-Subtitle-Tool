# 详细安装指南

## Windows系统配置

### 1. 安装Python

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载Python 3.8或更高版本
3. 安装时勾选"Add Python to PATH"
4. 验证安装：
   ```bash
   python --version
   ```

### 2. 安装依赖包

#### 方法1: 自动安装（推荐）

双击运行`run.bat`，脚本会自动检查并安装依赖。

#### 方法2: 手动安装

```bash
cd ai_subtitle_tool
pip install -r requirements.txt
```

#### PyAudio安装问题解决

如果PyAudio安装失败，尝试以下方法：

**方法A: 使用pipwin**
```bash
pip install pipwin
pipwin install pyaudio
```

**方法B: 下载预编译包**
1. 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. 下载对应Python版本的.whl文件
3. 安装：`pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl`

**方法C: 使用conda**
```bash
conda install pyaudio
```

### 3. 配置音频设备

#### 启用立体声混音（Stereo Mix）

**Windows 10/11:**

1. 右键点击任务栏右下角的音量图标
2. 选择"声音设置"
3. 向下滚动，点击"声音控制面板"
4. 切换到"录制"选项卡
5. 右键点击空白区域，勾选"显示已禁用的设备"
6. 找到"立体声混音"或"Stereo Mix"
7. 右键点击，选择"启用"
8. （可选）右键点击，选择"设置为默认设备"

**如果找不到立体声混音:**

某些声卡驱动可能不支持，可以尝试：
- 更新声卡驱动程序
- 使用虚拟音频设备（如VB-Audio Virtual Cable）

#### 安装虚拟音频设备（备选方案）

如果系统不支持立体声混音，可以使用虚拟音频设备：

1. 下载VB-Audio Virtual Cable: https://vb-audio.com/Cable/
2. 安装后，在"播放设备"中将"CABLE Input"设为默认
3. 在"录制设备"中启用"CABLE Output"
4. 在应用程序中选择"CABLE Output"作为音频输入

### 4. 获取API密钥

#### OpenAI API密钥（推荐）

1. 访问 https://platform.openai.com/
2. 注册/登录账号
3. 进入API Keys页面
4. 创建新的API密钥
5. 复制密钥到`.env`文件

**费用说明:**
- Whisper API按分钟计费
- 约$0.006/分钟
- 建议设置使用限额

#### Azure Speech Service密钥

1. 访问 https://azure.microsoft.com/
2. 创建Azure账号（有免费额度）
3. 创建"语音服务"资源
4. 获取密钥和区域
5. 复制到`.env`文件

**免费额度:**
- 每月5小时免费语音转文字
- 超出后按使用量计费

#### 阿里云百炼密钥（国内推荐）

1. 访问 https://dashscope.aliyun.com/
2. 注册/登录阿里云账号
3. 开通百炼服务
4. 创建API Key
5. 复制密钥到`.env`文件

**优势:**
- 中文识别准确率高
- 国内访问速度快
- 价格实惠（约¥0.003-0.005/分钟）
- 有免费试用额度

**详细配置**: 查看 [docs/aliyun_setup.md](docs/aliyun_setup.md)

#### 本地Whisper模型（免费）

无需API密钥，但需要：
- 较好的CPU/GPU性能
- 足够的内存（至少8GB）
- 首次运行会下载模型文件

安装额外依赖：
```bash
pip install openai-whisper
```

### 5. 配置环境变量

1. 复制`.env.example`为`.env`
2. 根据选择的AI服务编辑配置

**OpenAI配置示例:**
```env
AI_SERVICE=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=whisper-1
```

**Azure配置示例:**
```env
AI_SERVICE=azure
AZURE_SPEECH_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_SPEECH_REGION=eastus
```

**阿里云百炼配置示例:**
```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ALIYUN_MODEL=paraformer-realtime-v2
```

**本地Whisper配置示例:**
```env
AI_SERVICE=local_whisper
```

### 6. 测试运行

```bash
# 方法1: 使用批处理文件
run.bat

# 方法2: 直接运行Python
python main.py
```

## 常见问题

### Q1: 程序启动后没有声音输入

**A:** 
- 检查是否启用了立体声混音
- 查看控制台输出的设备列表
- 尝试手动指定设备索引

### Q2: API调用失败

**A:**
- 检查API密钥是否正确
- 确认网络连接正常
- 检查API账户余额
- 查看控制台错误信息

### Q3: 转录结果不准确

**A:**
- 增加`CHUNK_DURATION`获取更多上下文
- 确保音频质量良好
- 尝试不同的AI服务
- 调整音频采样率

### Q4: 程序运行缓慢

**A:**
- 减小`CHUNK_DURATION`
- 使用更快的AI服务（Azure实时流式）
- 检查网络延迟
- 考虑使用本地Whisper（需要GPU）

### Q5: 窗口显示异常

**A:**
- 调整`.env`中的UI参数
- 检查显示器缩放设置
- 尝试不同的窗口透明度

## 性能优化建议

### 降低延迟
- 使用Azure Speech Service的实时流式识别
- 减小音频块时长（CHUNK_DURATION）
- 使用本地Whisper模型（需要GPU）

### 提高准确度
- 增加音频块时长
- 使用更大的Whisper模型（large）
- 确保音频质量清晰

### 降低成本
- 使用本地Whisper模型（完全免费）
- 使用Azure免费额度
- 增加CHUNK_DURATION减少API调用次数

## 技术支持

如遇到问题，请：
1. 查看控制台输出的详细错误信息
2. 检查`.env`配置是否正确
3. 确认所有依赖已正确安装
4. 查看README.md中的故障排除部分

## 进阶配置

### 自定义音频设备

在`.env`中设置：
```env
AUDIO_DEVICE_INDEX=2  # 使用特定设备索引
```

运行程序查看所有可用设备及其索引。

### 调整UI样式

修改`subtitle_window.py`中的样式表代码自定义外观。

### 添加自定义AI服务

在`transcription_service.py`中实现新的`TranscriptionService`子类。

---

**祝使用愉快！** 🎉
