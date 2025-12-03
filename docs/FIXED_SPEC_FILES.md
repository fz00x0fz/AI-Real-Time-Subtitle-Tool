# Spec文件修复说明

## 🐛 问题

打包时出现错误：
```
Unable to find 'E:\project\LiteTool\ai_subtitle_tool\QUICKSTART_ALIYUN.md' when adding binary and data files.
```

## 🔍 原因

之前将所有md文档移动到了`docs`目录，但spec文件和build脚本仍然引用旧路径。

## ✅ 已修复的文件

### 1. **ai_subtitle.spec**
- ❌ 移除：`QUICKSTART_ALIYUN.md`（已移动到docs）
- ✅ 添加：`README_EN.md`
- ✅ 添加：`LICENSE`
- ✅ 保留：`docs` 目录（包含所有文档）

### 2. **ai_subtitle_with_whisper.spec**
- ❌ 移除：`QUICKSTART_ALIYUN.md`（已移动到docs）
- ✅ 添加：`README_EN.md`
- ✅ 添加：`LICENSE`
- ✅ 保留：`docs` 目录（包含所有文档）

### 3. **build.bat**
- ❌ 移除：复制`QUICKSTART_ALIYUN.md`
- ✅ 添加：复制`README_EN.md`
- ✅ 添加：复制`LICENSE`
- ✅ 添加：复制`docs`目录
- ✅ 更新：使用说明中的文档路径

### 4. **build_with_whisper.bat**
- ❌ 移除：复制多个已移动的md文件
- ✅ 添加：复制`README_EN.md`
- ✅ 添加：复制`LICENSE`
- ✅ 简化：只复制`docs`目录（包含所有文档）

### 5. **build_portable.bat**
- ✅ 更新：文档路径引用

## 📦 打包文件结构

### 标准版 (dist/AI实时字幕/)
```
AI实时字幕/
├── AI实时字幕.exe
├── .env.example
├── .env.aliyun.example
├── README.md
├── README_EN.md
├── LICENSE
├── docs/
│   ├── QUICKSTART_ALIYUN.md
│   ├── AUDIO_SETUP.md
│   ├── SETTINGS_GUIDE.md
│   └── ... (所有其他文档)
└── 使用说明.txt
```

### 本地模型版 (dist/AI实时字幕_本地模型版/)
```
AI实时字幕_本地模型版/
├── AI实时字幕_本地模型版.exe
├── .env.example
├── .env.aliyun.example
├── README.md
├── README_EN.md
├── LICENSE
├── docs/
│   └── ... (所有文档)
└── 使用说明_本地模型版.txt
```

## 🚀 现在可以打包了

### 标准版
```bash
build.bat
```

### 本地模型版
```bash
build_with_whisper.bat
```

### 便携版
```bash
build_portable.bat
```

## ✅ 验证

打包完成后，检查：
1. ✅ dist目录中有README.md、README_EN.md、LICENSE
2. ✅ dist目录中有docs文件夹
3. ✅ docs文件夹包含所有md文档
4. ✅ 应用可以正常启动

## 📝 注意事项

### 文档组织
- **根目录**：只保留README.md、README_EN.md、LICENSE
- **docs目录**：包含所有其他文档
- **spec文件**：引用docs目录，自动包含所有文档
- **build脚本**：复制docs目录，不需要单独复制每个文档

### 优势
- ✅ 文档集中管理
- ✅ 打包配置简化
- ✅ 易于维护
- ✅ 结构清晰

---

**修复完成！** 现在可以正常打包了。🎉
