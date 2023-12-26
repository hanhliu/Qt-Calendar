import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QDate

from src.common_controller.common_qsettings import CommonQSettings
from src.common_controller.main_controller import MainController
from src.grid_custom.grid_main import MainGrid
from src.grid_custom.grid_main_two import MainGridTwo


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_controller = MainController()
        self.common_qsettings = CommonQSettings()
        self.main_controller.list_divisions = self.common_qsettings.get_data_grid()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Custom Grid')

        layout = QVBoxLayout()
        self.mainwindow = MainGridTwo()
        layout.addWidget(self.mainwindow)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())
