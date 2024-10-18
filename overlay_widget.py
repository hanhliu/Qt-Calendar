import os
import sys

from PySide6.QtCore import QRectF
from PySide6.QtGui import Qt, QPalette, QPainter, QBrush, QColor, QPainterPath, QRegion, QPen
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton, QGridLayout, \
    QDialog, QHBoxLayout


class CtmWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.button = QPushButton("Close Overlay")
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.button)

        self.button.clicked.connect(self.hideOverlay)

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        pen = QPen(Qt.white, 1)
        painter.setPen(pen)
        painter.fillPath(path, Qt.white)
        painter.drawPath(path)
        painter.end()

    def hideOverlay(self):
        self.parent().hide()

class Overlay(QWidget):
    def __init__(self, parent, widget):
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        # palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

        self.widget = widget
        self.widget.setParent(self)


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 127)))
        painter.end()

    def resizeEvent(self, event):
        position_x = (self.frameGeometry().width()-self.widget.frameGeometry().width())/2
        position_y = (self.frameGeometry().height()-self.widget.frameGeometry().height())/2

        self.widget.move(position_x, position_y)
        event.accept()

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(800, 500)

        self.button = QPushButton("Click Me")

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.button)
        self.popup = Overlay(self, CtmWidget())
        self.popup.hide()

        # Connections
        self.button.clicked.connect(self.displayOverlay)

    def displayOverlay(self):
        self.popup.show()
        print( "clicked")

    def resizeEvent(self, event):
        self.popup.resize(event.size())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
