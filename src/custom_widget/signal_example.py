import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("0")
        layout.addWidget(self.label)

        self.button_1 = QPushButton("1")
        self.button_1.clicked.connect(lambda: self.append_number("1"))
        layout.addWidget(self.button_1)

        self.button_2 = QPushButton("2")
        self.button_2.clicked.connect(lambda: self.append_number("2"))
        layout.addWidget(self.button_2)

        self.button_plus = QPushButton("+")
        self.button_plus.clicked.connect(lambda: self.perform_operation("+"))
        layout.addWidget(self.button_plus)

        self.button_minus = QPushButton("-")
        self.button_minus.clicked.connect(lambda: self.perform_operation("-"))
        layout.addWidget(self.button_minus)

        self.button_equals = QPushButton("=")
        self.button_equals.clicked.connect(self.calculate_result)
        layout.addWidget(self.button_equals)

        self.setLayout(layout)

        self.current_number = ""
        self.current_operator = None
        self.result = 0

    @Slot()
    def append_number(self, number):
        self.current_number += number
        self.label.setText(self.current_number)

    @Slot()
    def perform_operation(self, operator):
        self.current_operator = operator
        self.result = int(self.current_number)
        self.current_number = ""
        self.label.setText("0")

    @Slot()
    def calculate_result(self):
        if self.current_operator and self.current_number:
            if self.current_operator == "+":
                self.result += int(self.current_number)
            elif self.current_operator == "-":
                self.result -= int(self.current_number)

            self.current_number = ""
            self.current_operator = None
            self.label.setText(str(self.result))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = CalculatorWidget()
    widget.setWindowTitle("Calculator")
    widget.show()

    sys.exit(app.exec())
