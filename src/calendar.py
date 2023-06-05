from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtCore import Qt, QDate, QLocale
from PySide6.QtWidgets import QWidget,  QVBoxLayout, QLabel, QHBoxLayout, QCalendarWidget

class CalendarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = None
        self.calendar = None
        self.load_ui()

    def load_ui(self):
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.setCurrentPage(QDate.currentDate().year(), QDate.currentDate().month())
        self.calendar.setNavigationBarVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)


        # Get the current date
        today = QDate.currentDate()

        # Create a QLabel widget to display the month and year
        label = QLabel('Month and Year: {}'.format(today.toString('MMMM yyyy')))

        locale = QLocale(QLocale.English)

        # Create a list of all months
        all_months = []
        for month in range(1, 13):
            date = QDate(2023, month, 1)
            month_name = locale.toString(date, 'MMMM')
            all_months.append(month_name)




        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(label)
        self.setLayout(self.layout)
