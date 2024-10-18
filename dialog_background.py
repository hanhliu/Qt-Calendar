import os
import sys

from PySide6.QtCore import QEvent, QObject, Signal
from PySide6.QtGui import Qt, QPalette, QPainter, QBrush, QColor
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog

class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        palette = QPalette(self.palette())
        # palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 127)))
        painter.end()

    def resizeEvent(self, event):
        self.resize(self.parent().size())

class BackgroundDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop)
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(400, 300)
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.dialog_monitor = DialogMonitor(self)
        self.dialog_monitor.signal_test.connect(self.show_overlay)
        QApplication.instance().installEventFilter(self.dialog_monitor)
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        self.label = QLabel('HanhLT')
        self.btn_1 = QPushButton('Show Dialog')
        self.btn_1.clicked.connect(self.show_dialog)
        self.btn_2 = QPushButton('Button 2')

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        largest_item = QWidget()
        largest_item.setStyleSheet('background-color: lightblue;')
        grid_layout.addWidget(largest_item, 1, 1, 2, 2)  # Span 3 rows and 3 columns, starting from row 1 and column 1
        self.add_position_label(largest_item, 1, 1)
        for row in range(0, 4):
            for col in range(0, 4):
                if row == 1 and col == 1:
                    continue  # Skip the center item
                item = QWidget()
                item.setStyleSheet('background-color: lightblue;')
                grid_layout.addWidget(item, row, col)

        self.central_layout.addWidget(self.label)
        self.central_layout.addWidget(self.btn_1)
        self.central_layout.addWidget(self.btn_2)
        self.central_layout.addLayout(grid_layout)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # Create the overlay
        self.overlay = Overlay(self)
        self.overlay.hide()

    def show_dialog(self):

        self.dialog = BackgroundDialog(self)
        result = self.dialog.exec()

        if result == QDialog.Accepted:
            print(f"Name entered:")

    def add_position_label(self, item, row, col):
        if row == 1 and col == 1:  # Add label only to the largest item
            label = QLabel(f"Position: ({row}, {col})")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout = QVBoxLayout(item)
            layout.addWidget(label)

    def show_overlay(self, is_show):
        if is_show:
            if self.overlay.isVisible():
                pass
            else:
                self.overlay.show()
        else:
            if not self.overlay.isVisible():
                pass
            else:
                self.overlay.hide()



class DialogMonitor(QObject):
    signal_test = Signal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog_open = False

    def eventFilter(self, obj, event):
        if isinstance(obj, QDialog):
            print(f"HanhLT: Dialog")
            if obj.isVisible():
                self.dialog_open = True
                self.signal_test.emit(self.dialog_open)
                print(f"HanhLT: Show")
            else:
                print(f"HanhLT: Hide")
                self.dialog_open = False
                self.signal_test.emit(self.dialog_open)
            # if event.type() == QEvent.Show:
            #     print(f"HanhLT: Show")
            # elif event.type() == QEvent.Hide:
            #     print(f"HanhLT: Hide")
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
