from PySide6 import QtCore
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QSplitter, QTextEdit, QVBoxLayout, QToolButton, QApplication, QSizePolicy, \
    QLabel, QMainWindow, QMenu, QMenuBar

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(400, 200)
        self.centralWidget = QLabel(f"&Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        self._createMenuBar()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")

        self.newAction = QAction("New")
        self.newAction.setShortcut("Ctrl+N")
        fileMenu.addAction(self.newAction)
        self.open_action = QAction("Open")
        self.open_action.setShortcut("Ctrl+O")
        fileMenu.addAction(self.open_action)
        fileMenu.addSeparator()
        fileMenu.addAction("Saveeeeeeeeeeeee")
        fileMenu.addAction("Exit")

        editMenu.addAction("Cut")
        editMenu.addAction("Copy")
        editMenu.addAction("Paste")

        helpMenu.addAction("About")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
