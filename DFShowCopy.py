import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence

class DataFrameWidget(QWidget):
    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DataFrame Viewer')

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QTableWidget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.dataframe.shape[0])
        self.tableWidget.setColumnCount(self.dataframe.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(self.dataframe.columns)

        # Set the data in the QTableWidget
        for i in range(self.dataframe.shape[0]):
            for j in range(self.dataframe.shape[1]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.dataframe.iloc[i, j])))

        # Adjust the column widths and row heights
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i, 150)  # Adjust the width as needed
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(i, 30)  # Adjust the height as needed

        # Add the QTableWidget to the layout
        layout.addWidget(self.tableWidget)

        # Set the layout to the main widget
        self.setLayout(layout)

        # Set up the shortcut for copying
        copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        copy_shortcut.activated.connect(self.copySelection)

    def copySelection(self):
        selection = self.tableWidget.selectedRanges()
        if not selection:
            return

        copied_data = []
        for r in selection:
            rows = range(r.topRow(), r.bottomRow() + 1)
            cols = range(r.leftColumn(), r.rightColumn() + 1)
            for row in rows:
                copied_row = []
                for col in cols:
                    item = self.tableWidget.item(row, col)
                    if item:
                        copied_row.append(item.text())
                copied_data.append('\t'.join(copied_row))
        
        clipboard = QApplication.clipboard()
        clipboard.setText('\n'.join(copied_data))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create a sample DataFrame
    df = pd.DataFrame({
        'Column 1': [1, 2, 3, 4],
        'Column 2': ['A', 'B', 'C', 'D'],
        'Column 3': [10.1, 20.2, 30.3, 40.4]
    })

    # Create and show the DataFrameWidget
    widget = DataFrameWidget(df)
    widget.resize(600, 400)  # Adjust the initial size as needed
    widget.show()

    sys.exit(app.exec_())
