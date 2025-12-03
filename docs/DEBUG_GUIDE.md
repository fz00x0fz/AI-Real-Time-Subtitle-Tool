# 调试指南 (Debug Guide)

## 问题：调试退出后Shell窗口无法终止

### 问题描述

在Windows上调试PyQt5应用程序时，有时会遇到以下问题：
- 程序退出后，命令行窗口（Shell）无法正常关闭
- 需要手动按Ctrl+C或强制关闭窗口
- Python进程可能残留在后台

### 原因分析

1. **音频流未正确关闭**: sounddevice音频流在异常退出时可能未被正确释放
2. **线程未正确终止**: 后台工作线程（如转录线程）可能仍在运行
3. **信号处理不完善**: 程序未正确处理系统信号（SIGINT、SIGTERM）
4. **资源清理不彻底**: 某些资源（如队列、缓冲区）未被清空

### 解决方案

项目已实施以下改进：

#### 1. 信号处理机制

```python
# 注册信号处理器
signal.signal(signal.SIGINT, self._signal_handler)
signal.signal(signal.SIGTERM, self._signal_handler)

def _signal_handler(self, signum, frame):
    """处理系统信号，优雅关闭"""
    print(f"\nReceived signal {signum}, shutting down...")
    self.cleanup()
    sys.exit(0)
```

#### 2. 退出时清理机制

```python
# 注册退出清理函数
atexit.register(self.cleanup)
self.app.aboutToQuit.connect(self.cleanup)
```

#### 3. 音频流强制关闭

```python
# 如果正常关闭失败，强制中止
try:
    self.stream.stop()
    self.stream.close()
except Exception as e:
    print(f"Warning: Error closing stream: {e}")
    try:
        self.stream.abort()  # 强制中止
    except:
        pass
```

#### 4. 队列清空

```python
# 清空音频队列，防止阻塞
while not self.audio_queue.empty():
    try:
        self.audio_queue.get_nowait()
    except queue.Empty:
        break
```

#### 5. QTimer处理Ctrl+C

```python
# 设置定时器让Qt事件循环能响应Ctrl+C
self.timer = QTimer()
self.timer.timeout.connect(lambda: None)
self.timer.start(500)
```

### 使用建议

#### 方式1: 使用调试脚本（推荐）

使用提供的 `run_debug.bat` 脚本运行程序：

```bash
run_debug.bat
```

该脚本会：
- 正确设置Python环境
- 运行程序
- 程序退出后自动清理残留进程
- 显示清理状态

#### 方式2: 直接运行

如果直接运行 `python main.py`：

**正常退出**:
1. 点击窗口的关闭按钮（✕）
2. 等待程序完成清理（约0.5秒）
3. Shell窗口会自动关闭

**强制退出**:
1. 在Shell窗口按 `Ctrl+C`
2. 程序会捕获信号并执行清理
3. 等待清理完成后退出

**如果窗口仍未关闭**:
1. 再次按 `Ctrl+C`
2. 或直接关闭Shell窗口
3. 使用任务管理器结束Python进程

### 开发建议

#### 1. 使用IDE调试

在IDE（如PyCharm、VS Code）中调试时：
- 使用IDE的停止按钮而不是直接关闭窗口
- IDE会发送正确的终止信号
- 程序能够正确执行清理流程

#### 2. 添加日志

在关键清理点添加日志输出：

```python
print("Stopping transcription worker...")
print("Closing audio stream...")
print("Cleanup complete")
```

这样可以看到清理进度，判断是否卡在某个步骤。

#### 3. 设置超时

为线程join操作设置超时：

```python
self.thread.join(timeout=2)  # 最多等待2秒
```

避免无限等待导致程序挂起。

#### 4. 使用daemon线程

对于不需要等待完成的线程，设置为daemon：

```python
self.thread = threading.Thread(target=self._process_audio, daemon=True)
```

daemon线程会在主程序退出时自动终止。

### 故障排除

#### 问题1: 按Ctrl+C无响应

**原因**: Qt事件循环阻塞了信号处理

**解决**: 
- 已添加QTimer定期触发事件循环
- 多按几次Ctrl+C
- 使用任务管理器强制结束

#### 问题2: 音频流无法关闭

**原因**: sounddevice底层驱动问题

**解决**:
- 程序已添加stream.abort()强制中止
- 检查音频驱动是否正常
- 重启音频服务

#### 问题3: 线程无法终止

**原因**: 线程可能在等待队列或I/O操作

**解决**:
- 设置队列超时: `queue.get(timeout=0.5)`
- 使用daemon线程
- 添加线程join超时

### 最佳实践

1. **总是使用try-finally**: 确保清理代码一定执行
2. **设置合理超时**: 避免无限等待
3. **使用daemon线程**: 对于后台任务
4. **注册清理函数**: 使用atexit和信号处理
5. **测试异常退出**: 确保各种退出方式都能正确清理

### 相关文件

- `main.py`: 主程序，包含信号处理和清理逻辑
- `audio_capture.py`: 音频捕获，包含流关闭逻辑
- `run_debug.bat`: 调试运行脚本
- `run.bat`: 正常运行脚本

### 参考资料

- [PyQt5 Signal Handling](https://doc.qt.io/qt-5/signalsandslots.html)
- [Python atexit Module](https://docs.python.org/3/library/atexit.html)
- [sounddevice Documentation](https://python-sounddevice.readthedocs.io/)
