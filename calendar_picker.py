import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCalendarWidget
from PySide6.QtCore import QDate

class CalendarExample(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Styled Calendar Example")

        # Layout
        layout = QVBoxLayout()

        # Create calendar widget
        self.calendar = QCalendarWidget(self)

        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.LongDayNames)
        self.calendar.setGridVisible(True)  # Show grid

        # Set custom stylesheet
        self.set_calendar_style()

        # Create label to show the selected date
        self.date_label = QLabel(self)
        self.date_label.setText("Selected date: " + self.calendar.selectedDate().toString())

        # Add widgets to layout
        layout.addWidget(self.calendar)
        layout.addWidget(self.date_label)

        # Connect signal for date selection change
        self.calendar.selectionChanged.connect(self.update_label)

        self.setLayout(layout)

    def set_calendar_style(self):
        stylesheet = """
        QCalendarWidget {
            background-color: #f0f0f0;  /* Background of the calendar */
            border: 1px solid #d4d4d4;  /* Border around the calendar */
            font-family: Arial, sans-serif;
        }

        /* Styling the navigation bar (year and month) */
        QCalendarWidget QToolButton {
            background-color: #4CAF50;   /* Header button background */
            color: white;                /* Header button text color */
            border: none;
            font-size: 16px;
            margin: 5px;
            padding: 5px;
        }

        /* Styling the left and right arrow buttons */
        QCalendarWidget QToolButton#qt_calendar_prevmonth {
            qproperty-icon: url(left-arrow.png); /* You can customize arrow icons if you have them */
        }

        QCalendarWidget QToolButton#qt_calendar_nextmonth {
            qproperty-icon: url(right-arrow.png);
        }

        QCalendarWidget QTableView {
            background-color: white;   /* Background for the whole table (weekdays included) */
        }
        
        QCalendarWidget QTableView QHeaderView::section {
            background-color: red;     /* Background for the weekday headers */
            color: white;              /* Text color for the weekday headers */
            font-weight: bold;
            padding: 5px;
        }
        /* Styling the individual date cells */
        QCalendarWidget QWidget {
            background-color: #ffffff;  /* Default date cell background */
        }

        /* Styling the selected date */
        QCalendarWidget QAbstractItemView:enabled:selected {
            background-color: #FF5722;  /* Background color for the selected date */
            color: white;               /* Text color for the selected date */
        }

        /* Styling today's date */
        QCalendarWidget QAbstractItemView:enabled {
            selection-background-color: #FF9800;  /* Background for today's date */
            color: black;  /* Text color for today's date */
        }
        """
        self.calendar.setStyleSheet(stylesheet)

    def update_label(self):
        # Update label text when a date is selected
        selected_date = self.calendar.selectedDate()
        self.date_label.setText(f"Selected date: {selected_date.toString()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CalendarExample()
    window.show()

    sys.exit(app.exec())
