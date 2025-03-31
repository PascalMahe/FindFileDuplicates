import sys


from PyQt6.QtWidgets import QApplication, QWidget

from create_window import create_main_widget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(create_main_widget(self))
        self.setWindowTitle("Duplicate File Analyzer")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    