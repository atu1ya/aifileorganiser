"""
PySide6 GUI logic placeholder
"""
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QCheckBox, QGroupBox, QFrame, QSpacerItem, QSizePolicy
)
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI File Organiser")
        self.resize(540, 340)
        self.setStyleSheet("""
            QWidget {
                background: #f7f8fa;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 17px;
                color: #1a1a1a;
            }
            QLabel#HeaderLabel {
                font-size: 30px;
                font-weight: bold;
                color: #1a237e;
                margin-bottom: 14px;
                letter-spacing: 1px;
            }
            QGroupBox {
                border: 1.5px solid #b0b7c3;
                border-radius: 10px;
                margin-top: 12px;
                background: #fff;
                font-size: 17px;
            }
            QPushButton {
                background: #1976d2;
                color: #fff;
                border-radius: 7px;
                padding: 12px 0;
                font-size: 18px;
                margin: 8px 0;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #0d47a1;
            }
            QCheckBox {
                margin: 10px 0 10px 0;
                font-size: 19px;
                font-weight: bold;
                color: #0d47a1;
                background: #e3f2fd;
                border-radius: 5px;
                padding: 6px 10px 6px 10px;
            }
            QLabel#StatsLabel {
                color: #374151;
                font-size: 16px;
                margin-top: 10px;
            }
            QLabel#StatusLabel {
                color: #e65100;
                font-size: 17px;
                margin-top: 10px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 18, 24, 18)
        main_layout.setSpacing(10)

        # Header
        header = QLabel("AI File Organiser")
        header.setObjectName("HeaderLabel")
        header.setAlignment(Qt.AlignCenter)
        header.setWordWrap(True)
        main_layout.addWidget(header)

        # Group: Folder selection
        folder_group = QGroupBox("Folders")
        folder_layout = QVBoxLayout()
        self.label = QLabel("Select source and destination folders.")
        self.label.setObjectName("StatusLabel")
        self.label.setWordWrap(True)
        folder_layout.addWidget(self.label)

        btn_layout = QHBoxLayout()
        self.src_btn = QPushButton("Select Source Folder")
        self.src_btn.setMinimumWidth(200)
        self.src_btn.setToolTip("Choose the folder containing files to organise.")
        self.src_btn.clicked.connect(self.select_source)
        btn_layout.addWidget(self.src_btn)
        self.dst_btn = QPushButton("Select Destination Folder")
        self.dst_btn.setMinimumWidth(200)
        self.dst_btn.setToolTip("Choose the folder where organised files will be placed.")
        self.dst_btn.clicked.connect(self.select_destination)
        btn_layout.addWidget(self.dst_btn)
        folder_layout.addLayout(btn_layout)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)

        # Group: Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self.ai_checkbox = QCheckBox("Enable AI-based content sorting")
        self.ai_checkbox.setToolTip("Use AI to group files by content and type.")
        options_layout.addWidget(self.ai_checkbox)
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # Group: Actions
        actions_group = QGroupBox()
        actions_layout = QVBoxLayout()
        self.organise_btn = QPushButton("Organise Files")
        self.organise_btn.setMinimumHeight(44)
        self.organise_btn.setToolTip("Start organising files from source to destination.")
        self.organise_btn.setStyleSheet("font-weight: bold;")
        self.organise_btn.clicked.connect(self.organise_files)
        actions_layout.addWidget(self.organise_btn)
        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)

        # Stats
        self.stats_label = QLabel("Files sorted: 0 | Duplicates detected: 0")
        self.stats_label.setObjectName("StatsLabel")
        self.stats_label.setWordWrap(True)
        main_layout.addWidget(self.stats_label)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)
        self.source_folder = None
        self.destination_folder = None

    def organise_files(self):
        if not self.source_folder or not self.destination_folder:
            self.label.setText("Please select both source and destination folders.")
            return
        from organiser.organiser import organise_files
        use_ai = self.ai_checkbox.isChecked()
        try:
            files_sorted, duplicates_detected = organise_files(self.source_folder, self.destination_folder, use_ai)
            self.stats_label.setText(f"Files sorted: {files_sorted} | Duplicates detected: {duplicates_detected}")
            self.label.setText("Organisation complete!")
        except Exception as e:
            self.label.setText(f"Error: {e}")

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

from PySide6.QtCore import Qt

def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
