"""
Whisper本地模型安装器
在运行时检测和安装openai-whisper包
"""
import subprocess
import sys
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QTextEdit, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont


class WhisperInstallThread(QThread):
    """Whisper安装线程"""
    progress = pyqtSignal(str)  # 进度信息
    finished = pyqtSignal(bool, str)  # 完成信号(成功, 消息)
    
    def run(self):
        """执行安装"""
        try:
            self.progress.emit("正在检查pip...")
            
            # 升级pip
            self.progress.emit("升级pip到最新版本...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    encoding='utf-8',
                    errors='ignore'
                )
            except Exception:
                # 升级失败不影响后续安装
                pass
            
            # 安装openai-whisper
            self.progress.emit("正在安装openai-whisper...")
            self.progress.emit("这可能需要几分钟时间，请耐心等待...")
            
            # 不使用encoding参数，以字节模式读取，避免编码问题
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "openai-whisper"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                # 不指定encoding，以字节模式读取
            )
            
            # 实时输出安装信息
            try:
                for line in iter(process.stdout.readline, b''):
                    if not line:
                        break
                    try:
                        # 手动解码，使用多种编码尝试
                        decoded_line = None
                        for enc in ['utf-8', 'gbk', 'gb2312', 'ascii']:
                            try:
                                decoded_line = line.decode(enc, errors='ignore').strip()
                                if decoded_line:
                                    break
                            except:
                                continue
                        
                        if decoded_line:
                            # 再次确保可以用GBK编码（用于PyQt信号）
                            safe_line = decoded_line.encode('ascii', errors='ignore').decode('ascii')
                            if safe_line.strip():
                                self.progress.emit(safe_line)
                    except Exception:
                        # 忽略单行输出错误
                        pass
            except Exception as e:
                self.progress.emit(f"读取输出时出错: {str(e)}")
            
            process.wait()
            
            if process.returncode == 0:
                self.progress.emit("\n[OK] 安装成功！")
                self.progress.emit("正在验证安装...")
                
                # 验证安装
                try:
                    import whisper
                    self.progress.emit("[OK] Whisper模块验证成功")
                    self.finished.emit(True, "安装完成！重启应用后即可使用本地Whisper模型。")
                except ImportError as e:
                    self.finished.emit(False, f"安装完成但验证失败: {e}")
            else:
                self.finished.emit(False, "安装失败，请查看详细信息")
                
        except Exception as e:
            self.progress.emit(f"\n[ERROR] 错误: {str(e)}")
            self.finished.emit(False, f"安装失败: {str(e)}")


class WhisperInstallerDialog(QDialog):
    """Whisper安装对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("安装本地Whisper模型")
        self.setModal(True)
        self.resize(600, 450)
        self.install_thread = None
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 标题
        title = QLabel("本地Whisper模型安装")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 说明文本
        info_text = QLabel(
            "本地Whisper模型可以让您在离线环境下使用语音识别功能。\n\n"
            "安装内容:\n"
            "• openai-whisper 包 (约50MB)\n"
            "• 首次使用时会自动下载模型文件 (base模型约74MB)\n\n"
            "系统要求:\n"
            "• 至少2GB可用磁盘空间\n"
            "• 稳定的网络连接 (仅安装时需要)\n"
            "• Python 3.8 或更高版本\n\n"
            "注意: 安装过程可能需要3-5分钟"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_text)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 日志输出
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setVisible(False)
        self.log_text.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas;")
        layout.addWidget(self.log_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.install_btn = QPushButton("开始安装")
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.install_btn.clicked.connect(self.start_install)
        button_layout.addWidget(self.install_btn)
        
        self.close_btn = QPushButton("取消")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ccc;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.close_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def start_install(self):
        """开始安装"""
        # 显示进度条和日志
        self.progress_bar.setVisible(True)
        self.log_text.setVisible(True)
        self.log_text.clear()
        
        # 禁用按钮
        self.install_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        
        # 创建并启动安装线程
        self.install_thread = WhisperInstallThread()
        self.install_thread.progress.connect(self.on_progress)
        self.install_thread.finished.connect(self.on_finished)
        self.install_thread.start()
    
    def on_progress(self, message):
        """更新进度"""
        try:
            # 只保留ASCII字符，彻底避免编码问题
            safe_message = str(message)
            
            # 转换为纯ASCII
            ascii_message = safe_message.encode('ascii', errors='ignore').decode('ascii').strip()
            
            # 如果清理后为空，跳过
            if ascii_message:
                self.log_text.append(ascii_message)
                # 自动滚动到底部
                self.log_text.verticalScrollBar().setValue(
                    self.log_text.verticalScrollBar().maximum()
                )
        except Exception:
            # 静默失败
            pass
    
    def on_finished(self, success, message):
        """安装完成"""
        self.progress_bar.setVisible(False)
        self.close_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(
                self,
                "安装成功",
                message + "\n\n请重启应用以使用本地Whisper模型。"
            )
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "安装失败",
                message + "\n\n请查看日志了解详细信息。"
            )
            self.install_btn.setEnabled(True)


def check_whisper_available():
    """检查Whisper是否可用"""
    try:
        import whisper
        return True
    except ImportError:
        return False


def show_whisper_installer(parent=None):
    """显示Whisper安装对话框"""
    dialog = WhisperInstallerDialog(parent)
    return dialog.exec_() == QDialog.Accepted


if __name__ == "__main__":
    """测试安装器"""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    if check_whisper_available():
        QMessageBox.information(None, "提示", "Whisper已安装")
    else:
        show_whisper_installer()
    
    sys.exit(0)
