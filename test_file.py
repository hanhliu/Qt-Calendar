from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QGraphicsLineItem, QMainWindow, QGraphicsScene, \
    QGraphicsView, QGraphicsProxyWidget, QApplication


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.combo_box = QComboBox()
        self.combo_box.addItem("Option 1")
        self.combo_box.addItem("Option 2")
        layout.addWidget(self.combo_box)
        self.setLayout(layout)


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, start_item, end_item, parent=None):
        super().__init__(parent)
        self.setPen(QPen(Qt.black, 2))
        start_pos = start_item.pos() + QPointF(start_item.boundingRect().width() / 2,
                                               start_item.boundingRect().height() / 2)
        end_pos = end_item.pos() + QPointF(end_item.boundingRect().width() / 2,
                                           end_item.boundingRect().height() / 2)
        self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.custom_widget_1 = CustomWidget()
        self.custom_widget_2 = CustomWidget()

        self.proxy_widget_1 = QGraphicsProxyWidget()
        self.proxy_widget_1.setWidget(self.custom_widget_1)
        self.proxy_widget_1.setPos(100, 100)

        self.proxy_widget_2 = QGraphicsProxyWidget()
        self.proxy_widget_2.setWidget(self.custom_widget_2)
        self.proxy_widget_2.setPos(300, 300)

        self.scene.addItem(self.proxy_widget_1)
        self.scene.addItem(self.proxy_widget_2)

        self.connection_line = ConnectionLine(self.proxy_widget_1, self.proxy_widget_2)
        self.scene.addItem(self.connection_line)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setGeometry(100, 100, 600, 400)
    window.show()
    app.exec()
