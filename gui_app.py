"""
GUI Application for Vietnamese Font Converter
Supports DOCX, XLSX files and text paste-in conversion
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog,
    QMessageBox, QComboBox, QProgressBar, QSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from document_converter import DocumentConverter
from vni_unicode_mapping import (
    vni_to_unicode, unicode_to_vni, VNI_FONTS, UNICODE_FONTS
)


class ConversionWorker(QThread):
    """Worker thread for file conversion"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    
    def __init__(self, converter, input_path, output_path, conversion_type):
        super().__init__()
        self.converter = converter
        self.input_path = input_path
        self.output_path = output_path
        self.conversion_type = conversion_type
    
    def run(self):
        try:
            success, message, output_path = self.converter.convert_file(
                self.input_path, self.output_path, self.conversion_type
            )
            if success:
                self.success.emit(message)
            else:
                self.error.emit(message)
        except Exception as e:
            self.error.emit(f"Conversion error: {str(e)}")
        finally:
            self.finished.emit()


class VNFontConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.converter = DocumentConverter()
        self.conversion_worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Vietnamese Font Converter")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:pressed {
                background-color: #003d7a;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QLabel {
                color: #333;
            }
        """)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Tab widget
        tabs = QTabWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(tabs)
        
        # Tab 1: File Conversion
        tabs.addTab(self.create_file_tab(), "📄 File Conversion")
        
        # Tab 2: Text Conversion
        tabs.addTab(self.create_text_tab(), "✍️ Text Conversion")
        
        # Tab 3: Settings
        tabs.addTab(self.create_settings_tab(), "⚙️ Settings")
    
    def create_file_tab(self):
        """Create file conversion tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Input file section
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Input File:"))
        self.input_file_path = QLineEdit()
        self.input_file_path.setReadOnly(True)
        input_layout.addWidget(self.input_file_path)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(browse_btn)
        layout.addLayout(input_layout)
        
        # Output file section
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output File:"))
        self.output_file_path = QLineEdit()
        output_layout.addWidget(self.output_file_path)
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Conversion type section
        conv_layout = QHBoxLayout()
        conv_layout.addWidget(QLabel("Conversion Type:"))
        self.file_conversion_type = QComboBox()
        self.file_conversion_type.addItems([
            "Auto Detect",
            "VNI → Unicode",
            "Unicode → VNI"
        ])
        conv_layout.addWidget(self.file_conversion_type)
        conv_layout.addStretch()
        layout.addLayout(conv_layout)
        
        # File supported info
        info_label = QLabel(
            "📋 Supported formats: .docx (Word), .xlsx (Excel)\n"
            "✨ All formatting (colors, fonts, styles) will be preserved"
        )
        info_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(info_label)
        
        # Progress bar
        self.file_progress = QProgressBar()
        self.file_progress.setVisible(False)
        layout.addWidget(self.file_progress)
        
        # Convert button
        convert_btn = QPushButton("Convert File")
        convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        convert_btn.clicked.connect(self.convert_file)
        layout.addWidget(convert_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_text_tab(self):
        """Create text conversion tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("Vietnamese Text Font Converter")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Conversion type
        conv_layout = QHBoxLayout()
        conv_layout.addWidget(QLabel("Conversion:"))
        self.text_conversion_type = QComboBox()
        self.text_conversion_type.addItems([
            "VNI → Unicode",
            "Unicode → VNI"
        ])
        self.text_conversion_type.currentTextChanged.connect(self.update_text_labels)
        conv_layout.addWidget(self.text_conversion_type)
        conv_layout.addStretch()
        layout.addLayout(conv_layout)
        
        # Input text section
        self.input_text_label = QLabel("VNI Text (Input):")
        self.input_text_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.input_text_label)
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Paste your VNI encoded text here...")
        self.input_text.setMinimumHeight(150)
        layout.addWidget(self.input_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        clear_input_btn = QPushButton("Clear Input")
        clear_input_btn.clicked.connect(lambda: self.input_text.clear())
        button_layout.addWidget(clear_input_btn)
        
        convert_text_btn = QPushButton("Convert")
        convert_text_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        convert_text_btn.clicked.connect(self.convert_text)
        button_layout.addWidget(convert_text_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Output text section
        self.output_text_label = QLabel("Unicode Text (Output):")
        self.output_text_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.output_text_label)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(150)
        layout.addWidget(self.output_text)
        
        # Copy button
        copy_btn = QPushButton("Copy Output to Clipboard")
        copy_btn.clicked.connect(self.copy_output_text)
        layout.addWidget(copy_btn)
        
        return widget
    
    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # VNI Fonts section
        vni_label = QLabel("VNI Fonts Detected:")
        vni_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(vni_label)
        vni_text = QTextEdit()
        vni_text.setReadOnly(True)
        vni_text.setPlainText("\n".join(VNI_FONTS))
        vni_text.setMaximumHeight(100)
        layout.addWidget(vni_text)
        
        # Unicode Fonts section
        unicode_label = QLabel("Unicode Fonts (Target):")
        unicode_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(unicode_label)
        unicode_text = QTextEdit()
        unicode_text.setReadOnly(True)
        unicode_text.setPlainText("\n".join(UNICODE_FONTS))
        unicode_text.setMaximumHeight(100)
        layout.addWidget(unicode_text)
        
        # Info section
        info_label = QLabel(
            "ℹ️ Information:\n"
            "• VNI fonts use encoding system where Vietnamese characters are mapped differently\n"
            "• Unicode fonts use standard Unicode encoding (U+0000 to U+FFFF)\n"
            "• This tool automatically detects and converts between these encodings\n"
            "• All formatting is preserved during conversion\n\n"
            "📌 Common Vietnamese fonts:\n"
            "VNI: VNI-Times, VnArial, VnTimes\n"
            "Unicode: Times New Roman, Arial, Calibri"
        )
        info_label.setStyleSheet("color: #555; line-height: 1.6;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        return widget
    
    def browse_input_file(self):
        """Browse for input file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input File", "",
            "Office Files (*.docx *.xlsx);;Word Files (*.docx);;Excel Files (*.xlsx)"
        )
        if file_path:
            self.input_file_path.setText(file_path)
            # Auto-generate output path
            base, ext = os.path.splitext(file_path)
            self.output_file_path.setText(f"{base}_converted{ext}")
    
    def browse_output_file(self):
        """Browse for output file location"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Output File", "",
            "Office Files (*.docx *.xlsx);;Word Files (*.docx);;Excel Files (*.xlsx)"
        )
        if file_path:
            self.output_file_path.setText(file_path)
    
    def convert_file(self):
        """Convert file with progress indication"""
        input_path = self.input_file_path.text()
        output_path = self.output_file_path.text()
        
        if not input_path:
            QMessageBox.warning(self, "Error", "Please select an input file")
            return
        
        if not output_path:
            QMessageBox.warning(self, "Error", "Please specify an output file")
            return
        
        # Get conversion type
        conversion_type = self.file_conversion_type.currentText()
        if conversion_type == "Auto Detect":
            conversion_type = "auto"
        elif conversion_type == "VNI → Unicode":
            conversion_type = "vni_to_unicode"
        else:
            conversion_type = "unicode_to_vni"
        
        # Disable button and show progress
        sender = self.sender()
        sender.setEnabled(False)
        self.file_progress.setVisible(True)
        self.file_progress.setRange(0, 0)  # Indeterminate progress
        
        # Start conversion in separate thread
        self.conversion_worker = ConversionWorker(
            self.converter, input_path, output_path, conversion_type
        )
        self.conversion_worker.success.connect(self.on_conversion_success)
        self.conversion_worker.error.connect(self.on_conversion_error)
        self.conversion_worker.finished.connect(lambda: sender.setEnabled(True))
        self.conversion_worker.finished.connect(lambda: self.file_progress.setVisible(False))
        self.conversion_worker.start()
    
    def convert_text(self):
        """Convert pasted text"""
        input_text = self.input_text.toPlainText()
        
        if not input_text:
            QMessageBox.warning(self, "Error", "Please enter some text to convert")
            return
        
        conversion_type = self.text_conversion_type.currentText()
        
        if "VNI → Unicode" in conversion_type:
            output_text = vni_to_unicode(input_text)
        else:
            output_text = unicode_to_vni(input_text)
        
        self.output_text.setPlainText(output_text)
    
    def copy_output_text(self):
        """Copy output text to clipboard"""
        text = self.output_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Success", "Text copied to clipboard!")
        else:
            QMessageBox.warning(self, "Error", "Nothing to copy")
    
    def update_text_labels(self):
        """Update labels based on conversion type"""
        conversion_type = self.text_conversion_type.currentText()
        if "VNI → Unicode" in conversion_type:
            self.input_text_label.setText("VNI Text (Input):")
            self.output_text_label.setText("Unicode Text (Output):")
            self.input_text.setPlaceholderText("Paste your VNI encoded text here...")
        else:
            self.input_text_label.setText("Unicode Text (Input):")
            self.output_text_label.setText("VNI Text (Output):")
            self.input_text.setPlaceholderText("Paste your Unicode text here...")
    
    def on_conversion_success(self, message):
        """Handle successful conversion"""
        QMessageBox.information(self, "Success", message)
    
    def on_conversion_error(self, error_message):
        """Handle conversion error"""
        QMessageBox.critical(self, "Error", error_message)


def main():
    app = QApplication(sys.argv)
    window = VNFontConverterGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
