import sys

from PySide6.QtCore import QRectF, QLineF, Qt, QPoint
from PySide6.QtGui import QColor, QPainterPath, QPainter, QPen, QBrush
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsItem, QGraphicsScene, QApplication, \
    QGraphicsView, QWidget, QVBoxLayout, QMainWindow, QGraphicsProxyWidget, QLabel


class Connection(QGraphicsLineItem):
    def __init__(self, start, p2):
        super().__init__()
        self.start = start
        self.end = None
        self._line = QLineF(start.scenePos(), p2)
        self.setLine(self._line)

    def controlPoints(self):
        return self.start, self.end

    def setP2(self, p2):
        self._line.setP2(p2)
        self.setLine(self._line)

    def setStart(self, start):
        self.start = start
        self.updateLine()

    def setEnd(self, end):
        self.end = end
        self.updateLine(end)

    def updateLine(self, source):
        if source == self.start:
            self._line.setP1(source.scenePos())
        else:
            self._line.setP2(source.scenePos())
        self.setLine(self._line)


class ControlPoint(QGraphicsEllipseItem):
    def __init__(self, parent, onLeft):
        super().__init__(-5, -5, 10, 10, parent)
        self.onLeft = onLeft
        self.lines = []
        # this flag **must** be set after creating self.lines!
        self.setFlags(self.GraphicsItemFlag.ItemSendsScenePositionChanges)

    def addLine(self, lineItem):
        for existing in self.lines:
            if existing.controlPoints() == lineItem.controlPoints():
                # another line with the same control points already exists
                return False
        self.lines.append(lineItem)
        return True

    def removeLine(self, lineItem):
        for existing in self.lines:
            if existing.controlPoints() == lineItem.controlPoints():
                self.scene().removeItem(existing)
                self.lines.remove(existing)
                return True
        return False

    def itemChange(self, change, value):
        for line in self.lines:
            line.updateLine(self)
        return super().itemChange(change, value)


class CustomItem(QGraphicsItem):
    pen = QPen(Qt.red, 2)
    brush = QBrush(QColor(31, 176, 224))
    controlBrush = QBrush(QColor(214, 13, 36))
    rect = QRectF(0, 0, 100, 100)

    def __init__(self, widget, edges=None, number_test=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if edges is None:
            edges = ["left", "top", "right", "bottom"]
        self.edges = edges
        self.widget = widget
        self.number_test = number_test
        self.init_ui()

    def init_ui(self):
        self.proxy_widget = QGraphicsProxyWidget(self)
        self.proxy_widget.setWidget(self.widget)
        self.setFlags(self.GraphicsItemFlag.ItemIsMovable)

        self.controls = []

        for edge in self.edges:
            control = ControlPoint(self, edge)
            self.controls.append(control)
            control.setPen(self.pen)
            control.setBrush(self.controlBrush)
            if edge == "left":
                control.setY(45)
            elif edge == "top":
                control.setX(45)
            elif edge == "right":
                control.setX(100)
                control.setY(45)
            elif edge == "bottom":
                control.setY(100)
                control.setX(45)

    def boundingRect(self):
        adjust = self.pen.width() / 2
        return self.rect.adjusted(-adjust, -adjust, adjust, adjust)

    def paint(self, painter, option, widget=None):
        painter.save()
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.rect, 4, 4)
        painter.drawText(QPoint(10, self.rect.height()/2), self.number_test)
        painter.restore()


class Scene(QGraphicsScene):
    startItem = newConnection = None

    def controlPointAt(self, pos):
        mask = QPainterPath()
        mask.setFillRule(Qt.WindingFill)
        for item in self.items(pos):
            if mask.contains(pos):
                # ignore objects hidden by others
                return
            if isinstance(item, ControlPoint):
                return item
            if not isinstance(item, Connection):
                mask.addPath(item.shape().translated(item.scenePos()))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.controlPointAt(event.scenePos())
            if item:
                self.startItem = item
                self.newConnection = Connection(item, event.scenePos())
                self.addItem(self.newConnection)
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.newConnection:
            item = self.controlPointAt(event.scenePos())
            if item and item != self.startItem and self.startItem.onLeft != item.onLeft:
                p2 = item.scenePos()
            else:
                p2 = event.scenePos()
            self.newConnection.setP2(p2)
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.newConnection:
            item = self.controlPointAt(event.scenePos())
            if item and item != self.startItem:
                self.newConnection.setEnd(item)
                if self.startItem.addLine(self.newConnection):
                    item.addLine(self.newConnection)
                else:
                    # delete the connection if it exists; remove the following
                    # line if this feature is not required
                    self.startItem.removeLine(self.newConnection)
                    self.removeItem(self.newConnection)
            else:
                self.removeItem(self.newConnection)
        self.startItem = self.newConnection = None
        super().mouseReleaseEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        lay = QVBoxLayout(central_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        self.label1 = QLabel("Label 1")
        self.label2 = QLabel("Label 2")
        self.label3 = QLabel("Label 3")
        self.label4 = QLabel("Label 4")

        self.scene = Scene()

        item1 = CustomItem(number_test="Camera 1", widget=self.label1)
        self.scene.addItem(item1)

        item2 = CustomItem(number_test="Camera 2", widget=self.label2)
        self.scene.addItem(item2)

        item3 = CustomItem(number_test="Camera 3", widget=self.label3)
        self.scene.addItem(item3)

        item4 = CustomItem(number_test="Camera 4", widget=self.label4)
        self.scene.addItem(item4)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(QPainter.Antialiasing)
        lay.addWidget(self.view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.exit(app.exec())


# def main():
#     import sys
#     app = QApplication(sys.argv)
#     scene = Scene()
#
#     scene.addItem(CustomItem(left=True, top=True))
#     scene.addItem(CustomItem(left=True, right=True))
#
#     scene.addItem(CustomItem(right=True, bottom=True))
#     scene.addItem(CustomItem(right=True))
#
#     view = QGraphicsView(scene)
#     view.setRenderHints(QPainter.Antialiasing)
#
#     view.show()
#
#     sys.exit(app.exec())
