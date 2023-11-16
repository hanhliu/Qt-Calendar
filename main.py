import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QDate

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Month and Year Selection')
        self.setGeometry(100, 100, 400, 200)

        self.month_combo = QComboBox()
        self.year_combo = QComboBox()

        # Add months to the month combo box
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        self.month_combo.addItems(months)
        current_month = QDate.currentDate().month()
        self.month_combo.setCurrentIndex(current_month - 1)

        # Add years to the year combo box (5 years before and 5 years after the current year)
        current_year = QDate.currentDate().year()
        years = [str(current_year - i) for i in range(5)]
        self.year_combo.addItems(years)

        self.label = QLabel("Selected Date: ")

        layout = QVBoxLayout()
        layout.addWidget(self.month_combo)
        layout.addWidget(self.year_combo)
        layout.addWidget(self.label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.month_combo.activated[str].connect(self.on_combo_activated)
        self.year_combo.activated[str].connect(self.on_combo_activated)

    def on_combo_activated(self, text):
        selected_month = self.month_combo.currentText()
        selected_year = self.year_combo.currentText()
        self.label.setText(f"Selected Date: {selected_month} {selected_year}")

def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
