import sys

from PySide6.QtGui import QImage
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QMainWindow, QStackedWidget, \
    QStackedLayout, QPushButton


class TestStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.uiAnh1()
        self.uiAnh2()

        # start add ui to StackedWidget
        self.addWidget(self.widget_anh2)  # Cái này index = 0
        self.addWidget(self.widget_anh1)  # Cái này index = 1

        # Muốn cho hiển thị Ui ảnh 1 nên phải setIndext, nếu ko set thì cái nào add vào trước nó sẽ hiển thị
        # Ở đây nó sẽ hiển thị Ui ảnh 2 vì mình add vào trước mà
        self.setCurrentIndex(1)  # Nhớ chỗ này để hiểu logic bên dưới

    def onHandleBuoc3(self):
        self.setCurrentIndex(0)  # Hiển thị Ui ảnh 2

    def uiAnh1(self):
        # create widget and layou
        self.widget_anh1 = QWidget()
        self.layout_anh1 = QVBoxLayout()

        # create child widget
        self.button1 = QPushButton("Bước 1")
        self.button2 = QPushButton("Bước 2")
        self.button3 = QPushButton("Bước 3")
        self.button3.clicked.connect(self.onHandleBuoc3)
        self.button4 = QPushButton("Bước 4")

        # add widget to layout
        self.layout_anh1.addWidget(self.button1)
        self.layout_anh1.addWidget(self.button2)
        self.layout_anh1.addWidget(self.button3)
        self.layout_anh1.addWidget(self.button4)

        #set layout to widget
        self.widget_anh1.setLayout(self.layout_anh1)

    def uiAnh2(self):
        self.widget_anh2 = QWidget()
        self.layout_anh2 = QVBoxLayout()

        # create child widget
        self.open1 = QPushButton("Open 1")
        self.open2 = QPushButton("Open 2")
        self.open3 = QPushButton("Open 3")

        # add widget to layout
        self.layout_anh2.addWidget(self.open1)
        self.layout_anh2.addWidget(self.open2)
        self.layout_anh2.addWidget(self.open3)

        # set layout to widget
        self.widget_anh2.setLayout(self.layout_anh2)

class StackedApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.test_stacked_widget = TestStackedWidget()
        self.layout.addWidget(self.test_stacked_widget)
        self.central_widget.setLayout(self.layout)

    def show_dialog(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StackedApp()
    main_window.show()
    sys.exit(app.exec())