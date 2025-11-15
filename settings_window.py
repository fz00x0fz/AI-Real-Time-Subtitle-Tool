"""
配置窗口模块
提供图形化界面配置应用参数
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QGroupBox, QFormLayout, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os
from typing import Dict, Any


class SettingsWindow(QDialog):
    """配置窗口"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # 配置数据
        self.config_data = {}
        
        # 初始化UI
        self.init_ui()
        
        # 加载当前配置
        self.load_config()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # AI服务配置
        self.ai_tab = self.create_ai_tab()
        self.tabs.addTab(self.ai_tab, "AI服务")
        
        # 音频配置
        self.audio_tab = self.create_audio_tab()
        self.tabs.addTab(self.audio_tab, "音频设置")
        
        # UI配置
        self.ui_tab = self.create_ui_tab()
        self.tabs.addTab(self.ui_tab, "界面设置")
        
        layout.addWidget(self.tabs)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.test_btn = QPushButton("测试连接")
        self.test_btn.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_btn)
        
        button_layout.addStretch()
        
        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_config)
        self.save_btn.setDefault(True)
        button_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_ai_tab(self) -> QWidget:
        """创建AI服务配置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # AI服务选择
        service_group = QGroupBox("AI服务选择")
        service_layout = QFormLayout()
        
        self.ai_service = QComboBox()
        self.ai_service.addItems([
            "aliyun - 阿里云百炼（推荐）",
            "openai - OpenAI Whisper",
            "azure - Azure Speech",
            "local_whisper - 本地Whisper"
        ])
        self.ai_service.currentIndexChanged.connect(self.on_service_changed)
        service_layout.addRow("服务类型:", self.ai_service)
        
        # 本地Whisper安装提示
        whisper_layout = QHBoxLayout()
        self.whisper_status = QLabel()
        whisper_layout.addWidget(self.whisper_status)
        
        self.install_whisper_btn = QPushButton("安装本地模型")
        self.install_whisper_btn.setMaximumWidth(120)
        self.install_whisper_btn.clicked.connect(self.install_whisper)
        whisper_layout.addWidget(self.install_whisper_btn)
        whisper_layout.addStretch()
        
        # 更新状态（在按钮创建之后）
        self.update_whisper_status()
        
        service_layout.addRow("", whisper_layout)
        
        service_group.setLayout(service_layout)
        layout.addWidget(service_group)
        
        # 阿里云配置
        self.aliyun_group = QGroupBox("阿里云百炼配置")
        aliyun_layout = QFormLayout()
        
        self.aliyun_api_key = QLineEdit()
        self.aliyun_api_key.setPlaceholderText("sk-xxxxxxxxxxxxxxxx")
        self.aliyun_api_key.setEchoMode(QLineEdit.Password)
        aliyun_layout.addRow("API Key*:", self.aliyun_api_key)
        
        self.show_aliyun_key = QCheckBox("显示密钥")
        self.show_aliyun_key.stateChanged.connect(
            lambda: self.toggle_password(self.aliyun_api_key, self.show_aliyun_key)
        )
        aliyun_layout.addRow("", self.show_aliyun_key)
        
        self.aliyun_app_id = QLineEdit()
        self.aliyun_app_id.setPlaceholderText("可选，留空使用默认")
        aliyun_layout.addRow("App ID:", self.aliyun_app_id)
        
        self.aliyun_model = QComboBox()
        self.aliyun_model.addItems([
            "paraformer-realtime-v2 - 实时识别（推荐）",
            "paraformer-v2 - 高精度识别",
            "paraformer-8k-v2 - 8kHz采样率",
            "paraformer-mtl-v2 - 多语言"
        ])
        aliyun_layout.addRow("模型:", self.aliyun_model)
        
        self.aliyun_endpoint = QLineEdit()
        self.aliyun_endpoint.setText("https://dashscope.aliyuncs.com/api/v1/services/audio/asr")
        aliyun_layout.addRow("端点:", self.aliyun_endpoint)
        
        # 添加获取密钥链接
        help_label = QLabel('<a href="https://dashscope.aliyun.com/">点击获取API Key</a>')
        help_label.setOpenExternalLinks(True)
        aliyun_layout.addRow("", help_label)
        
        self.aliyun_group.setLayout(aliyun_layout)
        layout.addWidget(self.aliyun_group)
        
        # OpenAI配置
        self.openai_group = QGroupBox("OpenAI配置")
        openai_layout = QFormLayout()
        
        self.openai_api_key = QLineEdit()
        self.openai_api_key.setPlaceholderText("sk-xxxxxxxxxxxxxxxx")
        self.openai_api_key.setEchoMode(QLineEdit.Password)
        openai_layout.addRow("API Key*:", self.openai_api_key)
        
        self.show_openai_key = QCheckBox("显示密钥")
        self.show_openai_key.stateChanged.connect(
            lambda: self.toggle_password(self.openai_api_key, self.show_openai_key)
        )
        openai_layout.addRow("", self.show_openai_key)
        
        self.openai_model = QComboBox()
        self.openai_model.addItems(["whisper-1"])
        openai_layout.addRow("模型:", self.openai_model)
        
        help_label = QLabel('<a href="https://platform.openai.com/api-keys">点击获取API Key</a>')
        help_label.setOpenExternalLinks(True)
        openai_layout.addRow("", help_label)
        
        self.openai_group.setLayout(openai_layout)
        layout.addWidget(self.openai_group)
        
        # Azure配置
        self.azure_group = QGroupBox("Azure Speech配置")
        azure_layout = QFormLayout()
        
        self.azure_speech_key = QLineEdit()
        self.azure_speech_key.setPlaceholderText("xxxxxxxxxxxxxxxx")
        self.azure_speech_key.setEchoMode(QLineEdit.Password)
        azure_layout.addRow("Speech Key*:", self.azure_speech_key)
        
        self.show_azure_key = QCheckBox("显示密钥")
        self.show_azure_key.stateChanged.connect(
            lambda: self.toggle_password(self.azure_speech_key, self.show_azure_key)
        )
        azure_layout.addRow("", self.show_azure_key)
        
        self.azure_speech_region = QLineEdit()
        self.azure_speech_region.setPlaceholderText("eastus")
        azure_layout.addRow("区域*:", self.azure_speech_region)
        
        help_label = QLabel('<a href="https://portal.azure.com/">点击获取密钥</a>')
        help_label.setOpenExternalLinks(True)
        azure_layout.addRow("", help_label)
        
        self.azure_group.setLayout(azure_layout)
        layout.addWidget(self.azure_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        return widget
    
    def create_audio_tab(self) -> QWidget:
        """创建音频配置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 音频参数
        audio_group = QGroupBox("音频参数")
        audio_layout = QFormLayout()
        
        self.sample_rate = QComboBox()
        self.sample_rate.addItems(["8000", "16000", "22050", "44100", "48000"])
        self.sample_rate.setCurrentText("16000")
        audio_layout.addRow("采样率 (Hz):", self.sample_rate)
        
        self.chunk_duration = QSpinBox()
        self.chunk_duration.setRange(1, 10)
        self.chunk_duration.setValue(3)
        self.chunk_duration.setSuffix(" 秒")
        audio_layout.addRow("音频块时长:", self.chunk_duration)
        
        self.audio_device_index = QSpinBox()
        self.audio_device_index.setRange(-1, 99)
        self.audio_device_index.setValue(-1)
        self.audio_device_index.setSpecialValueText("自动选择")
        audio_layout.addRow("音频设备索引:", self.audio_device_index)
        
        # 添加设备列表按钮
        device_btn = QPushButton("查看可用设备")
        device_btn.clicked.connect(self.show_audio_devices)
        audio_layout.addRow("", device_btn)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        
        # 音频说明
        info_group = QGroupBox("说明")
        info_layout = QVBoxLayout()
        
        info_text = QLabel(
            "• 采样率: 建议使用16000Hz，适合语音识别\n"
            "• 音频块时长: 2-4秒平衡延迟和准确率\n"
            "• 设备索引: -1为自动选择，或手动指定设备\n"
            "• 需要启用Windows的\"立体声混音\"功能"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        return widget
    
    def create_ui_tab(self) -> QWidget:
        """创建UI配置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 窗口设置
        window_group = QGroupBox("窗口设置")
        window_layout = QFormLayout()
        
        self.window_width = QSpinBox()
        self.window_width.setRange(400, 2000)
        self.window_width.setValue(800)
        self.window_width.setSuffix(" px")
        window_layout.addRow("窗口宽度:", self.window_width)
        
        self.window_height = QSpinBox()
        self.window_height.setRange(80, 500)
        self.window_height.setValue(120)
        self.window_height.setSuffix(" px")
        window_layout.addRow("窗口高度:", self.window_height)
        
        self.window_opacity = QDoubleSpinBox()
        self.window_opacity.setRange(0.1, 1.0)
        self.window_opacity.setValue(0.85)
        self.window_opacity.setSingleStep(0.05)
        window_layout.addRow("窗口透明度:", self.window_opacity)
        
        window_group.setLayout(window_layout)
        layout.addWidget(window_group)
        
        # 字体设置
        font_group = QGroupBox("字体设置")
        font_layout = QFormLayout()
        
        self.font_size = QSpinBox()
        self.font_size.setRange(12, 72)
        self.font_size.setValue(24)
        self.font_size.setSuffix(" pt")
        font_layout.addRow("字体大小:", self.font_size)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # 预览
        preview_group = QGroupBox("预览")
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel("这是字幕预览效果")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 180); "
            "color: white; "
            "padding: 10px; "
            "border-radius: 5px;"
        )
        preview_layout.addWidget(self.preview_label)
        
        # 连接信号更新预览
        self.font_size.valueChanged.connect(self.update_preview)
        self.window_opacity.valueChanged.connect(self.update_preview)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        return widget
    
    def toggle_password(self, line_edit: QLineEdit, checkbox: QCheckBox):
        """切换密码显示/隐藏"""
        if checkbox.isChecked():
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)
    
    def on_service_changed(self, index: int):
        """AI服务改变时的处理"""
        service = self.ai_service.currentText().split(" - ")[0]
        
        # 显示/隐藏对应的配置组
        self.aliyun_group.setVisible(service == "aliyun")
        self.openai_group.setVisible(service == "openai")
        self.azure_group.setVisible(service == "azure")
    
    def update_preview(self):
        """更新预览效果"""
        font_size = self.font_size.value()
        opacity = self.window_opacity.value()
        
        font = QFont("Microsoft YaHei", font_size)
        self.preview_label.setFont(font)
        
        alpha = int(180 * opacity)
        self.preview_label.setStyleSheet(
            f"background-color: rgba(0, 0, 0, {alpha}); "
            "color: white; "
            "padding: 10px; "
            "border-radius: 5px;"
        )
    
    def show_audio_devices(self):
        """显示可用音频设备"""
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            
            device_list = "可用音频设备:\n\n"
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    device_list += f"[{i}] {device['name']}\n"
            
            QMessageBox.information(self, "音频设备", device_list)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法获取音频设备列表:\n{e}")
    
    def load_config(self):
        """加载当前配置"""
        env_file = '.env'
        if not os.path.exists(env_file):
            env_file = '.env.example'
        
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.config_data[key.strip()] = value.strip()
        
        # 应用配置到UI
        self.apply_config_to_ui()
    
    def apply_config_to_ui(self):
        """将配置应用到UI"""
        # AI服务
        service = self.config_data.get('AI_SERVICE', 'aliyun')
        service_map = {
            'aliyun': 0,
            'openai': 1,
            'azure': 2,
            'local_whisper': 3
        }
        self.ai_service.setCurrentIndex(service_map.get(service, 0))
        
        # 阿里云
        self.aliyun_api_key.setText(self.config_data.get('ALIYUN_API_KEY', ''))
        self.aliyun_app_id.setText(self.config_data.get('ALIYUN_APP_ID', ''))
        
        model = self.config_data.get('ALIYUN_MODEL', 'paraformer-realtime-v2')
        model_map = {
            'paraformer-realtime-v2': 0,
            'paraformer-v2': 1,
            'paraformer-8k-v2': 2,
            'paraformer-mtl-v2': 3
        }
        self.aliyun_model.setCurrentIndex(model_map.get(model, 0))
        self.aliyun_endpoint.setText(
            self.config_data.get('ALIYUN_ENDPOINT', 
            'https://dashscope.aliyuncs.com/api/v1/services/audio/asr')
        )
        
        # OpenAI
        self.openai_api_key.setText(self.config_data.get('OPENAI_API_KEY', ''))
        
        # Azure
        self.azure_speech_key.setText(self.config_data.get('AZURE_SPEECH_KEY', ''))
        self.azure_speech_region.setText(self.config_data.get('AZURE_SPEECH_REGION', ''))
        
        # 音频
        self.sample_rate.setCurrentText(self.config_data.get('SAMPLE_RATE', '16000'))
        self.chunk_duration.setValue(int(self.config_data.get('CHUNK_DURATION', '3')))
        self.audio_device_index.setValue(int(self.config_data.get('AUDIO_DEVICE_INDEX', '-1')))
        
        # UI
        self.window_width.setValue(int(self.config_data.get('WINDOW_WIDTH', '800')))
        self.window_height.setValue(int(self.config_data.get('WINDOW_HEIGHT', '120')))
        self.window_opacity.setValue(float(self.config_data.get('WINDOW_OPACITY', '0.85')))
        self.font_size.setValue(int(self.config_data.get('FONT_SIZE', '24')))
        
        # 更新预览
        self.update_preview()
    
    def get_config_from_ui(self) -> Dict[str, str]:
        """从UI获取配置"""
        config = {}
        
        # AI服务
        service = self.ai_service.currentText().split(" - ")[0]
        config['AI_SERVICE'] = service
        
        # 阿里云
        config['ALIYUN_API_KEY'] = self.aliyun_api_key.text().strip()
        config['ALIYUN_APP_ID'] = self.aliyun_app_id.text().strip()
        config['ALIYUN_MODEL'] = self.aliyun_model.currentText().split(" - ")[0]
        config['ALIYUN_ENDPOINT'] = self.aliyun_endpoint.text().strip()
        
        # OpenAI
        config['OPENAI_API_KEY'] = self.openai_api_key.text().strip()
        config['OPENAI_MODEL'] = self.openai_model.currentText()
        
        # Azure
        config['AZURE_SPEECH_KEY'] = self.azure_speech_key.text().strip()
        config['AZURE_SPEECH_REGION'] = self.azure_speech_region.text().strip()
        
        # 音频
        config['SAMPLE_RATE'] = self.sample_rate.currentText()
        config['CHUNK_DURATION'] = str(self.chunk_duration.value())
        config['AUDIO_DEVICE_INDEX'] = str(self.audio_device_index.value())
        
        # UI
        config['WINDOW_WIDTH'] = str(self.window_width.value())
        config['WINDOW_HEIGHT'] = str(self.window_height.value())
        config['WINDOW_OPACITY'] = str(self.window_opacity.value())
        config['FONT_SIZE'] = str(self.font_size.value())
        
        return config
    
    def validate_config(self) -> bool:
        """验证配置"""
        service = self.ai_service.currentText().split(" - ")[0]
        
        if service == 'aliyun':
            if not self.aliyun_api_key.text().strip():
                QMessageBox.warning(self, "配置错误", "请填写阿里云API Key")
                self.tabs.setCurrentIndex(0)
                self.aliyun_api_key.setFocus()
                return False
        
        elif service == 'openai':
            if not self.openai_api_key.text().strip():
                QMessageBox.warning(self, "配置错误", "请填写OpenAI API Key")
                self.tabs.setCurrentIndex(0)
                self.openai_api_key.setFocus()
                return False
        
        elif service == 'azure':
            if not self.azure_speech_key.text().strip():
                QMessageBox.warning(self, "配置错误", "请填写Azure Speech Key")
                self.tabs.setCurrentIndex(0)
                self.azure_speech_key.setFocus()
                return False
            if not self.azure_speech_region.text().strip():
                QMessageBox.warning(self, "配置错误", "请填写Azure区域")
                self.tabs.setCurrentIndex(0)
                self.azure_speech_region.setFocus()
                return False
        
        return True
    
    def save_config(self):
        """保存配置"""
        if not self.validate_config():
            return
        
        config = self.get_config_from_ui()
        
        # 写入.env文件
        try:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write("# AI实时字幕工具配置文件\n")
                f.write("# 由配置界面自动生成\n\n")
                
                f.write("# ===== AI服务配置 =====\n")
                f.write(f"AI_SERVICE={config['AI_SERVICE']}\n\n")
                
                f.write("# ===== 阿里云百炼配置 =====\n")
                f.write(f"ALIYUN_API_KEY={config['ALIYUN_API_KEY']}\n")
                f.write(f"ALIYUN_APP_ID={config['ALIYUN_APP_ID']}\n")
                f.write(f"ALIYUN_ENDPOINT={config['ALIYUN_ENDPOINT']}\n")
                f.write(f"ALIYUN_MODEL={config['ALIYUN_MODEL']}\n\n")
                
                f.write("# ===== OpenAI配置 =====\n")
                f.write(f"OPENAI_API_KEY={config['OPENAI_API_KEY']}\n")
                f.write(f"OPENAI_MODEL={config['OPENAI_MODEL']}\n\n")
                
                f.write("# ===== Azure配置 =====\n")
                f.write(f"AZURE_SPEECH_KEY={config['AZURE_SPEECH_KEY']}\n")
                f.write(f"AZURE_SPEECH_REGION={config['AZURE_SPEECH_REGION']}\n\n")
                
                f.write("# ===== 音频设置 =====\n")
                f.write(f"SAMPLE_RATE={config['SAMPLE_RATE']}\n")
                f.write(f"CHUNK_DURATION={config['CHUNK_DURATION']}\n")
                f.write(f"AUDIO_DEVICE_INDEX={config['AUDIO_DEVICE_INDEX']}\n\n")
                
                f.write("# ===== UI设置 =====\n")
                f.write(f"WINDOW_WIDTH={config['WINDOW_WIDTH']}\n")
                f.write(f"WINDOW_HEIGHT={config['WINDOW_HEIGHT']}\n")
                f.write(f"WINDOW_OPACITY={config['WINDOW_OPACITY']}\n")
                f.write(f"FONT_SIZE={config['FONT_SIZE']}\n")
            
            QMessageBox.information(
                self, 
                "保存成功", 
                "配置已保存到 .env 文件\n\n请重启应用使配置生效"
            )
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"无法保存配置:\n{e}")
    
    def update_whisper_status(self):
        """更新Whisper安装状态"""
        try:
            # 检查按钮是否已创建
            if not hasattr(self, 'install_whisper_btn'):
                return
            
            # 尝试导入whisper
            try:
                import whisper
                self.whisper_status.setText("✅ 本地模型已安装")
                self.whisper_status.setStyleSheet("color: green;")
                self.install_whisper_btn.setText("重新安装")
            except ImportError:
                self.whisper_status.setText("⚠️ 本地模型未安装")
                self.whisper_status.setStyleSheet("color: orange;")
                self.install_whisper_btn.setText("安装本地模型")
        except Exception as e:
            # 静默处理错误，避免影响主程序
            print(f"更新Whisper状态时出错: {e}")
    
    def install_whisper(self):
        """安装Whisper模型"""
        try:
            from whisper_installer import show_whisper_installer
            
            if show_whisper_installer(self):
                # 安装成功，更新状态
                self.update_whisper_status()
                QMessageBox.information(
                    self,
                    "安装成功",
                    "本地Whisper模型安装成功！\n\n"
                    "请重启应用后在AI服务中选择\"本地Whisper\"即可使用。"
                )
        except ImportError as e:
            QMessageBox.critical(
                self,
                "功能不可用",
                f"无法加载安装器模块。\n\n"
                f"请手动安装:\n"
                f"pip install openai-whisper\n\n"
                f"错误详情: {e}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "安装失败",
                f"安装过程中出现错误:\n{e}"
            )
    
    def test_connection(self):
        """测试AI服务连接"""
        if not self.validate_config():
            return
        
        service = self.ai_service.currentText().split(" - ")[0]
        
        QMessageBox.information(
            self,
            "测试连接",
            f"正在测试 {service} 服务连接...\n\n"
            "此功能需要实现具体的测试逻辑。\n"
            "建议保存配置后使用主程序测试。"
        )
