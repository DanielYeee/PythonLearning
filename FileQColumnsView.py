import os
from PyQt5.QtCore import QDir, Qt, QObject, QEvent
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QColumnView, QFileSystemModel, QVBoxLayout, QWidget, QMenu, QAction, QMessageBox

class FileExplorer(QWidget):
    def __init__(self):
        super(FileExplorer, self).__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a file system model
        model = QFileSystemModel()
        model.setRootPath("/")
        model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        # Create a column view
        column_view = QColumnView()
        column_view.setModel(model)
        column_view.setRootIndex(model.index("/"))  # Set the root directory

        # Connect the custom context menu
        column_view.setContextMenuPolicy(Qt.CustomContextMenu)
        column_view.customContextMenuRequested.connect(self.show_context_menu)

        # Install an event filter to capture key press events
        event_filter = KeyPressFilter(self)
        column_view.installEventFilter(event_filter)

        layout.addWidget(column_view)
        self.setLayout(layout)

    def show_context_menu(self, pos):
        index = self.sender().currentIndex()
        if not index.isValid():
            return

        menu = QMenu(self)

        # Actions for the context menu
        move_to_trash_action = QAction("Move to Trash", self)
        get_info_action = QAction("Get Info", self)
        rename_action = QAction("Rename", self)
        compress_action = QAction("Compress", self)

        # Connect actions to slots (dummy slots, customize as needed)
        move_to_trash_action.triggered.connect(self.move_to_trash)
        get_info_action.triggered.connect(self.get_info)
        rename_action.triggered.connect(self.rename)
        compress_action.triggered.connect(self.compress)

        # Add actions to the context menu
        menu.addAction(move_to_trash_action)
        menu.addAction(get_info_action)
        menu.addAction(rename_action)
        menu.addAction(compress_action)

        # Show the context menu at the specified position
        menu.exec_(self.sender().viewport().mapToGlobal(pos))

    # Define slot functions for the context menu actions (customize as needed)
    def move_to_trash(self):
        print("Move to Trash")

    def get_info(self):
        print("Get Info")

    def rename(self):
        print("Rename")

    def compress(self):
        print("Compress")

    # def show_item_info(self, index):
    #     if not index.isValid():
    #         return

    #     file_info = QFileSystemModel().fileInfo(index)
    #     path = file_info.absoluteFilePath()

    #     if file_info.isDir():
    #         QMessageBox.information(self, "Folder Info", f"Folder Path:\n{path}")
    #     else:
    #         with open(path, 'r') as file:
    #             content = file.read()
    #         QMessageBox.information(self, "File Contents", f"File Path:\n{path}\n\nContents:\n{content}")
    def show_item_info(self, index):
        if not index.isValid():
            return

        file_info = QFileSystemModel().fileInfo(index)
        path = file_info.absoluteFilePath()

        QMessageBox.information(self, "Item Info", f"Absolute Path:\n{path}")


class KeyPressFilter(QObject):
    def __init__(self, parent):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Space:
            if isinstance(obj, QColumnView):
                obj.show_item_info(obj.currentIndex())
                return True
        return False


if __name__ == "__main__":
    app = QApplication([])
    window = FileExplorer()

    # Set the window size similar to macOS Finder
    window.resize(800, 600)

    window.show()
    app.exec_()
