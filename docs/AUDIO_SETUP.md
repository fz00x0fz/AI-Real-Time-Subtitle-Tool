# 音频设置指南

## 🎯 问题：检测不到语音

如果看到 `No speech detected in audio chunk` 提示，说明应用正在捕获音频，但使用了错误的音频设备。

## 🔍 问题诊断

### 症状
```
Processing audio chunk: 48000 samples
No speech detected in audio chunk
```

### 原因
- 使用了**麦克风**（默认输入设备）
- 需要使用**立体声混音**来捕获系统播放的音频

## ✅ 解决方案

### 方法1: 启用并设置立体声混音（推荐）

#### Windows 10/11 步骤

1. **打开声音设置**
   - 右键点击任务栏的🔊音量图标
   - 选择"声音设置"

2. **打开声音控制面板**
   - 滚动到页面底部
   - 点击"声音控制面板"或"更多声音设置"

3. **显示已禁用的设备**
   - 切换到"录制"选项卡
   - 在空白处右键
   - 勾选"显示已禁用的设备"
   - 勾选"显示已断开的设备"

4. **启用立体声混音**
   - 找到"立体声混音"或"Stereo Mix"
   - 右键点击
   - 选择"启用"

5. **设置为默认设备**（重要！）
   - 右键"立体声混音"
   - 选择"设置为默认设备"
   - 点击"确定"

6. **重启应用**
   ```bash
   python main.py
   ```

### 方法2: 使用设备检测工具

运行设备检测脚本查找正确的设备索引：

```bash
python check_devices.py
```

脚本会显示：
- 所有可用设备列表
- 立体声混音设备的索引号
- 配置建议

### 方法3: 手动指定设备索引

#### 步骤1: 查看设备列表

```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

#### 步骤2: 找到立体声混音设备

查找包含以下关键词的设备：
- "Stereo Mix"
- "立体声混音"
- "What U Hear"
- "Wave Out Mix"

记下设备的索引号（例如：3）

#### 步骤3: 配置设备索引

**使用图形化配置界面**:
1. 启动应用: `python main.py`
2. 点击⚙按钮
3. 切换到"音频设置"标签页
4. 点击"查看可用设备"
5. 在"音频设备索引"中输入索引号
6. 点击"保存"
7. 重启应用

**或手动编辑.env文件**:
```env
AUDIO_DEVICE_INDEX=3  # 替换为你的设备索引号
```

## 🎤 不同使用场景

### 场景1: 转录视频/音乐（系统音频）
**使用**: 立体声混音  
**配置**: 
```env
AUDIO_DEVICE_INDEX=-1  # 自动选择（需设为默认）
# 或
AUDIO_DEVICE_INDEX=3   # 手动指定索引
```

### 场景2: 转录语音输入（麦克风）
**使用**: 麦克风  
**配置**: 
```env
AUDIO_DEVICE_INDEX=0   # 通常麦克风是索引0
```

### 场景3: 在线会议（混合音频）
**使用**: 立体声混音 + 虚拟音频设备  
**推荐**: 使用VB-Audio Virtual Cable等虚拟音频设备

## ❓ 常见问题

### Q1: 找不到立体声混音设备？

**原因**: 
- 声卡驱动不支持
- 设备被禁用
- 使用的是USB声卡

**解决方法**:

**方法A: 更新声卡驱动**
1. 打开设备管理器
2. 找到"声音、视频和游戏控制器"
3. 右键声卡，选择"更新驱动程序"

**方法B: 使用虚拟音频设备**
1. 下载安装 VB-Audio Virtual Cable
   - 官网: https://vb-audio.com/Cable/
2. 设置系统音频输出到虚拟设备
3. 在应用中选择虚拟设备作为输入

**方法C: 使用Realtek音频管理器**
1. 打开Realtek音频管理器
2. 启用"立体声混音"功能

### Q2: 启用后仍然检测不到语音？

**检查清单**:
- ✅ 立体声混音已启用
- ✅ 立体声混音已设为默认设备
- ✅ 应用已重启
- ✅ 系统正在播放音频
- ✅ 音量不是静音

**测试方法**:
1. 播放一段音频/视频
2. 运行 `python check_devices.py`
3. 确认设备索引
4. 重启应用测试

### Q3: 音频延迟太高？

**优化方法**:
1. 打开配置界面
2. 音频设置 → 音频块时长
3. 改为2秒（默认3秒）
4. 保存并重启

### Q4: 识别准确率低？

**优化方法**:
1. 增加音频块时长到4秒
2. 确保音频清晰，无杂音
3. 调整系统音量到合适水平
4. 使用更好的AI模型

### Q5: 麦克风和系统音频都想要？

**解决方案**:
使用虚拟音频混音器：
1. 安装 Voicemeeter Banana
2. 配置麦克风和系统音频混音
3. 在应用中选择Voicemeeter输出

## 🔧 测试音频捕获

### 测试脚本

创建 `test_audio.py`:
```python
import sounddevice as sd
import numpy as np

def test_audio_capture(device_index=-1, duration=5):
    """测试音频捕获"""
    print(f"测试设备索引: {device_index}")
    print(f"录制时长: {duration}秒")
    print("请播放音频...")
    
    # 录制音频
    audio = sd.rec(
        int(duration * 16000),
        samplerate=16000,
        channels=1,
        device=device_index
    )
    sd.wait()
    
    # 分析音频
    max_amplitude = np.max(np.abs(audio))
    mean_amplitude = np.mean(np.abs(audio))
    
    print(f"\n音频分析:")
    print(f"最大振幅: {max_amplitude:.4f}")
    print(f"平均振幅: {mean_amplitude:.4f}")
    
    if max_amplitude < 0.01:
        print("⚠️  音频信号太弱，可能没有捕获到声音")
    elif max_amplitude > 0.5:
        print("✅ 音频信号正常")
    else:
        print("⚠️  音频信号较弱，建议调高音量")

if __name__ == "__main__":
    # 测试默认设备
    test_audio_capture()
    
    # 或测试指定设备
    # test_audio_capture(device_index=3)
```

运行测试:
```bash
python test_audio.py
```

## 📚 相关文档

- **[README.md](README.md)** - 主文档
- **[SETTINGS_GUIDE.md](SETTINGS_GUIDE.md)** - 配置指南
- **[check_devices.py](check_devices.py)** - 设备检测工具

## 💡 最佳实践

1. **首次使用**
   - 运行 `python check_devices.py`
   - 确认立体声混音设备
   - 设置为默认设备

2. **日常使用**
   - 确保立体声混音已启用
   - 播放音频前启动应用
   - 调整合适的音量

3. **问题排查**
   - 检查设备是否正确
   - 确认音频正在播放
   - 查看控制台输出
   - 运行设备检测工具

## 🎉 成功标志

当配置正确时，你会看到：
```
Processing audio chunk: 48000 samples
Transcription result: [识别出的文字内容]
```

而不是：
```
No speech detected in audio chunk
```

---

**需要帮助？** 运行 `python check_devices.py` 获取设备信息！
