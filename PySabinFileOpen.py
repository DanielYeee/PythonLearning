import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

class FileChooserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SABIN File Chooser Example")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("No file selected", self)
        layout.addWidget(self.label)

        self.button = QPushButton("Choose SABIN File", self)
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open SABIN File", "", "SABIN Files (*.sabin);;All Files (*)", options=options)
        if file_path:
            self.label.setText(file_path)
            self.read_sabin_file(file_path)

    def read_sabin_file(self, file_path):
        try:
            with open(file_path, 'r') as file:  # Adjust mode 'r' or 'rb' based on your file format (text/binary)
                content = file.read()
                # Process the content based on SABIN file specification
                self.label.setText(f"File loaded: {file_path}")
                # You can add more detailed parsing and display here
        except Exception as e:
            self.label.setText(f"Error reading file: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileChooserWindow()
    window.show()
    sys.exit(app.exec_())
