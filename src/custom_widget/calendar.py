import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget

class CustomCalendarWidget(QCalendarWidget):
    def __init__(self):
        super().__init__()

        # Add custom initialization or settings here
        self.setGridVisible(True)  # Example: Show grid lines
        # QCalendar
        self.setNavigationBarVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)

        style = "QMenu { font-size:16px; width: 150px; left: 20px;"
        "background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);}"
        "QToolButton {icon-size: 48px, 48px;background-color: qlineargradient(x1:0, y1:0, x2:0,"
        "y2:1, stop: 0 #cccccc, stop: 1 #333333);"
        "height: 100px; width: 200px;}"
        "QAbstractItemView {selection-background-color: rgb(255, 174, 0);}"
        "QToolButton::menu-arrow {}"
        "QToolButton::menu-button {}"
        "QToolButton::menu-indicator{width: 50px;}"
        "QToolButton::menu-indicator:pressed,"
        "QToolButton::menu-indicator:open{top:10px; left: 10px;}"
        "QListView {background-color:white;}"
        "QSpinBox::up-button { subcontrol-origin: border;"
        "subcontrol-position: top right; width:50px; border-image: url(icons:arrow_up_n.png);}"
        "QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right;"
        "border-width: 1px; width:50px;}"
        "QSpinBox::down-arrow { width:26px; height:17px;"
        "image: url(icons:arrow_down_n.png); } "

        self.setStyleSheet(f'''
            QCalendarWidget QWidget{{
                background-color: white;
                color: green;
                
            }}
            QCalendarWidget {{
                background-color: red;
                color: darkblue;
                font-size: 16px;
            }}
            
            QCalendarWidget QHeaderView:horizontal {{
                background-color: red;
                font-weight: bold;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: white;
                color: black;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: yellow;
            }}
            QCalendarWidget QToolButton#qt_calendar_nextmonth::right-arrow{{
               icon: url(/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-down.png)
            }}
            QCalendarWidget QToolButton#qt_calendar_nextmonth::left-arrow{{
                icon: url(/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-down.png)
            }}

            QCalendarWidget QAbstractItemView:disabled {{
                color: lightgray;
            }}
            
            QCalendarWidget QAbstractItemView:focus {{
                border: 2px solid black;
            }}
            QCalendarWidget QAbstractItemView:enabled{{
                background-color: white;
                color: black;
            }}
            QCalendarWidget QMenu{{
                background-color: rgb(255, 46, 221);
            }}
            
            QCalendarWidget QSpinBox{{
                background-color: black;
            }}
        ''')

    # Override showNextMonth and showPreviousMonth to prevent scrolling
    def showNextMonth(self):
        pass

    def showPreviousMonth(self):
        pass

    def showNextYear(self) -> None:
        pass

    def showPreviousYear(self) -> None:
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        custom_calendar = CustomCalendarWidget()
        layout.addWidget(custom_calendar)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
