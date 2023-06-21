import math
import random

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.root_stackedwidget = QStackedWidget()
        self.root_stackedwidget.addWidget(QWidget())
        self.grid_size = 4
        self.my_dict = {}
        page_index = 0

        string1 = "New String 1"
        string2 = "New String 2"
        # Insert string1 at position 1
        self.my_dict[1] = string1

        # Insert string2 at position 3
        self.my_dict[5] = string2

        layout = QVBoxLayout()
        self.setLayout(layout)

        button1 = QPushButton("Next")
        button1.clicked.connect(self.nextPage)
        button2 = QPushButton("Previous")
        button2.clicked.connect(self.previousPage)
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(button1)
        hBoxLayout.addWidget(button2)

        button3 = QPushButton("2x2")
        button3.clicked.connect(self.Button3Clicked)
        layout.addWidget(button3)

        button5 = QPushButton("3x3")
        button5.clicked.connect(self.Button5Clicked)
        layout.addWidget(button5)

        button4 = QPushButton("4x4")
        button4.clicked.connect(self.Button4Clicked)
        layout.addWidget(button4)
        layout.addLayout(hBoxLayout)

        self.grid = QGridLayout()
        self.root_stackedwidget.widget(page_index).setLayout(self.grid)

        layout.addWidget(self.root_stackedwidget)
        self.labels = []
        self.setupGridLayout()

    def setupGridLayout(self):
        for label in self.labels:
            label.setParent(None)
        self.labels.clear()
        for i in range(self.grid_size):
            row = i // math.sqrt(self.grid_size)
            col = i % math.sqrt(self.grid_size)
            label = QLabel(f"Label {row}-{col}")
            self.labels.append(label)
            for k, label in enumerate(self.labels):
                if k in self.my_dict:
                    label.setText(self.my_dict[k])
            self.grid.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)

    def nextPage(self):
        if self.root_stackedwidget.count() == 1:
            return
        currentIndex = self.root_stackedwidget.currentIndex()
        nextPageIndex = (currentIndex + 1) % self.root_stackedwidget.count()
        self.root_stackedwidget.setCurrentIndex(nextPageIndex)

    def previousPage(self):
        if self.root_stackedwidget.count() == 1:
            return
        currentIndex = self.root_stackedwidget.currentIndex()
        previousPageIndex = (currentIndex - 1) % self.root_stackedwidget.count()
        self.root_stackedwidget.setCurrentIndex(previousPageIndex)

    def Button3Clicked(self):
        self.grid_size = 4
        self.grid.setSizeConstraint(QGridLayout.SetFixedSize)
        self.setupGridLayout()

    def Button5Clicked(self):
        self.grid_size = 9
        self.grid.setSizeConstraint(QGridLayout.SetFixedSize)
        self.setupGridLayout()

    def Button4Clicked(self):
        self.grid_size = 16
        self.grid.setSizeConstraint(QGridLayout.SetFixedSize)
        self.setupGridLayout()

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
