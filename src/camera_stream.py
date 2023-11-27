# rtsp://admin:abcd1234@113.161.47.101/Streaming/channels/102

import sys
from typing import List

import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget,  QStackedLayout, QHBoxLayout
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer, QRect, QPoint, QRectF

from draw_shape_model import DrawShapModel, ArrowModel, ShapeType


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.temp_rect = None
        self.temp_shape_model: DrawShapModel = None
        self.draw_shape_to_move: DrawShapModel = None

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
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_click)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button_checkin)
        self.hbox.addWidget(self.button_checkout)
        self.hbox.addWidget(self.save_button)
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

        self.draw_color_checkin = (0, 0, 255)  # Blue
        self.draw_color_checkout = (255, 0, 0)  # Red

        self.is_drawing_checkin = False
        self.is_drawing_checkout = False

        self.list_draw_shape_model: List[DrawShapModel] = []

        self.temp_points = []
        self.temp_line = []
        self.shape_type: ShapeType = ShapeType.ZONE_IN
        self.arrow_model: ArrowModel = ArrowModel()

        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.camera_active = False

        self.selected_point_index = None
        self.mouse_press_pos = None
        self.mouse_move_pos = None

    def save_click(self):
        for item in self.list_draw_shape_model:
            print("HanhLT: self.list_draw_shape_model   ", item.rect)
        draw_shape_model: DrawShapModel = self.temp_shape_model
        # rect = self.temp_points
        # line = self.temp_line
        # color = self.draw_color
        # arrow = ArrowModel(self.midpoint_temp, self.arrow_x, self.arrow_y, self.arrow_color, self.arrow_image)
        # shape_type = self.shape_type
        #
        # draw_shape_model: DrawShapModel = DrawShapModel(rect, line, arrow, color, shape_type)

    def allow_draw_checkin(self):
        self.drawing_enabled = True
        self.is_drawing_checkin = True
        self.is_drawing_checkout = False

    def allow_draw_checkout(self):
        self.drawing_enabled = True
        self.is_drawing_checkin = False
        self.is_drawing_checkout = True

    def clear_shape(self):
        self.drawing_enabled = False
        self.is_drawing_checkin = False
        self.is_drawing_checkout = False

        self.temp_points.clear()
        self.list_draw_shape_model.clear()
        self.temp_line.clear()

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
                for item_shape_model in self.list_draw_shape_model:
                    item_shape_model: DrawShapModel
                    if item_shape_model is not None:
                        # Draw previously saved rectangles
                        for i in range(len(item_shape_model.rect) - 1):
                            self.draw_line(item_shape_model.rect[i], item_shape_model.rect[i + 1],
                                           item_shape_model.color_line)

                        if len(item_shape_model.rect) % 4 == 0:
                            for i in range(4):
                                self.draw_line(item_shape_model.rect[i], item_shape_model.rect[(i + 1) % 4],
                                               item_shape_model.color_line)

                        # print('item_shape_model.line: ', item_shape_model.line, ' - item_shape_model.arrow: ',
                        #       item_shape_model.arrow)
                        if item_shape_model.line and item_shape_model.arrow:
                            self.draw_arrows_for_rectangles(self.current_frame, item_shape_model.line[0],
                                                            item_shape_model.line[1], item_shape_model.arrow.midpoint,
                                                            (0, 255, 0), item_shape_model)


                        for point in item_shape_model.rect:
                            preview_offset_x = self.camera_frame.geometry().x()
                            preview_offset_y = self.camera_frame.geometry().y()

                            scaled_x = int((point[0] - preview_offset_x))
                            scaled_y = int((point[1] - preview_offset_y))
                            cv2.circle(self.current_frame, (scaled_x, scaled_y), 5, item_shape_model.color_point, -1)

                for i in range(len(self.temp_points)):
                    point = self.temp_points[i]
                    # # Draw the current rectangle being drawn
                    if len(self.temp_points) == 4:
                        color = (0, 255, 0) if self.is_drawing_checkin else (0, 0, 255)
                        self.draw_line(self.temp_points[i], self.temp_points[(i + 1) % 4], color)
                    elif len(self.temp_points) >= 2 and (i + 1) < len(self.temp_points):
                        color = (0, 255, 0) if self.is_drawing_checkin else (0, 0, 255)
                        self.draw_line(self.temp_points[i], self.temp_points[i + 1], color)

                    preview_offset_x = self.camera_frame.geometry().x()
                    preview_offset_y = self.camera_frame.geometry().y()

                    scaled_x = int((point[0] - preview_offset_x))
                    scaled_y = int((point[1] - preview_offset_y))

                    if self.is_drawing_checkin:
                        cv2.circle(self.current_frame, (scaled_x, scaled_y), 5, (255, 0, 0), -1)
                    elif self.is_drawing_checkout:
                        cv2.circle(self.current_frame, (scaled_x, scaled_y), 5, (255, 255, 0), -1)

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

            def handle_selection_or_draw(is_drawing, list_draw_shape_model, color_line, shape_draw_type, point_color):
                on_edge = False  # Flag to check if the click is on an edge

                for p in list_draw_shape_model:
                    for point in p.rect:
                        if self.is_point_close(clicked_point, point, proximity_threshold):
                            self.handle_selection(event, p)
                            return
                    if self.detect_selected_edge(event.position(), p) is not None:
                        on_edge = True
                        self.change_edge_color_and_draw_arrow(self.detect_selected_edge(event.position(), p), p.rect, model=p)

                if not on_edge:
                    self.handle_mouse_press(event, preview_rect, is_drawing, list_draw_shape_model, color_line, shape_draw_type, point_color)

            flag_mode = None
            color_line_draw = None
            shape_type = None
            color_point = None

            if self.is_drawing_checkin:
                color_line_draw = (0, 255, 0)
                shape_type = "ZONE_IN"
                flag_mode = self.is_drawing_checkin
                color_point = (255, 0, 0)
            elif self.is_drawing_checkout:
                color_line_draw = (0, 0, 255)
                shape_type = "ZONE_OUT"
                flag_mode = self.is_drawing_checkout
                color_point = (255, 255, 0)
            # else:
            #     flag_mode = True
            #     color_line_draw = (255, 0, 255)
            #     shape_type = "LICENSE_PLATE"
            #     color_point = (127, 0, 255)

            handle_selection_or_draw(flag_mode, self.list_draw_shape_model, color_line_draw, shape_type, color_point)

    def handle_mouse_press(self, event, preview_rect, is_drawing, list_draw_shape_model,
                           color_line, shape_type, point_color):
        if event.button() == Qt.LeftButton and preview_rect.contains(event.position().toPoint()):
            point = (int(event.position().x()), int(event.position().y()))
            self.temp_points.append(point)
            if len(self.temp_points) == 4:
                # Call arrange_points and store the result in a variable
                arranged_points = self.arrange_points(self.temp_points)

                # Update self.points_checkin or self.points_checkout based on the drawing mode
                if is_drawing:
                    temp_shape_model = DrawShapModel(rect=arranged_points, color=color_line, shape_type=shape_type, color_point=point_color)
                    # Save the current rectangle's points to the list
                    list_draw_shape_model.append(temp_shape_model)

                    self.temp_shape_model = temp_shape_model
                # Clear the current points to start a new rectangle
                self.temp_points.clear()

    def detect_selected_edge(self, mouse_pos, model):
        for i in range(len(model.rect)):
            start_point = QPoint(*model.rect[i])
            end_point = QPoint(*model.rect[(i + 1) % len(model.rect)])
            edge_rect = QRectF(start_point, end_point).normalized().adjusted(-10, -10, 10, 10)
            if edge_rect.contains(mouse_pos):
                return i  # Return the index of the selected edge
        return None  # No edge selected

    def draw_arrows_for_rectangles(self, image, start, end, midpoint, color, model):
        self.draw_arrow(image, start, end, midpoint, color, model)

    def change_edge_color_and_draw_arrow(self, edge_index, points, model=None):
        print("HanhLT: chay vao change_edge_color_and_draw_arrow")
        # Modify the color of the selected edge
        num_points = len(points)
        if num_points >= 4:
            start_point = tuple(points[edge_index])
            end_point = tuple(points[(edge_index + 1) % num_points])

            midpoint = self.calculate_midpoint(start_point, end_point)
            self.temp_line = [start_point, end_point]
            if model is not None:
                # if model.arrow is None:
                arrow_model = ArrowModel(midpoint=midpoint, edge_index=edge_index)
                # else:
                #     arrow_model = model.arrow
                model.update_data(arrow=arrow_model, line=self.temp_line)

    def calculate_midpoint(self, start, end):
        return ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)

    def draw_arrow(self, image, start, end, midpoint, color, thickness=2, arrow_size=10, model=None):

        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        print("HanhLT: angle   ", angle)
        '''Tat ca huong ra ngoai'''
        if np.pi / 4 < angle % np.pi < 3 * np.pi / 4:
            # Vertical edge
            arrow_x = int(midpoint[0] - arrow_size * np.cos(angle - 3 * np.pi / 2))
            arrow_y = int(midpoint[1] - arrow_size * np.sin(angle - 3 * np.pi / 2))
        else:
            # Horizontal edge
            arrow_x = int(midpoint[0] - arrow_size * np.cos(angle + np.pi / 2))
            arrow_y = int(midpoint[1] - arrow_size * np.sin(angle + np.pi / 2))

        cv2.arrowedLine(image, midpoint, (arrow_x, arrow_y), color, thickness=2, tipLength=0.3)
        if model:
            model.arrow.update_data(midpoint=midpoint, arrow_x=arrow_x, arrow_y=arrow_y, color=color)

        # if np.pi / 4 < angle % np.pi < 3 * np.pi / 4:
        #     # Vertical edge
        #     arrow_x = int(midpoint[0] - arrow_size * np.cos(angle - np.pi / 2)) // huong vao trong
        #     arrow_y = int(midpoint[1] - arrow_size * np.sin(angle - np.pi / 2))
        # else:
        #     # Horizontal edge
        #     arrow_x = int(midpoint[0] - arrow_size * np.cos(angle + np.pi)) // nam ngang
        #     arrow_y = int(midpoint[1] - arrow_size * np.sin(angle + np.pi))

    def handle_selection(self, event, model):
        self.draw_shape_to_move = model
        for i, points in enumerate(model.rect):
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

                if (self.is_drawing_checkin or self.is_drawing_checkout) and self.draw_shape_to_move in self.list_draw_shape_model:
                    self.handle_point_movement(event, self.draw_shape_to_move, region_limits)

    def handle_point_movement(self, event, model, region_limits):
        if region_limits.contains(event.position().toPoint()):
            dx = int(event.position().x() - self.mouse_press_pos.x())
            dy = int(event.position().y() - self.mouse_press_pos.y())
            new_x = int(model.rect[self.selected_point_index][0] + dx)
            new_y = int(model.rect[self.selected_point_index][1] + dy)
            if region_limits.contains(QPoint(new_x, new_y)):
                model.rect[self.selected_point_index] = (new_x, new_y)
                self.mouse_press_pos = event.position()
                self.temp_rect = self.arrange_points(model.rect)

                if model.arrow is not None:
                    start_point = tuple(model.rect[model.arrow.edge_index])
                    end_point = tuple(model.rect[(model.arrow.edge_index + 1) % len(model.rect)])
                    midpoint = self.calculate_midpoint(start_point, end_point)
                    model.update_data(line=(start_point, end_point))
                    model.arrow.update_data(midpoint=midpoint)

                self.update_frame()

    def mouseReleaseEvent(self, event):
        if self.temp_rect:
            self.draw_shape_to_move.update_data(rect=self.temp_rect)
        if self.drawing_enabled:
            self.selected_point_index = None
            self.mouse_press_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = CameraApp()
    mainWin.show()
    sys.exit(app.exec())
