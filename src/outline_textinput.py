import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QListView, QDialog, QVBoxLayout, QListWidget, \
    QListWidgetItem, QAction


class CustomMenu(QMenu):
    showDialogSignal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        action = QAction("Action 1", self)
        action.triggered.connect(self.showDialogSignal.emit)
        self.addAction(action)

    def mouseReleaseEvent(self, event):
        action = self.activeAction()
        if action:
            if isinstance(action.parent(), QListWidget):
                self.showDialog()
                return

        super().mouseReleaseEvent(event)

    def showDialog(self):
        dialog = QDialog(self.parentWidget())
        layout = QVBoxLayout()
        list_widget = QListWidget(dialog)
        for i in range(5):
            item = QListWidgetItem(f"Item {i + 1}")
            list_widget.addItem(item)
        list_widget.itemClicked.connect(dialog.accept)
        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec_()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Menu and Dialog Example')

        self.central_widget = QPushButton('Show Menu', self)
        self.central_widget.setGeometry(100, 100, 150, 30)

        self.central_widget.clicked.connect(self.showContextMenu)

    def showContextMenu(self):
        menu = CustomMenu(self)
        menu.showDialogSignal.connect(menu.showDialog)  # Connect the signal to the showDialog method
        menu.popup(self.central_widget.mapToGlobal(self.central_widget.rect().bottomLeft()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
