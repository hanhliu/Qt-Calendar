from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction, QDialog, QLabel

class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Application")
        self.button = QPushButton("Show Menu", self)
        self.button.clicked.connect(self.show_menu)
        self.setCentralWidget(self.button)
        self.menu = None  # Track the menu

    def show_menu(self):
        if self.menu is None:
            self.menu = QMenu(self)
            action1 = QAction("Option 1", self)
            action2 = QAction("Option 2", self)
            self.menu.addAction(action1)
            self.menu.addAction(action2)
            action1.triggered.connect(lambda: self.show_dialog(1))
            action2.triggered.connect(lambda: self.show_dialog(2))
        self.menu.exec_(self.button.mapToGlobal(self.button.rect().bottomLeft()))

    def show_dialog(self, option):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Option {option} Dialog")
        label = QLabel(f"Option {option} selected!", dialog)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication([])
    window = MyApplication()
    window.show()
    app.exec_()