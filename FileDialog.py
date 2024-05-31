import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

class FileChooserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Chooser Example")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("No file selected", self)
        layout.addWidget(self.label)

        self.button = QPushButton("Choose File", self)
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.label.setText(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileChooserWindow()
    window.show()
    sys.exit(app.exec_())
