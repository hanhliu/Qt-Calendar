# rtsp://admin:abcd1234@113.161.47.101/Streaming/channels/102

import sys

import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QStackedWidget, \
    QStackedLayout, QHBoxLayout, QGroupBox
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer, QRect, QPoint, QRectF


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

        self.drawing_enabled = True

        self.draw_color_checkin = (0, 0, 255)  # Blue
        self.draw_color_checkout = (255, 0, 0)  # Red

        self.is_drawing_checkin = False
        self.is_drawing_checkout = False

        self.rectangle_list_checkin = []
        self.rectangle_list_checkout = []
        self.points_checkin = []
        self.points_checkout = []
        self.temp_point_in = []
        self.temp_point_out = []

        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.camera_active = False

        self.selected_point_index = None
        self.mouse_press_pos = None
        self.mouse_move_pos = None

    def allow_draw_checkin(self):
        self.is_drawing_checkin = True
        self.is_drawing_checkout = False

    def allow_draw_checkout(self):
        self.is_drawing_checkin = False
        self.is_drawing_checkout = True

    def clear_shape(self):
        self.points_checkout.clear()  # Reset the points
        self.points_checkin.clear()
        self.is_drawing_checkout = False
        self.is_drawing_checkout = False
        self.rectangle_list_checkout.clear()
        self.rectangle_list_checkin.clear()

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
                for points, is_drawing, draw_color, rectangle_list in [
                    (self.temp_point_in, self.is_drawing_checkin, self.draw_color_checkin, self.rectangle_list_checkin),
                    (self.temp_point_out, self.is_drawing_checkout, self.draw_color_checkout, self.rectangle_list_checkout)
                ]:
                    for rectangle_points in rectangle_list:
                        # Draw previously saved rectangles
                        for i in range(len(rectangle_points) - 1):
                            self.draw_line(rectangle_points[i], rectangle_points[i + 1], draw_color)

                        if len(rectangle_points) % 4 == 0:
                            for i in range(4):
                                self.draw_line(rectangle_points[i], rectangle_points[(i + 1) % 4], draw_color)
                        if is_drawing:
                            for point in rectangle_points:
                                preview_offset_x = self.camera_frame.geometry().x()
                                preview_offset_y = self.camera_frame.geometry().y()

                                scaled_x = int((point[0] - preview_offset_x))
                                scaled_y = int((point[1] - preview_offset_y))

                                cv2.circle(self.current_frame, (scaled_x, scaled_y), 5, (0, 0, 255, 50), -1)

                    # # Draw the current rectangle being drawn
                    for i in range(len(points) - 1):
                        self.draw_line(points[i], points[i + 1], draw_color)

                    if len(points) == 4:
                        for i in range(4):
                            self.draw_line(points[i], points[(i + 1) % 4], draw_color)

                    if is_drawing:
                        for point in points:
                            preview_offset_x = self.camera_frame.geometry().x()
                            preview_offset_y = self.camera_frame.geometry().y()

                            scaled_x = int((point[0] - preview_offset_x))
                            scaled_y = int((point[1] - preview_offset_y))

                            cv2.circle(self.current_frame, (scaled_x, scaled_y), 5, (0, 0, 255, 50), -1)

            temp_pixmap = QPixmap.fromImage(
                QImage(self.current_frame.data, self.current_frame.shape[1], self.current_frame.shape[0],
                       self.current_frame.strides[0], QImage.Format_RGB888))

            self.camera_frame.setPixmap(temp_pixmap)

            frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            qimage = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_frame.setPixmap(QPixmap.fromImage(qimage))

    def toggle_drawing(self):
        self.drawing_enabled = True

    def draw_line(self, start_point, end_point, draw_color):
        scaled_start = (int(start_point[0]), int(start_point[1]))
        scaled_end = (int(end_point[0]), int(end_point[1]))
        cv2.line(self.current_frame, scaled_start, scaled_end, draw_color, 2, cv2.LINE_AA)

    def mousePressEvent(self, event):
        if self.drawing_enabled:
            preview_rect = self.camera_frame.geometry()
            clicked_point = (int(event.position().x()), int(event.position().y()))
            proximity_threshold = 20

            def handle_selection_or_draw(is_drawing, points, temp_point, rectangle_list):
                print("HanhLT: rectangle_list   ",rectangle_list)
                for p in rectangle_list:
                    for point in p:
                        if self.is_point_close(clicked_point, point, proximity_threshold):
                            self.handle_selection(event, p)
                            return
                self.handle_mouse_press(event, points, temp_point, preview_rect, is_drawing, rectangle_list)

            if self.is_drawing_checkin:
                handle_selection_or_draw(self.is_drawing_checkin, self.points_checkin, self.temp_point_in,
                                         self.rectangle_list_checkin)
            elif self.is_drawing_checkout:
                handle_selection_or_draw(self.is_drawing_checkout, self.points_checkout, self.temp_point_out,
                                         self.rectangle_list_checkout)

    def handle_mouse_press(self, event, points, temp_point, preview_rect, is_drawing, rectangle_list):
        if event.button() == Qt.LeftButton and preview_rect.contains(event.position().toPoint()):
            point = (int(event.position().x()), int(event.position().y()))
            temp_point.append(point)

            if len(temp_point) == 4:
                # Call arrange_points and store the result in a variable
                arranged_points = self.arrange_points(temp_point)
                # Update self.points_checkin or self.points_checkout based on the drawing mode
                if is_drawing:
                    points = arranged_points
                # Save the current rectangle's points to the list
                rectangle_list.append(points)
                # Clear the current points to start a new rectangle
                temp_point.clear()

    def handle_selection(self, event, rectangle_points):
        print("HanhLT: rectangle_points   ", rectangle_points)
        self.list_to_move = rectangle_points
        for i, points in enumerate(rectangle_points):
            point_rect = QRect(points[0] - 20, points[1] - 20, 40, 40)
            if point_rect.contains(event.position().toPoint()):
                self.selected_point_index = i
                self.mouse_press_pos = event.position()
                break

    def is_point_close(self, point1, point2, threshold):
        distance = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        return distance <= threshold

    def arrange_points(self, points):
        if len(points) == 4:
            # Calculate the centroid (center point) of the four points
            centroid_x = sum(x for x, y in points) / 4
            centroid_y = sum(y for x, y in points) / 4
            # Sort the points based on their angles relative to the centroid
            sorted_points = sorted(points, key=lambda p: np.arctan2(p[1] - centroid_y, p[0] - centroid_x))
            # Rearrange the points as top-left, top-right, bottom-right, bottom-left
            top_left, top_right, bottom_right, bottom_left = sorted_points
            return [top_left, top_right, bottom_right, bottom_left]

    def mouseMoveEvent(self, event):
        if self.drawing_enabled:
            if self.selected_point_index is not None and self.mouse_press_pos is not None:
                region_limits = QRect(10, 10, self.camera_frame.width() - 10, self.camera_frame.height() - 10)

                if self.is_drawing_checkin:
                    if self.list_to_move in self.rectangle_list_checkin:
                        self.handle_point_movement(event, self.list_to_move, region_limits)

                elif self.is_drawing_checkout:
                    if self.list_to_move in self.rectangle_list_checkout:
                        self.handle_point_movement(event, self.list_to_move, region_limits)

    def handle_point_movement(self, event, points, region_limits):
        if region_limits.contains(event.position().toPoint()):
            dx = int(event.position().x() - self.mouse_press_pos.x())
            dy = int(event.position().y() - self.mouse_press_pos.y())
            new_x = int(points[self.selected_point_index][0] + dx)
            new_y = int(points[self.selected_point_index][1] + dy)

            if region_limits.contains(QPoint(new_x, new_y)):
                points[self.selected_point_index] = (new_x, new_y)
                self.mouse_press_pos = event.position()
                self.update_frame()
                arranged_points = self.arrange_points(points)
                # Update self.points_checkin or self.points_checkout based on the drawing mode
                # if self.is_drawing_checkin:
                #     self.points_checkin = arranged_points
                # elif self.is_drawing_checkout:
                #     self.points_checkout = arranged_points

    def mouseReleaseEvent(self, event):
        if self.drawing_enabled:
            self.selected_point_index = None
            self.mouse_press_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = CameraApp()
    mainWin.show()
    sys.exit(app.exec())


    #         if self.is_drawing_checkin and len(self.points_checkin) == 4:
    #             selected_edge = self.detect_selected_edge(event.position(), self.points_checkin)
    #             # print("HanhLT: selected_edge    ", selected_edge)
    #             if selected_edge is not None:
    #                 self.change_edge_color(selected_edge, self.points_checkin, (0, 255, 0))
    #         elif self.is_drawing_checkout and len(self.points_checkout) == 4:
    #             selected_edge = self.detect_selected_edge(event.position(), self.points_checkout)
    #             if selected_edge is not None:
    #                 self.change_edge_color(selected_edge, self.points_checkout, (0, 255, 0))
    #
    # # Add these helper methods to your class
    # def detect_selected_edge(self, mouse_pos, points):
    #     for i in range(len(points)):
    #         start_point = QPoint(*points[i])
    #         end_point = QPoint(*points[(i + 1) % len(points)])
    #         edge_rect = QRectF(start_point, end_point).normalized().adjusted(-10, -10, 10, 10)  # Adjust for tolerance
    #         if edge_rect.contains(mouse_pos):
    #             return i  # Return the index of the selected edge
    #     return None  # No edge selected
    #
    # def change_edge_color(self, edge_index, points, color):
    #     # Modify the color of the selected edge
    #     start_point = tuple(points[edge_index])
    #     end_point = tuple(points[(edge_index + 1) % len(points)])
    #     # print("HanhLT: start_point   ", start_point,"  end_point  ", end_point)
    #     self.draw_line(start_point, end_point, color)