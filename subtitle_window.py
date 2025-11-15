from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QApplication)
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
from config import Config


class SubtitleWindow(QWidget):
    """Floating subtitle window with modern UI"""
    
    # Signals
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.offset = QPoint()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Window properties
        self.setWindowTitle("AI实时字幕")
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        
        # Make window frameless and always on top
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        
        # Set window opacity
        self.setWindowOpacity(Config.WINDOW_OPACITY)
        
        # Set background color with transparency
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 220))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(10)
        
        # Control bar
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        
        # Title label
        self.title_label = QLabel("🎙️ AI实时字幕")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #00D9FF;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        control_layout.addWidget(self.title_label)
        
        control_layout.addStretch()
        
        # Status indicator
        self.status_label = QLabel("● 待机")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12px;
            }
        """)
        control_layout.addWidget(self.status_label)
        
        # Start button
        self.start_button = QPushButton("▶ 开始")
        self.start_button.setFixedSize(80, 30)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #00D9FF;
                color: #000000;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #00B8D4;
            }
            QPushButton:pressed {
                background-color: #0097A7;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        self.start_button.clicked.connect(self.on_start_clicked)
        control_layout.addWidget(self.start_button)
        
        # Stop button
        self.stop_button = QPushButton("■ 停止")
        self.stop_button.setFixedSize(80, 30)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5252;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E53935;
            }
            QPushButton:pressed {
                background-color: #C62828;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        self.stop_button.clicked.connect(self.on_stop_clicked)
        control_layout.addWidget(self.stop_button)
        
        # Settings button
        self.settings_button = QPushButton("⚙")
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #444444;
                border-radius: 5px;
            }
        """)
        self.settings_button.clicked.connect(self.on_settings_clicked)
        control_layout.addWidget(self.settings_button)
        
        # Close button
        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF5252;
                border-radius: 5px;
            }
        """)
        self.close_button.clicked.connect(self.close)
        control_layout.addWidget(self.close_button)
        
        main_layout.addLayout(control_layout)
        
        # Subtitle label
        self.subtitle_label = QLabel("等待音频输入...")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet(f"""
            QLabel {{
                color: #FFFFFF;
                font-size: {Config.FONT_SIZE}px;
                font-weight: bold;
                padding: 10px;
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
            }}
        """)
        main_layout.addWidget(self.subtitle_label, 1)
        
        self.setLayout(main_layout)
        
        # Auto-hide timer for subtitles
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.clear_subtitle)
        
    def on_start_clicked(self):
        """Handle start button click"""
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("● 录音中")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00FF00;
                font-size: 12px;
            }
        """)
        self.subtitle_label.setText("正在监听音频...")
        self.start_clicked.emit()
        
    def on_stop_clicked(self):
        """Handle stop button click"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("● 待机")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12px;
            }
        """)
        self.subtitle_label.setText("等待音频输入...")
        self.stop_clicked.emit()
    
    def on_settings_clicked(self):
        """Handle settings button click"""
        from settings_window import SettingsWindow
        settings_dialog = SettingsWindow(self)
        settings_dialog.exec_()
        
    def update_subtitle(self, text: str):
        """Update subtitle text"""
        if text and text.strip():
            self.subtitle_label.setText(text)
            # Auto-hide after 5 seconds
            self.hide_timer.stop()
            self.hide_timer.start(5000)
        
    def clear_subtitle(self):
        """Clear subtitle text"""
        self.subtitle_label.setText("正在监听音频...")
        
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.offset))
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
    def closeEvent(self, event):
        """Handle window close"""
        self.stop_clicked.emit()
        event.accept()
