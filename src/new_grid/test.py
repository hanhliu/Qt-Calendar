import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
from PyQt5.QtGui import QPolygonF, QFont, QColor
from PyQt5.QtCore import Qt, QPointF


class RectangleItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height, index_text):
        super().__init__(x, y, width, height)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        # Thêm văn bản chỉ số
        self.index_text = QGraphicsTextItem(str(index_text), self)
        font = QFont()
        font.setPointSize(12)
        self.index_text.setFont(font)
        self.index_text.setDefaultTextColor(Qt.blue)
        self.index_text.setPos(x + width / 2 - 10, y + height / 2 - 10)

class GridExample(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Tạo grid 3x3 với các hình chữ nhật và chỉ số
        for i in range(3):
            for j in range(3):
                rect = RectangleItem(j * 100, i * 100, 100, 100, (i, j))
                self.scene.addItem(rect)

        self.current_polygon = None
        self.incomplete_rectangles = []
        self.points = []  # Add this line to initialize the points list

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.points.append(self.mapToScene(event.pos()))
            self.update_polygon()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.points.append(self.mapToScene(event.pos()))
            self.update_polygon()

    def mouseReleaseEvent(self, event):
        print("HanhLT: mouse release  ")
        if event.button() == Qt.LeftButton:
            self.points.append(self.mapToScene(event.pos()))
            self.update_polygon()
            self.points = []
            self.print_unfinished_rectangles()

    def update_polygon(self):
        if self.current_polygon is not None:
            self.scene.removeItem(self.current_polygon)

        if len(self.points) > 1:
            self.current_polygon = RectangleItem(
                self.points[0].x(),
                self.points[0].y(),
                self.points[-1].x() - self.points[0].x(),
                self.points[-1].y() - self.points[0].y(),
                ""
            )
            self.scene.addItem(self.current_polygon)
            self.incomplete_rectangles.append(self.current_polygon)
        print("HanhLT: self.scene   ", self.scene)

    def print_unfinished_rectangles(self):
        list_test = []
        for item in self.incomplete_rectangles:
            for grid_item in self.scene.items():
                if (
                    isinstance(grid_item, RectangleItem)
                    and grid_item is not item
                    and item.collidesWithItem(grid_item)
                ):
                    if grid_item.index_text.toPlainText() not in list_test:
                        list_test.append(grid_item.index_text.toPlainText())

        print("HanhLT: list_test   ", list_test)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GridExample()
    ex.show()
    sys.exit(app.exec_())
