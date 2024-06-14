import sys
import datetime
import pytz
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self, gyro_data):
        super().__init__()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)
        self.plot_gyro_data(gyro_data)

    def plot_gyro_data(self, gyro_data):
        x_data = [data[0] for data in gyro_data]
        y_data = [data[1] for data in gyro_data]
        z_data = [data[2] for data in gyro_data]
        w_data = [data[3] for data in gyro_data]

        self.canvas.axes.plot(x_data, y_data, label='X-axis')
        self.canvas.axes.plot(x_data, z_data, label='Y-axis')
        self.canvas.axes.plot(x_data, w_data, label='Z-axis')

        self.canvas.axes.set_xlabel('Time')
        self.canvas.axes.set_ylabel('Gyro Value')
        self.canvas.axes.legend()
        self.canvas.draw()


def read_gyro_data_from_file(file_path):
    gyro_data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 5:
                try:
                    timestamp = int(parts[0])
                    date_time = datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    gyro_data.append((date_time, x, y, z))
                except ValueError:
                    pass  # Skip lines with invalid data
    return gyro_data


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # File dialog to select the gyro data file
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Text files (*.txt)")
    file_dialog.setViewMode(QFileDialog.Detail)
    if file_dialog.exec_():
        file_path = file_dialog.selectedFiles()[0]

        # Read gyro data from the selected file
        gyro_data = read_gyro_data_from_file(file_path)

        if gyro_data:
            main_window = MainWindow(gyro_data)
            main_window.show()
            sys.exit(app.exec_())
        else:
            print("No valid gyro data found in the file.")
    else:
        print("No file selected.")
