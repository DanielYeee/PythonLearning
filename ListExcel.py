import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox
import pandas as pd

class ExcelSheetSelector(QWidget):
    def __init__(self, file_path):
        super().__init__()
        
        self.file_path = file_path
        self.sheet_names = self.get_sheet_names()
        self.selected_sheets = []

        self.initUI()

    def get_sheet_names(self):
        # Use pandas to read the sheet names
        xls = pd.ExcelFile(self.file_path)
        return xls.sheet_names

    def initUI(self):
        self.setWindowTitle('Select Excel Sheets')
        
        # Layouts
        self.layout = QVBoxLayout()
        self.sheet_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        # Sheet radio buttons
        self.radio_buttons = []
        for sheet in self.sheet_names:
            radio_button = QRadioButton(sheet)
            radio_button.toggled.connect(self.on_radio_button_toggled)
            self.sheet_layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        # Submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.on_submit)

        # Adding layouts to main layout
        self.layout.addLayout(self.sheet_layout)
        self.layout.addLayout(self.button_layout)

        # Adding submit button to button layout
        self.button_layout.addWidget(self.submit_button)

        # Set main layout
        self.setLayout(self.layout)

    def on_radio_button_toggled(self):
        self.selected_sheets = [rb.text() for rb in self.radio_buttons if rb.isChecked()]
        if len(self.selected_sheets) > 2:
            for rb in self.radio_buttons:
                if rb.text() not in self.selected_sheets[:2]:
                    rb.setChecked(False)

    def on_submit(self):
        if len(self.selected_sheets) == 2:
            QMessageBox.information(self, 'Selected Sheets', f"You selected: {self.selected_sheets[0]} and {self.selected_sheets[1]}")
        else:
            QMessageBox.warning(self, 'Selection Error', 'Please select exactly two sheets.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_path = 'your_excel_file.xlsx'  # Replace with your Excel file path
    ex = ExcelSheetSelector(file_path)
    ex.show()
    sys.exit(app.exec_())
