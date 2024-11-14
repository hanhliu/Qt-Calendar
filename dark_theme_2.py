import sys
import re
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QColor, QPalette, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QStackedWidget,
    QLineEdit, QTextEdit, QHBoxLayout, QApplication, QTableWidgetItem, QTableWidget, QDialog, QMessageBox
)

class ThemeSwitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Initialize widgets
        self.init_widgets()

        # Set initial theme to light
        self.is_dark_theme = False
        # self.apply_light_theme()

        # Set up the main window
        self.setWindowTitle("Theme Switcher App")
        self.setMinimumWidth(600)

    def init_widgets(self):
        # Theme switch button
        self.theme_switch_button = QPushButton("Switch to Dark Theme")
        self.theme_switch_button.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_switch_button)

        # ComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])

        self.layout.addWidget(QLabel("ComboBox:"))
        self.layout.addWidget(self.combo_box)

        # LineEdit
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter text here...")
        self.layout.addWidget(QLabel("LineEdit:"))
        self.layout.addWidget(self.line_edit)

        # TextEdit (multi-line text box)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter multiline text here...")
        self.layout.addWidget(QLabel("TextEdit:"))
        self.layout.addWidget(self.text_edit)

        # Buttons
        self.button1 = QPushButton("Button 1")
        self.button1.setObjectName('button_1')
        # self.button1.setIcon(QIcon('assets/close.svg'))
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.button4 = QPushButton()
        self.button4.setIcon(QIcon('assets/normal_window.svg'))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        button_layout.addWidget(self.button4)
        self.layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setRowCount(4)  # Set number of rows
        self.table.setColumnCount(3)  # Set number of columns
        self.table.setHorizontalHeaderLabels(["Name", "Age", "City"])

        # Add data to the table
        data = [
            ("John Doe", "28", "New York"),
            ("Jane Smith", "34", "London"),
            ("Mike Johnson", "45", "Sydney"),
            ("Anna Lee", "23", "Tokyo"),
        ]

        for row, (name, age, city) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(age))
            self.table.setItem(row, 2, QTableWidgetItem(city))

        # Connect cell click signal to a custom slot
        self.table.cellClicked.connect(self.cell_clicked)
        self.layout.addWidget(self.table)

        # stacked widget
        self.stacked_widget = QStackedWidget()
        self.btn1 = QPushButton('HanhLT 1')
        self.btn1.clicked.connect(self.showDialog)
        self.stacked_widget.addWidget(self.btn1)

        widget_test = QWidget()
        widget_test.setObjectName('widget_test')
        layout_test = QVBoxLayout()
        widget_test.setLayout(layout_test)
        layout_test.addWidget(self.stacked_widget)

        self.layout.addWidget(widget_test)

    def showDialog(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Dialog")
        msg_box.setText("Hello! This is a dialog box.")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        # Show the dialog and check the response
        response = msg_box.exec()


    def cell_clicked(self, row, column):
        # Get the clicked cell's content
        item = self.table.item(row, column)
        if item is not None:
            print(f"Clicked on cell ({row}, {column}): {item.text()}")

    def toggle_theme(self):
        # Switch between light and dark theme
        if self.is_dark_theme:
            current_theme = "light"
            apply_stylesheet(app, current_theme)
            self.theme_switch_button.setText("Switch to Dark Theme")
        else:
            current_theme = "dark"
            apply_stylesheet(app, current_theme)
        self.is_dark_theme = not self.is_dark_theme

    def apply_light_theme(self):
        app.setPalette(get_lightModePalette())

    def apply_dark_theme(self):
        app.setPalette(get_darkModePalette())

def preprocess_qss(variables_file, qss_file):
    # Đọc các biến từ variables.txt
    variables = {}
    with open(variables_file, 'r') as var_file:
        for line in var_file:
            match = re.match(r"@(\w+)\s*=\s*(.+)", line.strip())
            if match:
                key, value = match.groups()
                variables[key] = value

    # Đọc file qss và thay thế các biến
    with open(qss_file, 'r') as qss:
        stylesheet = qss.read()
        for key, value in variables.items():
            stylesheet = stylesheet.replace(f"@{key}", value)

    return stylesheet

def apply_stylesheet(app, theme):
    # stylesheet = preprocess_qss(variables_file, qss_file)
    # app.setStyleSheet(stylesheet)

    if theme == "dark":
        qss_file = "assets/qss/dark/dark_theme.qss"
        variables_file = "assets/qss/dark/dark_color.txt"
    else:
        qss_file = "assets/qss/light/light_theme.qss"
        variables_file = "assets/qss/light/light_theme.txt"

    stylesheet = preprocess_qss(variables_file, qss_file)
    app.setStyleSheet(f"{stylesheet}")


# def apply_stylesheet(app, theme):
    # if theme == "dark":
    #     qss_file = "assets/qss/dark/dark_theme.qss"
    # else:
    #     qss_file = "assets/qss/light/light_theme.qss"

    # file = QFile(qss_file)
    # if not file.open(QFile.ReadOnly | QFile.Text):
    #     print(f"Unable to open file: {qss_file}")
    #     return

    # stream = QTextStream(file)
    # stylesheet = stream.readAll()
    # app.setStyleSheet(stylesheet)
    # file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "light") 
    # app.setStyle("Fusion")
    window = ThemeSwitcherApp()

    window.show()
    sys.exit(app.exec())