import math
import sys
from typing import Any
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBox,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
    QGraphicsTextItem,
    QGraphicsItem,
    QGraphicsPolygonItem,
    QGraphicsEllipseItem,
    QGraphicsPathItem,
    QWidget,
)
from PySide6.QtGui import QPixmap, QPolygonF, QColor, QPainterPath, QPen, QPainter
from PySide6.QtCore import Qt, QPointF, QEvent, QPoint, QRectF


class HandleItem(QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setBrush(QColor(255, 255, 255, 150))  # Semi-transparent white
        self.polygon_item: CustomPolygonItem = None  # To keep track of the polygon item associated with this handle
        self.angle_item: CustomEllipseItem = None  # To keep track of the arc item associated with this handle

    def set_polygon_item(self, polygon_item):
        self.polygon_item = polygon_item

    def set_arc_item(self, angle_item):
        self.angle_item = angle_item

    def sceneEventFilter(self, watched: QGraphicsItem, event: QEvent) -> bool:
        # <PySide6.QtWidgets.QGraphicsSceneMouseEvent(GraphicsSceneMouseMove, buttons=LeftButton, pos=1,3, scenePos=-146,11, screenPos=674,512) at 0x106361fc0>
        # need update update_polygon_shape
        if event.type() == QEvent.GraphicsSceneMouseMove:
            print(f"watched: {watched}")
            if (
                watched in self.scene().items()
                and hasattr(watched, "corner_point")
                and watched.corner_point is not None
            ):
                print(f"corner_point - watched: x {watched.pos().x()} - y {watched.pos().y()}")
                # Update the associated corner point of the polygon
                watched.corner_point.setX(watched.pos().x())
                watched.corner_point.setY(watched.pos().y())

                if self.polygon_item:
                    # Update the shape of the polygon
                    self.polygon_item.update_polygon_shape(watched, event)
                
            if (
                watched in self.scene().items()
                and (hasattr(watched, "start_point_arc"))
                and (watched.start_point_arc is not None)
            ):
                if watched.start_point_arc:
                    # Update the associated corner point of the polygon
                    watched.start_point_arc.setX(watched.pos().x())
                    watched.start_point_arc.setY(watched.pos().y())
                if self.angle_item:
                    # Update the shape of the angle
                    self.angle_item.update_arc_shape(watched, event)
            
            if (
                watched in self.scene().items()
                and (hasattr(watched, "end_point_arc"))
                and (watched.end_point_arc is not None)
            ):
                if watched.end_point_arc:
                    # Update the associated corner point of the polygon
                    watched.end_point_arc.setX(watched.pos().x())
                    watched.end_point_arc.setY(watched.pos().y())
                if self.angle_item:
                    # Update the shape of the angle
                    self.angle_item.update_arc_shape(watched, event)

                
        return super().sceneEventFilter(watched, event)

class CustomView(QGraphicsView):
    def __init__(self, scene):
        super(CustomView, self).__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)

class CustomScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

