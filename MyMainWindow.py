from PyQt6.QtWidgets import QMainWindow
from FileChooser import FileChooser


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCentralWidget(FileChooser())
        self.setWindowTitle("Smarter Tuition")
        self.setMinimumSize(700, 500)
        self.setMaximumSize(700, 500)
