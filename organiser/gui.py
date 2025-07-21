"""
PySide6 GUI logic placeholder
"""
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QCheckBox
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI File Organiser")
        self.resize(500, 300)
        layout = QVBoxLayout()
        self.label = QLabel("Select source and destination folders.")
        layout.addWidget(self.label)
        self.src_btn = QPushButton("Select Source Folder")
        self.src_btn.clicked.connect(self.select_source)
        layout.addWidget(self.src_btn)
        self.dst_btn = QPushButton("Select Destination Folder")
        self.dst_btn.clicked.connect(self.select_destination)
        layout.addWidget(self.dst_btn)
        self.ai_checkbox = QCheckBox("Enable AI-based content sorting")
        layout.addWidget(self.ai_checkbox)
        self.stats_label = QLabel("Files sorted: 0 | Duplicates detected: 0")
        layout.addWidget(self.stats_label)
        self.setLayout(layout)
        self.source_folder = None
        self.destination_folder = None

    def select_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_folder = folder
            self.label.setText(f"Source: {folder}")

    def select_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.destination_folder = folder
            self.label.setText(f"Destination: {folder}")

def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
