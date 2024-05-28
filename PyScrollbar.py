import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QScrollArea, QLabel

class CheckBoxLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scrollable CheckBoxes on Labels')
        self.setGeometry(100, 100, 300, 400)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to contain the checkboxes
        widget = QWidget()
        scroll_area.setWidget(widget)

        # Create a vertical layout for the checkboxes
        layout = QVBoxLayout(widget)

        # Add checkboxes on labels
        for i in range(30):  # Adding 30 checkboxes for demonstration
            checkbox_label = QLabel(f'Checkbox {i}')
            checkbox = QCheckBox()
            checkbox_label.setBuddy(checkbox)
            layout.addWidget(checkbox_label)
            layout.addWidget(checkbox)

        # Set the layout of the main window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheckBoxLabel()
    window.show()
    sys.exit(app.exec_())
