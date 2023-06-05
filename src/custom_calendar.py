import sys
from PySide6.QtCore import QDate, QLocale, Qt, QTime, QDateTime
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCalendarWidget, \
    QDateTimeEdit
from PySide6.QtGui import QTextCharFormat, QPalette

month_names = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


class MonthViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Month Viewer")
        self.__highlight_format = QTextCharFormat()
        self.__highlight_format.setBackground(self.palette().brush(QPalette.Highlight))
        self.__highlight_format.setForeground(self.palette().color(QPalette.HighlightedText))

        self.__current_week = QDate.currentDate().weekNumber()
        self.__current_month = QDate.currentDate().month()
        self.__current_year = QDate.currentDate().year()
        self.__sYear = QDate.currentDate().year()
        self.__sMonth = QDate.currentDate().toString("MM")
        self.__sDate = QDate.currentDate().day()
        self.__sDateFinal = QDate().currentDate()  # this final date to use
        self.__calendar = QCalendarWidget()
        self.__calendar.setCurrentPage(QDate.currentDate().year(), QDate.currentDate().month())
        self.__calendar.setSelectedDate(QDate.currentDate())
        self.__calendar.setStyleSheet('''
            QCalendarWidget QTableView {
                selection-color: black;
                selection-background-color: #A4D8FD;
                background-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled{
                background-color: white;
                color: black;
            }

            QCalendarWidget QWidget{
                background-color:white;
                color: grey;
                border: 1px solid gray;
            }  
            ''')

        # Variable to keep track of the previously clicked label
        self.__previous_year_label = None
        self.__previous_month_label = None
        self.__label_year_pick = None
        self.__label_month_pick = None

        self.__begin_date = QDate().currentDate()
        self.__end_date = QDate().currentDate()
        self.start_value = QDateTime()
        self.end_value = QDateTime()
        self.end_time = QTime(23, 59, 00)
        self.start_time = QTime(00, 00, 00)
        self.__month_labels = []
        self.__year_labels = []
        self.setup_ui()

    def setup_ui(self):
        self.__label_year_pick = str(self.__sYear)
        self.__label_month_pick = self.__sMonth
        # Create layout for the month labels
        months_layout = QHBoxLayout()
        # Create layout for the navigation buttons
        month_buttons_layout = QHBoxLayout()
        # Create the navigation buttons
        month_prev_button = QPushButton("<")
        month_prev_button.clicked.connect(self.__previous_months)
        month_prev_button.setFixedSize(24, 24)
        month_next_button = QPushButton(">")
        month_next_button.clicked.connect(self.__next_months)
        month_next_button.setFixedSize(24, 24)
        # Create the month labels
        for i in range(3):
            self.__month_label = QLabel()
            self.__month_label.setAlignment(Qt.AlignCenter)
            self.__month_labels.append(self.__month_label)
            months_layout.addWidget(self.__month_label)
            self.__update_month_label(i)

        # Add the navigation buttons to the buttons layout
        month_buttons_layout.addWidget(month_prev_button)
        month_buttons_layout.addLayout(months_layout)
        month_buttons_layout.addWidget(month_next_button)
        months_widget = QWidget()
        months_widget.setLayout(month_buttons_layout)
        months_widget.setObjectName("month_parentWidget")
        months_widget.setStyleSheet('''
                    QWidget#month_parentWidget {
                        background-color: white;
                        border: 1px solid gray;
                    }

                    QWidget#month_parentWidget QPushButton {
                        background-color: white;
                        color: gray;
                        border-radius: 5px;
                        border: 1px solid gray;
                        padding: 5px 5px;
                    }

                    QWidget#month_parentWidget QPushButton:hover {
                        background-color: #A4D8FD;
                    }

                ''')

        # year UI
        year_prev_button = QPushButton("<")
        year_prev_button.clicked.connect(self.__previous_years)
        year_prev_button.setFixedSize(24, 24)
        year_next_button = QPushButton(">")
        year_next_button.clicked.connect(self.__next_years)
        year_next_button.setFixedSize(24, 24)
        year_layout = QHBoxLayout()
        year_button_layout = QHBoxLayout()
        year_widget = QWidget()
        for i in range(3):
            self.__year_label = QLabel()
            self.__year_label.setAlignment(Qt.AlignCenter)
            self.__year_labels.append(self.__year_label)
            year_layout.addWidget(self.__year_label)
            self.__update_year_label(i)
        year_button_layout.addWidget(year_prev_button)
        year_button_layout.addLayout(year_layout)
        year_button_layout.addWidget(year_next_button)
        year_widget.setLayout(year_button_layout)
        year_widget.setObjectName("year_parentWidget")
        year_widget.setStyleSheet('''
            QWidget#year_parentWidget {
                background-color: white;
                border: 1px solid gray;
            }
            QWidget#year_parentWidget QPushButton {
                background-color: white;
                color: gray;
                border-radius: 5px;
                border: 1px solid gray;
                padding: 5px 5px;
            }
            QWidget#year_parentWidget QPushButton:hover {
                background-color: #A4D8FD;
            }
        ''')

        # QCalendar
        self.__calendar.setNavigationBarVisible(False)
        self.__calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.__calendar.installEventFilter(self)
        self.__calendar.clicked.connect(self.__date_is_clicked)
        self.__calendar.setToolTip("Giữ phím Shift để chọn khoảng thời gian")

        self.__time_picker = TimePickerWidget()

        # Create the main layout and add the sub-layouts to it
        main_layout = QVBoxLayout()
        main_layout.addWidget(year_widget)
        main_layout.addWidget(months_widget)
        main_layout.addWidget(self.__calendar)
        main_layout.addWidget(self.__time_picker)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def getStartDate(self):
        return self.__begin_date

    def getEndDate(self):
        return self.__end_date

    def setStartDate(self, date):
        self.__begin_date = date
        return self.__begin_date

    def setEndDate(self, date):
        self.__end_date = date
        return self.__end_date

    def getStartTime(self):
        self.start_time = self.__time_picker.start_time_value
        return self.start_time

    def getEndTime(self):
        self.end_time = self.__time_picker.end_time_value
        return self.end_time

    def __format_range(self, format):
        if self.__begin_date and self.__end_date:
            d0 = min(self.__begin_date, self.__end_date)
            d1 = max(self.__begin_date, self.__end_date)
            while d0 <= d1:
                self.__calendar.setDateTextFormat(d0, format)
                d0 = d0.addDays(1)

    def __date_is_clicked(self, date):
        # reset highlighting of previously selected date range
        self.__format_range(QTextCharFormat())
        if QApplication.instance().keyboardModifiers() & Qt.ShiftModifier and self.__begin_date:
            self.start_value = QDateTime(self.__begin_date, self.__time_picker.start_time_value)
            self.end_value = QDateTime(self.__end_date, self.__time_picker.end_time_value)
            print("HanhLT: beginn   ", self.__begin_date, "      end ", self.__end_date)
            if self.__begin_date < date:
                self.setEndDate(date)
            elif self.__begin_date > date:
                self.setEndDate(self.__begin_date)
                self.__begin_date = date
            else:
                print("date1 and date2 are the same")

            # set high lighting of currently    selected date range
            self.__format_range(self.__highlight_format)
        else:
            # self.begin_date = date
            # self.end_date = date
            self.setStartDate(date)
            self.setEndDate(date)
            print("HanhLT: beginn   ", self.__begin_date, "      end ", self.__end_date)

    def __update_month_label(self, index):
        # Calculate the year and month for the label at the given index
        month_offset = index - 1
        year = self.__current_year + (self.__current_month + month_offset - 1) // 12
        month = (self.__current_month + month_offset - 1) % 12 + 1
        # Create a QLocale object for the current locale
        locale = QLocale()

        # Convert the date to a string using the current locale
        month_string = locale.standaloneMonthName(month, QLocale.ShortFormat)
        year_string = str(year)
        label_text = f"{month_string}"
        # Set the label text
        self.__month_labels[index].setText(label_text)
        self.__month_labels[index].setProperty('circle', 'true')
        self.__month_label.mousePressEvent = lambda event, label=label_text: self.__month_clicked(
            self.__month_labels[index],
            self.__month_labels[
                index].text())

        self.__month_labels[index].setStyleSheet('''QLabel {padding: 10px;}''')
        if self.__month_labels[index].text() == self.__label_month_pick:
            self.__previous_month_label = self.__month_labels[index]
            self.__month_labels[index].setStyleSheet('''
                                       QLabel {
                                        background-color: #A4D8FD;
                                        padding: 8px;
                                        border: 2px solid #A4D8FD;
                                        border-radius: 10px;
                                    }
                                    ''')

    def __month_clicked(self, label_obj, content):
        self.__change_Stylesheet(label_obj, check_year=False)
        self.__sMonth = content
        self.__sDateFinal = QDate(self.__sYear, month_names[self.__sMonth], self.__sDate)
        self.__calendar.setSelectedDate(QDate(self.__sYear, month_names[self.__sMonth], self.__sDate))

    def __update_year_label(self, index):
        # Calculate the year and month for the label at the given index
        year_offset = index - 2
        year = self.__current_year + year_offset

        # Create a QLocale object for the current locale
        locale = QLocale()

        # Convert the date to a string using the current locale
        year_string = str(year)
        label_text = f"{year_string}"
        # Set the label text
        self.__year_labels[index].setText(label_text)
        self.__year_label.mousePressEvent = lambda event, label=label_text: self.__year_clicked(
            self.__year_labels[index],
            self.__year_labels[
                index].text())

        self.__year_labels[index].setStyleSheet('''QLabel {padding: 10px;}''')
        if self.__year_labels[index].text() == self.__label_year_pick:
            self.__previous_year_label = self.__year_labels[index]
            self.__year_labels[index].setStyleSheet('''
                               QLabel {
                                background-color: #A4D8FD;
                                padding: 8px;
                                border: 2px solid #A4D8FD;
                                border-radius: 10px;
                            }
                            ''')

    def __year_clicked(self, label_obj, content):
        self.__change_Stylesheet(label_obj, check_year=True)
        self.__sYear = int(content)
        self.__sDateFinal = QDate(self.__sYear, month_names[self.__sMonth], self.__sDate)
        self.__calendar.setSelectedDate(QDate(self.__sYear, month_names[self.__sMonth], self.__sDate))

    def __next_months(self):
        # Increment the current month by 5
        self.__current_month += 3
        if self.__current_month > 12:
            self.__current_month -= 12
            self.__current_year += 1

        # Update the month labels
        for i in range(3):
            self.__update_month_label(i)

    def __previous_months(self):
        # Decrement the current month by 5
        self.__current_month -= 3
        if self.__current_month < 1:
            self.__current_month += 12
            self.__current_year -= 1

        # Update the month labels
        for i in range(3):
            self.__update_month_label(i)

    def __next_years(self):
        # Increment the current year by 5
        self.__current_year += 3
        # Update the year labels
        for i in range(3):
            self.__update_year_label(i)

    def __previous_years(self):
        # Decrement the current year by 5
        self.__current_year -= 3
        # Update the year labels
        for i in range(3):
            self.__update_year_label(i)

    def __change_Stylesheet(self, label_obj, check_year):
        # Reset the stylesheet of the previously clicked label
        if check_year:
            if self.__previous_year_label:
                self.__previous_year_label.setStyleSheet('''
                                    QLabel {
                                        padding: 10px;
                                    }
                                ''')
            # Set the stylesheet of the clicked label
            label_obj.setStyleSheet('''
                                QLabel {
                                    background-color: #A4D8FD;
                                    padding: 8px;

                                    border: 2px solid #A4D8FD;
                                    border-radius: 10px;
                                }
                            ''')
            # padding - top: 16px;
            # padding - right: 8px;
            # padding - bottom: 16px;
            # padding - left: 8px;

            self.__label_year_pick = label_obj.text()

            # Set the clicked label as the previously clicked label
            self.__previous_year_label = label_obj
        else:
            if self.__previous_month_label:
                self.__previous_month_label.setStyleSheet('''
                                    QLabel {
                                        padding: 8px;
                                    }
                                ''')
            # Set the stylesheet of the clicked label
            label_obj.setStyleSheet('''
                                QLabel {
                                    background-color: #A4D8FD;
                                    padding: 8px;
                                    border: 2px solid #A4D8FD;
                                    border-radius: 10px;
                                }
                            ''')

            self.__label_month_pick = label_obj.text()

            # Set the clicked label as the previously clicked label
            self.__previous_month_label = label_obj


