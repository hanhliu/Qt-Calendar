import os
import sys
import os
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QCalendarWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QGuiApplication
from src.custom_calendar import MonthViewer
from src.side_menu import LeftSideMenu


class CustomCalendarWidget(QCalendarWidget):
    def wheelEvent(self, event):
        event.ignore()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        screen = QGuiApplication.primaryScreen()
        full_screen_size = screen.geometry()
        desktop_screen_size = screen.availableGeometry()
        self.width_screen_desktop = desktop_screen_size.width()
        self.height_screen_desktop = desktop_screen_size.height()
        self.width_screen_fullscreen = full_screen_size.width()
        self.height_screen_fullscreen = full_screen_size.height()
        screen_size = screen.size()
        width_screen = screen_size.width()
        height_screen = screen_size.height()

        self.setGeometry(0, 0, self.width_screen_desktop,
                         self.height_screen_desktop)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.month_view = MonthViewer()
        self.button = QPushButton("Get Value")
        self.button.clicked.connect(self.getValue)

        self.layout.addWidget(self.month_view)
        self.layout.addWidget(self.button)
        side_widget = LeftSideMenu()

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(side_widget)
        main_layout.addLayout(self.layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

    def getValue(self):
        print("HanhLT: start date  ", self.month_view.getStartDate(), "    end  date  ", self.month_view.getEndDate())
        print("HanhLT: start time   ", self.month_view.getStartTime(), "     end time    ",
              self.month_view.getEndTime())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