class CustomPolygonItem(QGraphicsPolygonItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red

    def update_polygon_shape(self, moved_handle = None, event = None):
        # Get the list of corner points of the polygon
        corner_points = self.polygon().toPolygon().toList()
        if moved_handle and event:
            # Convert to list of QPoint
            corner_points_qpoint = [QPoint(p.x(), p.y()) for p in corner_points]

            # Find the index of the nearest corner point
            index = self.find_nearest_corner_index(moved_handle.corner_point, corner_points_qpoint)

            # Update the corresponding corner point in the polygon
            corner_points[index] = moved_handle.corner_point

        # Update the polygon shape
        new_polygon = QPolygonF(corner_points)
        self.setPolygon(new_polygon)

    def find_nearest_corner_index(self, point, corner_points):
        # Find the index of the nearest corner point
        distances = [self.point_manhattan_distance(point, corner) for corner in corner_points]
        return distances.index(min(distances))

    def point_manhattan_distance(self, point1, point2):
        return abs(point1.x() - point2.x()) + abs(point1.y() - point2.y())


class CustomEllipseItem(QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setPen(QPen(Qt.blue))  # Set the pen color for the arc
        self.start_handle: HandleItem = None
        self.end_handle: HandleItem = None
    
    def update_handle(self, start, end):
        self.start_handle = start
        self.end_handle = end

    def update_arc_shape(self, moved_handle, event, max_rotation=180):
        current_start_angle = self.startAngle()
        current_span_angle = self.spanAngle()
        start_angle_rad = math.radians(current_start_angle / 16.0)
        end_angle_rad = math.radians((current_start_angle + current_span_angle) / 16.0)

        point_center_of_circle = self.rect().center()

        new_start_angle = None
        new_span_angle = None

        new_end_point = None

        if hasattr(moved_handle, "start_point_arc") and moved_handle.start_point_arc:
            print('MOVE START HANDLE')
            # Calculate new start and end angles based on the movement of the handle
            new_start_point = moved_handle.start_point_arc

            angle_rad = math.atan2(new_start_point.y() - point_center_of_circle.y(),
                                new_start_point.x() - point_center_of_circle.x())

            new_start_angle = (0 - math.degrees(angle_rad)) * 16.0

            # Update the arc shape
            new_span_angle = current_span_angle  # You need to calculate this based on your logic

            # calculate arc size
            size_arc = math.sqrt((new_start_point.x() - point_center_of_circle.x())**2 + (new_start_point.y() - point_center_of_circle.y())**2)

            self.setRect(QRectF(point_center_of_circle.x() - size_arc, point_center_of_circle.y() - size_arc, size_arc * 2, size_arc * 2))

            # from new_start_angle and new_span_angle calculate new end point
            end_angle_rad = math.radians((0 - (new_start_angle + new_span_angle)) / 16.0)
            
            # calculate new end point
            new_end_point = point_center_of_circle + QPointF(self.rect().width() / 2 * math.cos(end_angle_rad),
                                                                            self.rect().height() / 2 * math.sin(end_angle_rad)) 
            # update self.end_handle 
            self.end_handle.setPos(new_end_point)

        elif hasattr(moved_handle, "end_point_arc") and moved_handle.end_point_arc:
            print('MOVE END HANDLE')
            # Calculate new start and end angles based on the movement of the handle
            new_end_point = moved_handle.end_point_arc
            point_center_of_circle = self.rect().center()

            angle_rad = math.atan2(new_end_point.y() - point_center_of_circle.y(),
                                new_end_point.x() - point_center_of_circle.x())

            new_end_angle = (0 - math.degrees(angle_rad)) * 16.0

            # calculate new span angle based on new start angle 
            new_span_angle = new_end_angle - current_start_angle

            # calculate arc size
            size_arc = math.sqrt((new_end_point.x() - point_center_of_circle.x())**2 + (new_end_point.y() - point_center_of_circle.y())**2)

            self.setRect(QRectF(point_center_of_circle.x() - size_arc, point_center_of_circle.y() - size_arc, size_arc * 2, size_arc * 2))

            # calculate new start start angle
            new_start_angle = new_end_angle - new_span_angle

            # calculate new start point
            start_angle_rad = math.radians((0 - new_start_angle) / 16.0)
            new_start_point = point_center_of_circle + QPointF(self.rect().width() / 2 * math.cos(start_angle_rad),
                                                                            self.rect().height() / 2 * math.sin(start_angle_rad))
            
            self.start_handle.setPos(new_start_point)

        if new_start_angle and new_span_angle:
            # Calculate the difference between the new start and end angles
            angle_difference = (new_start_angle + new_span_angle) - new_start_angle

            # Check if the angle difference exceeds the maximum allowed rotation
            if abs(angle_difference) > max_rotation * 16:
                # Limit the rotation to the maximum allowed
                if angle_difference > 0:
                    new_span_angle = max_rotation * 16
                else:
                    new_span_angle = -max_rotation * 16        

        # calculate new span angle
        if new_start_angle:
            self.setStartAngle(new_start_angle)
        if new_span_angle:
            self.setSpanAngle(new_span_angle)

        
class ImageToolboxApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Toolbox")
        self.setGeometry(100, 100, 800, 600)

        # Create a toolbox
        self.toolbox = QToolBox()
        self.setCentralWidget(self.toolbox)

        # Create an initial label in the toolbox
        self.default_label = QLabel("No Image")
        self.toolbox.addItem(self.default_label, "Default Image")

        # Create a layout for the central widget
        layout = QVBoxLayout()

        # Create buttons to add different items to the toolbox
        import_button = QPushButton("Import Image")
        import_button.clicked.connect(self.import_image)

        add_camera_button = QPushButton("Add Camera")
        add_camera_button.clicked.connect(lambda: self.add_item("Camera"))

        add_area_button = QPushButton("Add Area")
        add_area_button.clicked.connect(lambda: self.add_item("Area"))

        add_angle_button = QPushButton("Add Angle")
        add_angle_button.clicked.connect(lambda: self.add_item("Angle"))

        add_state_button = QPushButton("Add State")
        add_state_button.clicked.connect(lambda: self.add_item("State"))

        
        # Add the buttons to the layout
        layout.addWidget(import_button)
        layout.addWidget(add_camera_button)
        layout.addWidget(add_area_button)
        layout.addWidget(add_angle_button)
        layout.addWidget(add_state_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)

        # Create a QGraphicsScene and QGraphicsView
        self.scene = CustomScene()
        self.view = CustomView(self.scene)
        main_layout.addWidget(self.view)

        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create a QWidget to hold the zoom button
        zoom_button_widget = QWidget(self.view)
        
        zoom_button_layout = QVBoxLayout(zoom_button_widget)

        # Add Zoom In and Zoom Out buttons
        zoom_in_button = QPushButton("+")
        zoom_in_button.clicked.connect(self.zoom_in)

        zoom_out_button = QPushButton("-")
        zoom_out_button.clicked.connect(self.zoom_out)

        # Add the buttons to the layout
        zoom_button_layout.addWidget(zoom_in_button)
        zoom_button_layout.addWidget(zoom_out_button)

        # Set the layout for the zoom button widget
        zoom_button_widget.setLayout(zoom_button_layout)

        print(f'zoom_button_widget: {zoom_button_widget.width()} - {zoom_button_widget.height()}')

        # set the position of the zoom button widget in the top-right corner
        zoom_button_widget.setGeometry(
            self.view.width() - zoom_button_widget.width()/2,
            0,
            zoom_button_widget.width()/2,
            zoom_button_widget.height() * 3,
        )

        # Make the zoom button widget translucent
        zoom_button_widget.setWindowOpacity(0.8)

        # Show the zoom button widget
        zoom_button_widget.show()

    def zoom_in(self):
        factor = 1.2
        self.view.scale(factor, factor)

    def zoom_out(self):
        factor = 1.2
        self.view.scale(1.0 / factor, 1.0 / factor)

    def import_image(self):
        # Open a file dialog to choose an image file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.jpg *.bmp)"
        )

        # If a file is selected, update the label in the toolbox and display the image in the QGraphicsView
        if file_path:
            print(f"file_path: {file_path}")
            pixmap = QPixmap(file_path)
            self.scene.clear()

            # Add the image to the scene
            item = QGraphicsPixmapItem(pixmap)
            item.setFlag(QGraphicsItem.ItemIsMovable)
            self.scene.addItem(item)

            # Set the scene to the view
            self.view.setScene(self.scene)

    def add_item(self, item_type):
        if item_type == "Camera":
            # Create a draggable quadrilateral for the camera angle
            points = [QPointF(0, 0), QPointF(50, 0), QPointF(50, 50), QPointF(0, 50)]
            polygon_item = CustomPolygonItem(QPolygonF(points))
            polygon_item.setFlag(QGraphicsItem.ItemIsMovable)
            polygon_item.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red
            # Install the event filter on the polygon item
            self.scene.addItem(polygon_item)

            # Create handles for each corner point
            handles = []
            for point in points:
                handle = HandleItem(-5, -5, 10, 10)  # Handle size
                handle.set_polygon_item(polygon_item)
                handle.setPos(point)
                handle.setParentItem(polygon_item)
                handle.installSceneEventFilter(handle)
                handles.append(handle)

            # Connect handle movements to update the polygon shape
            for handle, corner_point in zip(handles, points):
                handle.corner_point = corner_point

        elif item_type == "Area":
            # Create a QGraphicsTextItem with the item type text and add it to the scene
            text_item = QGraphicsTextItem(f"{item_type} Item")
            text_item.setDefaultTextColor(Qt.red)
            text_item.setFlag(QGraphicsItem.ItemIsMovable)
            text_item.setPos(50, 50)  # Adjust the position as needed
            self.scene.addItem(text_item)
        elif item_type == "Angle":
            # Create a circular arc representing a 2-hour interval (from 2 o'clock to 4 o'clock)
            arc_item = CustomEllipseItem(0, 0, 300, 300)  # Adjust parameters as needed
            arc_item.setStartAngle(0)
            arc_item.setSpanAngle(1440)
            arc_item.setFlag(QGraphicsItem.ItemIsMovable)
            arc_item.setPen(QPen(Qt.blue))  # Set the pen color for the arc
            self.scene.addItem(arc_item)

            # get pos of start arc arc_item
            start_angle_rad = math.radians(arc_item.startAngle() / 16.0)
            end_angle_rad = math.radians((arc_item.startAngle() - arc_item.spanAngle()) / 16.0)

            start_point = arc_item.mapToScene(arc_item.rect().center()) + QPointF(arc_item.rect().width() / 2 * math.cos(start_angle_rad),
                                                                                arc_item.rect().height() / 2 * math.sin(start_angle_rad))
            end_point = arc_item.mapToScene(arc_item.rect().center()) + QPointF(arc_item.rect().width() / 2 * math.cos(end_angle_rad),
                                                                                arc_item.rect().height() / 2 * math.sin(end_angle_rad))
            
            # Calculate the midpoint on the arc
            # angle_midpoint_rad = (start_angle_rad + end_angle_rad) / 2

            # center_point = arc_item.mapToScene(arc_item.rect().center()) + QPointF(arc_item.rect().width() / 2 * math.cos(angle_midpoint_rad),
            #                                                                         arc_item.rect().height() / 2 * math.sin(angle_midpoint_rad))

            start_handle = HandleItem(-10, -10, 20, 20)  # Handle size
            start_handle.set_arc_item(arc_item)
            start_handle.setPos(start_point)
            start_handle.setParentItem(arc_item)
            start_handle.installSceneEventFilter(start_handle)
            # set color red
            start_handle.setBrush(QColor(255, 255, 140, 50))
            start_handle.start_point_arc = start_point

            end_handle = HandleItem(-10, -10, 20, 20)  # Handle size
            end_handle.set_arc_item(arc_item)
            end_handle.setPos(end_point)
            end_handle.setParentItem(arc_item)
            end_handle.installSceneEventFilter(end_handle)
            # set color green
            end_handle.setBrush(QColor(255, 140, 255, 50))
            end_handle.end_point_arc = end_point

            arc_item.update_handle(start_handle, end_handle)

            

        elif item_type == "State":
            # Create a QGraphicsTextItem with the item type text and add it to the scene
            text_item = QGraphicsTextItem(f"{item_type} Item")
            text_item.setDefaultTextColor(Qt.red)
            text_item.setFlag(QGraphicsItem.ItemIsMovable)
            text_item.setPos(50, 50)  # Adjust the position as needed
            self.scene.addItem(text_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageToolboxApp()
    window.show()
    sys.exit(app.exec())
