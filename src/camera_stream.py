# rtsp://admin:abcd1234@113.161.47.101/Streaming/channels/102

import sys

import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QStackedWidget, \
    QStackedLayout, QHBoxLayout, QGroupBox
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer, QRect, QPoint


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera App")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.central_widget.setLayout(self.layout)

        self.stacked_widget = QStackedLayout()
        self.camera_frame = QLabel()

        # add preview camera to layout
        self.stacked_widget.addWidget(self.camera_frame)

        self.layout.addLayout(self.stacked_widget)

        self.button_checkin = QPushButton("Chieu vao")
        self.button_checkin.clicked.connect(self.allow_draw_checkin)
        self.button_checkout = QPushButton("Chieu ra")
        self.button_checkout.clicked.connect(self.allow_draw_checkout)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button_checkin)
        self.hbox.addWidget(self.button_checkout)
        self.layout.addLayout(self.hbox)

        self.start_button = QPushButton("Start Camera")
        self.start_button.clicked.connect(self.start_camera)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Camera")
        self.stop_button.clicked.connect(self.stop_camera)
        self.layout.addWidget(self.stop_button)

        self.draw_button = QPushButton("Draw Shape")
        self.draw_button.clicked.connect(self.toggle_drawing)
        self.layout.addWidget(self.draw_button)

        self.clear_button = QPushButton("CLEAR SHAPE")
        self.clear_button.clicked.connect(self.clear_shape)
        self.layout.addWidget(self.clear_button)

        self.drawing_enabled = False
        # Variables to store the rectangle coordinates
        self.rectangle_start = None
        self.rectangle_end = None

        self.points = []

        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.camera_active = False

        self.selected_point_index = None
        self.mouse_press_pos = None
        self.mouse_move_pos = None

    def allow_draw_checkin(self):
        pass

    def allow_draw_checkout(self):
        pass

    def clear_shape(self):
        self.points = []  # Reset the points
        self.drawing_enabled = False

    def start_camera(self):
        rtsp_url = "rtsp://admin:abcd1234@113.160.187.79/Streaming/channels/102"  # Replace with your RTSP stream URL
        self.capture = cv2.VideoCapture(rtsp_url)
        if not self.capture.isOpened():
            print("Error: Camera not accessible.")
            return

        self.timer.start(30)  # Update frame every 30 ms
        self.camera_active = True

    def stop_camera(self):
        if self.capture:
            self.capture.release()
            self.timer.stop()
            self.camera_active = False
            self.camera_frame.clear()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            self.current_frame = frame.copy()
            if self.drawing_enabled:
                for i in range(len(self.points) - 1):
                    self.draw_line(self.points[i], self.points[i + 1])

                if len(self.points) == 4:
                    for i in range(len(self.points)):
                        self.draw_line(self.points[i], self.points[(i + 1) % 4])

            temp_pixmap = QPixmap.fromImage(
                QImage(self.current_frame.data, self.current_frame.shape[1], self.current_frame.shape[0],
                       self.current_frame.strides[0], QImage.Format_RGB888))

            for point in self.points:
                # Calculate offset of the camera preview within the main window
                preview_offset_x = self.camera_frame.geometry().x()
                preview_offset_y = self.camera_frame.geometry().y()

                # Adjust point coordinates with the offset
                scaled_x = int((point[0] - preview_offset_x))
                scaled_y = int((point[1] - preview_offset_y))

                cv2.circle(self.current_frame, (scaled_x, scaled_y), 5, (0, 0, 255, 50), -1)
            self.camera_frame.setPixmap(temp_pixmap)

            frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            qimage = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_frame.setPixmap(QPixmap.fromImage(qimage))

    def toggle_drawing(self):
        self.drawing_enabled = True

    def draw_line(self, start_point, end_point):
        scaled_start = (int(start_point[0]), int(start_point[1]))
        scaled_end = (int(end_point[0]), int(end_point[1]))

        cv2.line(self.current_frame, scaled_start, scaled_end, (0, 255, 0), 2, cv2.LINE_AA)

    def mousePressEvent(self, event):
        if self.drawing_enabled and len(self.points) < 4:
            if event.button() == Qt.LeftButton:
                preview_rect = self.camera_frame.geometry()

                if preview_rect.contains(event.position().toPoint()):
                    point = (int(event.position().x()), int(event.position().y()))
                    self.points.append(point)
                    # If all four points have been selected, find top-left and bottom-right points
                    if len(self.points) == 4:
                        self.arrange_points()

        if self.drawing_enabled:
            for i, point in enumerate(self.points):
                point_rect = QRect(point[0] - 20, point[1] - 20, 40, 40)
                if point_rect.contains(event.position().toPoint()):
                    self.selected_point_index = i
                    self.mouse_press_pos = event.position()
                    break

    def arrange_points(self):
        if len(self.points) == 4:
            # Calculate the centroid (center point) of the four points
            centroid_x = sum(x for x, y in self.points) / 4
            centroid_y = sum(y for x, y in self.points) / 4

            # Sort the points based on their angles relative to the centroid
            sorted_points = sorted(self.points, key=lambda p: np.arctan2(p[1] - centroid_y, p[0] - centroid_x))

            # Rearrange the points as top-left, top-right, bottom-right, bottom-left
            top_left, top_right, bottom_right, bottom_left = sorted_points

            self.points = [top_left, top_right, bottom_right, bottom_left]

    def mouseMoveEvent(self, event):
        if self.drawing_enabled:
            if self.selected_point_index is not None and self.mouse_press_pos is not None:
                region_limits = QRect(10, 10, self.camera_frame.width() - 10, self.camera_frame.height() - 10)
                if region_limits.contains(event.position().toPoint()):
                    dx = event.position().x() - self.mouse_press_pos.x()
                    dy = event.position().y() - self.mouse_press_pos.y()
                    new_x = self.points[self.selected_point_index][0] + dx
                    new_y = self.points[self.selected_point_index][1] + dy

                    # Ensure that the new point is within the region limits
                    if region_limits.contains(QPoint(new_x, new_y)):
                        self.points[self.selected_point_index] = (new_x, new_y)
                        self.mouse_press_pos = event.position()
                        self.update_frame()
                        self.arrange_points()

    def mouseReleaseEvent(self, event):
        if self.drawing_enabled:
            self.selected_point_index = None
            self.mouse_press_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = CameraApp()
    mainWin.show()
    sys.exit(app.exec())
