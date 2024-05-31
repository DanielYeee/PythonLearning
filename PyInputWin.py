import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Input Window')
        
        # Set up layout
        layout = QVBoxLayout()
        
        # Create and add widgets
        self.label = QLabel('Enter something:', self)
        layout.addWidget(self.label)
        
        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit)
        
        self.button = QPushButton('Submit', self)
        self.button.clicked.connect(self.onSubmit)
        layout.addWidget(self.button)
        
        self.resultLabel = QLabel('', self)
        layout.addWidget(self.resultLabel)
        
        # Set layout
        self.setLayout(layout)
        
    def onSubmit(self):
        # Get text from QLineEdit
        text = self.lineEdit.text()
        # Display the text in resultLabel
        self.resultLabel.setText(f'You entered: {text}')
        
# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
