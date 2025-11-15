# 如何打包 - 超简单指南

> 3步完成Windows应用打包

## 🎯 目标

将Python应用打包为Windows可执行文件（.exe），无需Python环境即可运行。

## 📋 前提条件

- ✅ Windows 10/11
- ✅ Python 3.8+ 已安装
- ✅ 项目代码完整

## 🚀 三步打包

### 第一步：安装打包工具

打开命令行，进入项目目录：

```bash
cd e:\project\LiteTool\ai_subtitle_tool
pip install -r build_requirements.txt
```

**等待安装完成**（约1-2分钟）

### 第二步：运行打包脚本

双击运行 `build.bat` 或在命令行执行：

```bash
build.bat
```

**等待打包完成**（约3-5分钟）

你会看到：
```
[1/5] 检查打包依赖... ✓
[2/5] 检查运行时依赖... ✓
[3/5] 清理旧的构建文件... ✓
[4/5] 开始打包应用... ✓
[5/5] 复制配置文件... ✓

✅ 打包完成！
输出目录: dist\AI实时字幕\
```

### 第三步：测试和使用

打包完成后：

```bash
# 进入输出目录
cd dist\AI实时字幕

# 运行程序
AI实时字幕.exe
```

## 🎁 创建便携版（可选）

如果要分发给其他人，创建便携版：

```bash
build_portable.bat
```

会生成：
- `AI实时字幕_便携版\` 文件夹
- `AI实时字幕_便携版.zip` 压缩包（可选）

## 📦 打包结果

### 文件结构

```
dist\AI实时字幕\
├── AI实时字幕.exe          # 主程序（双击运行）
├── _internal\              # 依赖库（自动加载）
├── .env.example            # 配置模板
├── README.md               # 使用文档
└── 使用说明.txt            # 快速说明
```

### 文件大小

- 未压缩: ~300-400 MB
- ZIP压缩: ~150-200 MB

## 🎮 如何使用打包后的程序

### 首次使用

1. **配置API密钥**
   ```bash
   # 复制配置模板
   copy .env.example .env
   
   # 编辑配置文件
   notepad .env
   ```

2. **填入API密钥**
   ```env
   AI_SERVICE=aliyun
   ALIYUN_API_KEY=sk-your-api-key-here
   ```

3. **启动程序**
   ```bash
   双击 AI实时字幕.exe
   ```

### 日常使用

直接双击 `AI实时字幕.exe` 即可！

## 🎨 自定义图标（可选）

想要自定义应用图标？

```bash
# 方法1: 自动生成
python create_icon.py

# 方法2: 使用自己的图标
# 将icon.ico放在项目根目录
```

然后重新运行 `build.bat`

## ❓ 常见问题

### Q1: 打包失败怎么办？

**A**: 清理后重试
```bash
rmdir /s /q build dist
pip install -r requirements.txt
pip install -r build_requirements.txt
build.bat
```

### Q2: 程序无法启动？

**A**: 检查是否缺少运行库
- 下载安装 [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Q3: 杀毒软件报毒？

**A**: 这是误报
- 添加到白名单
- 或暂时关闭杀毒软件

### Q4: 文件太大？

**A**: 使用虚拟环境打包
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
build.bat
```

## 📤 如何分发

### 方式1: 直接分享文件夹

压缩 `dist\AI实时字幕\` 文件夹为ZIP，发送给朋友。

### 方式2: 使用便携版

```bash
build_portable.bat
```

分享生成的 `AI实时字幕_便携版.zip`

### 方式3: 网盘分享

1. 上传ZIP到网盘
2. 分享下载链接
3. 附上使用说明

## 🎯 快速命令参考

```bash
# 安装打包工具
pip install -r build_requirements.txt

# 标准打包
build.bat

# 便携版打包
build_portable.bat

# 清理构建文件
rmdir /s /q build dist

# 测试程序
cd dist\AI实时字幕
AI实时字幕.exe
```

## 📚 需要更多帮助？

- **快速指南**: [PACKAGE_QUICKSTART.md](PACKAGE_QUICKSTART.md)
- **详细文档**: [BUILD_GUIDE.md](BUILD_GUIDE.md)
- **完整指南**: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)

## ✅ 检查清单

打包前检查：
- [ ] Python环境正常
- [ ] 所有依赖已安装
- [ ] 代码无错误
- [ ] 配置文件完整

打包后检查：
- [ ] 程序能启动
- [ ] UI显示正常
- [ ] 功能工作正常
- [ ] 配置文件存在

分发前检查：
- [ ] 在其他电脑测试
- [ ] 文档齐全
- [ ] 使用说明清晰
- [ ] 压缩包完整

## 🎉 完成！

现在你已经学会了如何打包Windows应用！

**下一步**:
1. 测试打包的程序
2. 分享给朋友使用
3. 收集反馈改进

**祝你打包顺利！** 🚀

---

**提示**: 第一次打包可能需要较长时间，请耐心等待。后续打包会快很多！
