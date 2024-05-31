import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QPushButton
from PyQt5.QtCore import QAbstractTableModel, Qt

class DataFrameModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._dataframe = df

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            elif orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

class DataFrameWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('DataFrame Viewer')
        
        layout = QVBoxLayout()
        
        self.tableView = QTableView()
        layout.addWidget(self.tableView)
        
        self.button = QPushButton('Load DataFrame')
        self.button.clicked.connect(self.loadDataFrame)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
    def loadDataFrame(self):
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [10, 20, 30, 40, 50]
        }
        df = pd.DataFrame(data)
        
        model = DataFrameModel(df)
        self.tableView.setModel(model)
        
def main():
    app = QApplication(sys.argv)
    window = DataFrameWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