class TimePickerWidget(QWidget):

    def __init__(self):
        super().__init__()

        # setting title
        self.__main_layout = None
        self.__end_time_edit = None
        self.__start_time_edit = None
        self.__end_time_label = None
        self.__start_time_label = None
        self.__end_widget = None
        self.__start_widget = None
        self.__end_time_layout = None
        self.__start_time_layout = None
        self.end_time_value = QTime(23, 59, 00)
        self.start_time_value = QTime(00, 00, 00)
        self.setWindowTitle("Python ")

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):
        # init Layout
        self.__start_time_layout = QVBoxLayout()
        self.__end_time_layout = QVBoxLayout()
        self.__start_widget = QWidget()
        self.__end_widget = QWidget()

        self.__start_time_label = QLabel("Start time")
        self.__end_time_label = QLabel("End time")

        self.__start_time_edit = QDateTimeEdit()
        self.__start_time_edit.setStyleSheet('''
            QDateTimeEdit {
                border:1px solid #C0DCF2;
                border-radius:3px;
                padding:2px;
                background:none;
                selection-background-color:#386488;
                selection-color:#FFFFFF;
            }

            QDateTimeEdit::up-button {
                image:url(:/src/assets/images/up_arrow.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }

            QDateTimeEdit::down-button {
                image:url(:/src/assets/images/down_arrow.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }
            QDateTimeEdit::down-button:hover, QDateTimeEdit::up-button:hover {
                background-color: #A4D8FD;
            }
        ''')

        self.__start_time_edit.setDisplayFormat("hh:mm:ss")
        self.__start_time_edit.setTime(QTime(00, 00))
        self.__start_time_edit.dateTimeChanged.connect(lambda: self.__st_method())
        self.__end_time_edit = QDateTimeEdit()
        self.__end_time_edit.setStyleSheet('''
            QDateTimeEdit {
                border:1px solid #C0DCF2;
                border-radius:3px;
                padding:2px;
                background:none;
                selection-background-color:#386488;
                selection-color:#FFFFFF;
            }

            QDateTimeEdit::up-button {
                image:url(:/src/assets/images/up_arrow.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }

            QDateTimeEdit::down-button {
                image:url(:/src/assets/images/down_arrow.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }
            QDateTimeEdit::down-button:hover, QDateTimeEdit::up-button:hover {
                background-color: #A4D8FD;
            }
        ''')
        self.__end_time_edit.setDisplayFormat("hh:mm:ss")
        self.__end_time_edit.setTime(QTime(23, 00))
        self.__end_time_edit.dateTimeChanged.connect(lambda: self.__et_method())

        self.__start_time_layout.addWidget(self.__start_time_label)
        self.__start_time_layout.addWidget(self.__start_time_edit)
        self.__start_time_layout.setContentsMargins(0, 0, 0, 0)

        self.__end_time_layout.addWidget(self.__end_time_label)
        self.__end_time_layout.addWidget(self.__end_time_edit)
        self.__end_time_layout.setContentsMargins(0, 0, 0, 0)

        self.__start_widget.setLayout(self.__start_time_layout)
        self.__end_widget.setLayout(self.__end_time_layout)

        self.__main_layout = QHBoxLayout(self)
        self.__main_layout.addWidget(self.__start_widget)
        self.__main_layout.addWidget(self.__end_widget)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def __st_method(self):
        # getting current datetime
        self.start_time_value = self.__start_time_edit.time()

    def __et_method(self):
        # getting current datetime
        self.end_time_value = self.__end_time_edit.time()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     viewer = MonthViewer()
#     viewer.show()
#     sys.exit(app.exec())
