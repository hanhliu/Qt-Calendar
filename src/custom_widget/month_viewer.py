import sys
from PySide6.QtCore import QDate, QLocale
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class MonthViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Month Viewer")
        self.current_month = QDate.currentDate().month()
        self.current_year = QDate.currentDate().year()
        self.month_labels = []
        self.setup_ui()

    def setup_ui(self):
        # Create layout for the month labels
        months_layout = QVBoxLayout()

        # Create layout for the navigation buttons
        buttons_layout = QHBoxLayout()

        # Create the navigation buttons
        prev_button = QPushButton("Previous")
        prev_button.clicked.connect(self.previous_months)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_months)

        # Add the navigation buttons to the buttons layout
        buttons_layout.addWidget(prev_button)
        buttons_layout.addWidget(next_button)

        # Create the month labels
        for i in range(4):
            month_label = QLabel()
            self.month_labels.append(month_label)
            months_layout.addWidget(month_label)
            self.update_month_label(i)

        # Create the main layout and add the sub-layouts to it
        main_layout = QVBoxLayout()
        main_layout.addLayout(months_layout)
        main_layout.addLayout(buttons_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def update_month_label(self, index):
        # Calculate the year and month for the label at the given index
        year = self.current_year + (self.current_month + index - 1) // 12
        month = (self.current_month + index - 1) % 12 + 1

        # Create a QDate object for the current month
        date = QDate(year, month, 1)

        # Create a QLocale object for the current locale
        locale = QLocale()

        # Convert the date to a string using the current locale
        month_string = locale.monthName(month)
        year_string = str(year)
        label_text = f"{month_string} {year_string}"

        # Set the label text
        self.month_labels[index].setText(label_text)

    def next_months(self):
        # Increment the current month by 4
        self.current_month += 4
        if self.current_month > 12:
            self.current_month -= 12
            self.current_year += 1

        # Update the month labels
        for i in range(4):
            self.update_month_label(i)

    def previous_months(self):
        # Decrement the current month by 4
        self.current_month -= 4
        if self.current_month < 1:
            self.current_month += 12
            self.current_year -= 1

        # Update the month labels
        for i in range(4):
            self.update_month_label(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MonthViewer()
    viewer.show()
    sys.exit(app.exec())
