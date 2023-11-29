import sys

import PySide6
from PySide6.QtCore import QDate, QLocale, Qt, QTime, QDateTime
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCalendarWidget, \
    QDateTimeEdit, QComboBox, QItemDelegate
from PySide6.QtGui import QTextCharFormat, QPalette, QStandardItemModel, QStandardItem

month_names = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

class ComboBoxUnit(QWidget):
    def __init__(self, list_input=None, type_combo=None):
        super().__init__()
        self.list_input = list_input
        self.type_combo = type_combo
        self.initUI()

    def initUI(self):
        # Create a QComboBox widget
        self.combo_box = QComboBox(self)

        # Create a QStandardItemModel
        model = QStandardItemModel()
        if self.list_input:
            for item in self.list_input:
                item_child = QStandardItem(item)
                model.appendRow(item_child)

        # Set the model for the ComboBox
        self.combo_box.setModel(model)

        if self.type_combo == "months":
            current_month = QDate.currentDate().month()
            self.combo_box.setCurrentIndex(current_month - 1)
        else:
            pass

        # Create a delegate to display icons and text
        delegate = QItemDelegate(self.combo_box)
        self.combo_box.setItemDelegate(delegate)

        # Set a style sheet for the ComboBox
        self.combo_box.setStyleSheet(f'''
            QComboBox {{ 
                background-color: white; 
                border: 1px solid #BBBBBB; border-radius: 2px;
            }}
            QComboBox::drop-down {{
                 background-color: white;
             }}
            
        ''')

        # Connect the ComboBox to a function that handles item selection
        # self.combo_box.activated.connect(self.comboBoxItemSelected)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.combo_box)
        self.setLayout(self.layout)

    def comboBoxItemSelected(self, index):
        # Get the selected item text
        selected_item = self.sender().currentText()

class CustomCalendar(QCalendarWidget):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event: PySide6.QtGui.QWheelEvent) -> None:
        event.ignore()

class MonthViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Month Viewer")
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(self.palette().brush(QPalette.Highlight))
        self.highlight_format.setForeground(self.palette().color(QPalette.HighlightedText))

        self.current_week = QDate.currentDate().weekNumber()
        self.current_month = QDate.currentDate().month()
        self.current_year = QDate.currentDate().year()
        self.sYear = QDate.currentDate().year()
        self.sMonth = QDate.currentDate().toString("MMMM")
        self.sDate = QDate.currentDate().day()
        self.sDateFinal = QDate().currentDate()  # this final date to use

        self.begin_date = QDate().currentDate()
        self.end_date = QDate().currentDate()
        self.start_value = QDateTime()
        self.end_value = QDateTime()
        self.end_time = QTime(23, 59, 00)
        self.start_time = QTime(00, 00, 00)
        self.month_labels = []
        self.year_labels = []
        self.setup_ui()

    def setup_ui(self):
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        self.combobox_month = ComboBoxUnit(list_input=months, type_combo='months')
        self.combobox_month.combo_box.activated.connect(self.on_combo_month_activated)
        current_year = QDate.currentDate().year()
        years = [str(current_year - i) for i in range(5)]
        self.combobox_year = ComboBoxUnit(list_input=years, type_combo='years')
        self.combobox_year.combo_box.activated.connect(self.on_combo_year_activated)

        # QCalendar
        self.calendar = CustomCalendar()
        self.calendar.setCurrentPage(QDate.currentDate().year(), QDate.currentDate().month())
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.setStyleSheet('''
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
        self.calendar.setNavigationBarVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.installEventFilter(self)
        self.calendar.clicked.connect(self.date_is_clicked)
        self.calendar.setToolTip("Giữ phím Shift để chọn khoảng thời gian")

        self.time_picker = TimePickerWidget()

        self.month_year_layout = QHBoxLayout()
        self.month_year_layout.addWidget(self.combobox_month)
        self.month_year_layout.addWidget(self.combobox_year)
        # Create the main layout and add the sub-layouts to it
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.month_year_layout)
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(self.time_picker)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Set the main layout for the widget
        self.setLayout(main_layout)
    def on_combo_month_activated(self):
        selected_month = self.combobox_month.combo_box.currentText()

        self.sMonth = selected_month
        self.sDateFinal = QDate(self.sYear, month_names[self.sMonth], self.sDate)
        self.calendar.setSelectedDate(QDate(self.sYear, month_names[self.sMonth], self.sDate))
    def on_combo_year_activated(self):
        selected_year = self.combobox_year.combo_box.currentText()
        self.sYear = int(selected_year)
        self.sDateFinal = QDate(self.sYear, month_names[self.sMonth], self.sDate)
        self.calendar.setSelectedDate(QDate(self.sYear, month_names[self.sMonth], self.sDate))

    def format_range(self, format):
        if self.begin_date and self.end_date:
            d0 = min(self.begin_date, self.end_date)
            d1 = max(self.begin_date, self.end_date)
            while d0 <= d1:
                self.calendar.setDateTextFormat(d0, format)
                d0 = d0.addDays(1)

    def date_is_clicked(self, date):
        # reset highlighting of previously selected date range
        self.format_range(QTextCharFormat())
        if QApplication.instance().keyboardModifiers() & Qt.ShiftModifier and self.begin_date:
            self.start_value = QDateTime(self.begin_date, self.time_picker.start_time_value)
            self.end_value = QDateTime(self.end_date, self.time_picker.end_time_value)
            if self.begin_date < date:
                self.setEndDate(date)
            elif self.begin_date > date:
                self.setEndDate(self.begin_date)
                self.begin_date = date
            else:
                print("date1 and date2 are the same")

            # set high lighting of currently    selected date range
            self.format_range(self.highlight_format)
        else:
            # self.begin_date = date
            # self.end_date = date
            self.setStartDate(date)
            self.setEndDate(date)

    def getStartDate(self):
        return self.begin_date

    def getEndDate(self):
        return self.end_date

    def setStartDate(self, date):
        self.begin_date = date
        return self.begin_date

    def setEndDate(self, date):
        self.end_date = date
        return self.end_date

    def getStartTime(self):
        self.start_time = self.time_picker.start_time_value
        return self.start_time

    def getEndTime(self):
        self.end_time = self.time_picker.end_time_value
        return self.end_time

    def getStartValue(self):
        return QDateTime(
            self.begin_date, self.time_picker.start_time_value)

    def getEndValue(self):
        return QDateTime(
            self.end_date, self.time_picker.end_time_value)

class TimePickerWidget(QWidget):

    def __init__(self):
        super().__init__()

        # setting title
        self.main_layout = None
        self.end_time_edit = None
        self.start_time_edit = None
        self.end_time_label = None
        self.start_time_label = None
        self.end_widget = None
        self.start_widget = None
        self.end_time_layout = None
        self.start_time_layout = None
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
        self.start_time_layout = QVBoxLayout()
        self.end_time_layout = QVBoxLayout()
        self.start_widget = QWidget()
        self.end_widget = QWidget()

        self.start_time_label = QLabel("Start time")
        self.end_time_label = QLabel("End time")

        self.start_time_edit = QDateTimeEdit()
        self.start_time_edit.setStyleSheet('''
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

        self.start_time_edit.setDisplayFormat("hh:mm:ss")
        self.start_time_edit.setTime(QTime(00, 00))
        self.start_time_edit.dateTimeChanged.connect(lambda: self.st_method())
        self.end_time_edit = QDateTimeEdit()
        self.end_time_edit.setStyleSheet('''
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
        self.end_time_edit.setDisplayFormat("hh:mm:ss")
        self.end_time_edit.setTime(QTime(23, 00))
        self.end_time_edit.dateTimeChanged.connect(lambda: self.et_method())

        self.start_time_layout.addWidget(self.start_time_label)
        self.start_time_layout.addWidget(self.start_time_edit)
        self.start_time_layout.setContentsMargins(0, 0, 0, 0)

        self.end_time_layout.addWidget(self.end_time_label)
        self.end_time_layout.addWidget(self.end_time_edit)
        self.end_time_layout.setContentsMargins(0, 0, 0, 0)

        self.start_widget.setLayout(self.start_time_layout)
        self.end_widget.setLayout(self.end_time_layout)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.start_widget)
        self.main_layout.addWidget(self.end_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)

    def st_method(self):
        # getting current datetime
        self.start_time_value = self.start_time_edit.time()

    def et_method(self):
        # getting current datetime
        self.end_time_value = self.end_time_edit.time()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MonthViewer()
    viewer.show()
    sys.exit(app.exec())
