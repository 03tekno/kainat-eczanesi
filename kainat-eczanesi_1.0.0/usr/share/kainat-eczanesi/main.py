import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QListWidget, QLabel, 
                             QFrame, QSplitter, QScrollArea, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QScreen

class KainatEczanesi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kainat Eczanesi")
        # İlk açılış artık Açık Mod (False = Light)
        self.is_dark = False 
        self.data = []
        self.load_all_data()
        
        # Ekranın %70'ı
        self.adjust_window_size(0.7)
        
        self.init_ui()
        self.apply_theme()

    def adjust_window_size(self, ratio):
        screen = QApplication.primaryScreen().geometry()
        width = int(screen.width() * ratio)
        height = int(screen.height() * ratio)
        self.setMinimumSize(900, 600)
        self.resize(width, height)
        qr = self.frameGeometry()
        qr.moveCenter(screen.center())
        self.move(qr.topLeft())

    def load_all_data(self):
        files = [f for f in os.listdir('.') if f.endswith('.json')]
        for file in sorted(files):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    self.data.extend(content.get('icerik', []))
            except Exception: pass

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- ÜST BAR ---
        self.top_bar = QFrame()
        self.top_bar.setObjectName("topBar")
        self.top_bar.setFixedHeight(55)
        top_layout = QHBoxLayout(self.top_bar)
        
        self.brand_label = QLabel("🌿 KAINAT ECZANESI")
        self.brand_label.setObjectName("brandLabel")
        
        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(120, 32)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)

        top_layout.addWidget(self.brand_label)
        top_layout.addStretch()
        top_layout.addWidget(self.theme_btn)

        # --- ANA GÖVDE ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)

        # Genişletilmiş Sol Sidebar
        left_widget = QWidget()
        left_widget.setObjectName("sidePanel")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Bitki veya fayda ara...")
        self.search_bar.setFixedHeight(40)
        self.search_bar.textChanged.connect(self.filter_list)
        
        self.list_widget = QListWidget()
        # Yatay kaydırmayı engelle ve metni sığdır
        self.list_widget.setWordWrap(True)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_widget.currentRowChanged.connect(self.display_details)
        
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(self.list_widget)

        # Detay Alanı
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setObjectName("contentArea")
        
        content_container = QWidget()
        content_container.setObjectName("contentContainer")
        self.detail_layout = QVBoxLayout(content_container)
        self.detail_layout.setContentsMargins(45, 40, 45, 40)
        self.detail_layout.setSpacing(20)

        self.title_label = QLabel("Şifa Rehberi")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setWordWrap(True)
        
        self.type_badge = QLabel("")
        self.type_badge.setObjectName("typeBadge")
        self.type_badge.hide()

        self.info_text = QLabel("Başlamak için sol menüden bir bitki seçebilirsiniz.")
        self.info_text.setWordWrap(True)
        self.info_text.setObjectName("infoText")

        self.detail_layout.addWidget(self.title_label)
        self.detail_layout.addWidget(self.type_badge)
        self.detail_layout.addWidget(self.info_text)
        self.detail_layout.addStretch()

        self.content_area.setWidget(content_container)

        splitter.addWidget(left_widget)
        splitter.addWidget(self.content_area)
        # Sol tarafı daha geniş başlatalım (Örn: %30 sol, %70 sağ)
        splitter.setSizes([300, 700]) 

        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(splitter)
        self.update_list(self.data)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def apply_theme(self):
        self.theme_btn.setText("🌙 Karanlık Mod" if not self.is_dark else "☀️ Aydınlık Mod")
        
        if self.is_dark:
            colors = {"bg": "#0f0f0f", "side": "#1a1a1a", "text": "#ffffff", "mute": "#bbb", "accent": "#4caf50", "border": "#333", "input": "#252525"}
        else:
            # Aydınlık Mod Renkleri
            colors = {"bg": "#ffffff", "side": "#f0f2f5", "text": "#1c1e21", "mute": "#606770", "accent": "#2e7d32", "border": "#ddd", "input": "#ffffff"}

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {colors['bg']}; }}
            #topBar {{ background-color: {colors['side']}; border-bottom: 1px solid {colors['border']}; }}
            #sidePanel {{ background-color: {colors['side']}; border-right: 1px solid {colors['border']}; }}
            #contentArea, #contentContainer {{ background-color: {colors['bg']}; border: none; }}
            
            #brandLabel {{ color: {colors['accent']}; font-weight: bold; font-size: 16px; letter-spacing: 1px; }}
            
            QPushButton {{ 
                background-color: {colors['accent']}; color: white; border-radius: 6px; 
                font-weight: bold; font-size: 12px; border: none;
            }}
            
            QLineEdit {{ 
                padding: 10px; border: 2px solid {colors['border']}; border-radius: 10px; 
                background: {colors['input']}; color: {colors['text']}; font-size: 14px;
            }}
            QLineEdit:focus {{ border: 2px solid {colors['accent']}; }}

            QListWidget {{ 
                border: none; background: transparent; color: {colors['text']}; 
                outline: none; font-size: 16px; /* Menü metinleri büyütüldü */
            }}
            QListWidget::item {{ 
                padding: 15px; border-radius: 10px; margin-bottom: 5px; border-bottom: 1px solid {colors['border']}33;
            }}
            QListWidget::item:selected {{ background: {colors['accent']}; color: white; font-weight: bold; }}
            QListWidget::item:hover:!selected {{ background: {colors['border']}; }}

            #titleLabel {{ font-size: 40px; color: {colors['text']}; font-weight: 800; }}
            #infoText {{ font-size: 18px; color: {colors['mute']}; line-height: 160%; }}
            
            #typeBadge {{ 
                background-color: {colors['accent']}22; color: {colors['accent']}; 
                padding: 6px 15px; border-radius: 8px; border: 1px solid {colors['accent']};
                font-weight: bold; font-size: 12px; max-width: 140px;
            }}
        """)

    def update_list(self, items):
        self.list_widget.clear()
        for item in items: self.list_widget.addItem(item['isim'])

    def filter_list(self):
        text = self.search_bar.text().lower()
        filtered = [i for i in self.data if text in i['isim'].lower() or text in i['faydalar'].lower()]
        self.list_widget.clear()
        for item in filtered: self.list_widget.addItem(item['isim'])

    def display_details(self, index):
        if index < 0 or not self.list_widget.currentItem(): return
        item = next((i for i in self.data if i['isim'] == self.list_widget.currentItem().text()), None)
        if item:
            self.type_badge.show()
            self.title_label.setText(item['isim'])
            self.type_badge.setText(f"KATEGORİ: {item['tur'].upper()}")
            
            accent = "#4caf50" if self.is_dark else "#2e7d32"
            content = f"""
                <div style='line-height: 160%;'>
                    <h3 style='color: {accent}; margin-bottom: 10px;'>🌟 Faydaları</h3>
                    <p>{item['faydalar']}</p>
                    <br>
                    <h3 style='color: #d35400; margin-bottom: 10px;'>🍵 Hazırlanışı</h3>
                    <p>{item['kullanim']}</p>
                </div>
            """
            self.info_text.setText(content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Sistem fontu olarak Inter veya Sans-Serif tercih et
    app.setFont(QFont("Sans-Serif", 10))
    window = KainatEczanesi()
    window.show()
    sys.exit(app.exec())