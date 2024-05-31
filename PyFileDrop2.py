import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap

class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setText("Drag and drop a file here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel { border: 2px dashed #aaa; background-color: white; }")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("QLabel { border: 2px dashed #aaa; background-color: paleblue; }")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("QLabel { border: 2px dashed #aaa; background-color: white; }")
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.setPixmap(QPixmap(file_path))  # Assuming the file is an image
                self.setText(file_path)

            self.setStyleSheet("QLabel { border: 2px dashed #aaa; background-color: white; }")
        else:
            event.ignore()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Drop Example")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.label = DropLabel(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
