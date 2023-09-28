import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen
from PySide6.QtCore import Qt


class ImageDrawApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Drawing App")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.central_widget.setLayout(self.layout)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.points_enabled = False

        self.clear_button = QPushButton("CLEAR SHAPE")
        self.clear_button.clicked.connect(self.clear_shape)
        self.layout.addWidget(self.clear_button)

        self.draw_button = QPushButton("DRAW SHAPE")
        self.draw_button.clicked.connect(self.enable_drawing)
        self.layout.addWidget(self.draw_button)


        self.points = []
        self.load_image("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/login_b.png")  # Replace with the path to your image
        self.image_label.setPixmap(QPixmap.fromImage(self.qimage))

    def enable_drawing(self):
        self.points_enabled = True
        self.draw_button.setEnabled(False)

    def enterEvent(self, event) -> None:
        self.image_label.setCursor(Qt.CursorShape.CrossCursor)

    def clear_shape(self):
        self.points = []  # Reset the points
        self.draw_points()  # Clear the drawn points
        self.draw_shape()  # Clear the drawn shape
        self.points_enabled = False  # Disable point picking
        self.draw_button.setEnabled(True)

    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        bytes_per_line = channels * width
        self.qimage = QImage(image_rgb.data, 1080, 681, bytes_per_line, QImage.Format_RGB888)

        self.image_label.setPixmap(QPixmap.fromImage(self.qimage))

    def mousePressEvent(self, event):
        if self.points_enabled and event.button() == Qt.LeftButton and len(self.points) < 4:
            point = (event.pos().x(), event.pos().y())
            self.points.append(point)
            self.draw_points()

            if len(self.points) == 4:
                print("HanhLT: self.point  ", self.points)
                self.draw_shape()  # Draw the shape once all four points are picked

    def draw_points(self):
        if self.qimage is not None:
            image_copy = self.qimage.copy()
            painter = QPainter(image_copy)
            pen = QPen(Qt.green)
            pen.setWidth(4)
            painter.setPen(pen)
            for point in self.points:
                painter.drawPoint(*point)
            painter.end()
            self.image_label.setPixmap(QPixmap.fromImage(image_copy))

    def draw_shape(self):
        image_copy = self.qimage.copy()  # Create a copy of the original image
        cv_image = self.convert_qpixmap_to_cvimage(QPixmap.fromImage(image_copy))  # Convert QPixmap to NumPy array
        num_points = len(self.points)
        # Draw lines connecting the points in order
        for i in range(num_points):
            pt1, pt2 = self.points[i], self.points[(i + 1)% num_points]
            cv2.line(cv_image, pt1, pt2, (0, 255, 0), 2)
            # Connect the last point to the first point to close the shape
            cv2.line(cv_image, pt1, pt2, (0, 255, 0), 1)

        image_copy = self.convert_cvimage_to_qimage(cv_image)  # Convert NumPy array to QImage
        self.image_label.setPixmap(QPixmap.fromImage(image_copy))

    def convert_cvimage_to_qimage(self, cv_image):
        height, width, channels = cv_image.shape
        bytes_per_line = channels * width
        qimage = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_ARGB32)
        return qimage

    def convert_qpixmap_to_cvimage(self, qpixmap):
        qimage = qpixmap.toImage()
        buffer = qimage.constBits()
        width, height = qimage.width(), qimage.height()
        cv_image = np.array(buffer).reshape(height, width, 4).copy()  # Copy data to a NumPy array
        return cv_image


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ImageDrawApp()
    mainWin.show()
    sys.exit(app.exec())
