import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl, QObject, Signal, Slot, Property
# from PySide6.QtQml import QQmlApplicationEngine
# from PySide6.QtQuickControls2 import QQuickStyle


class SelectionManager(QObject):
    selectionChanged = Signal()

    def __init__(self):
        super().__init__()
        self.selected_cells = [[False] * 24 for _ in range(7)]  # 7 days, 24 hours
        self.is_record_mode = True  # Default to "Record Always"
        self.dragging = False  # Track if mouse is dragging
        self.drag_mode = None  # Store selection state during drag
        self._fps_value = 10
        self._quality_index = 1  # ["Low", "Medium", "High", "Best"] ~ [0, 1, 2, 3]
        self._time_archieve = 1
        self._time_unit_index = 2  # ["Minutes", "Hours", "Days"] ~ [0, 1, 2]
        self._list_quality_value = ["Lo", "Me", "Hi", "Be"]
        self._quality_text_value = self._list_quality_value[self._quality_index]

    @Slot(int, int, result=bool)
    def isSelected(self, row, col):
        """ Returns whether a specific cell is selected. """
        return self.selected_cells[row][col]

    @Slot(bool)
    def setRecordMode(self, is_record):
        """Sets the selection mode based on the chosen button."""
        self.is_record_mode = is_record

    @Slot()
    def selectAll(self):
        for row in range(7):
            for col in range(24):
                self.selected_cells[row][col] = self.is_record_mode 
        self.selectionChanged.emit()

    @Slot(int, int)
    def selectCell(self, row, col):
        """Toggles individual cell selection without affecting others."""
        self.selected_cells[row][col] = self.is_record_mode
        self.selectionChanged.emit()

    @Slot(int)
    def selectColumn(self, column_index):
        print(f"HanhLT: selectColumn  = {column_index}")
        """ Selects an entire column in grid_option (corresponding to grid_hour selection). """
        for row in range(7):
            self.selected_cells[row][column_index] = self.is_record_mode
        self.selectionChanged.emit()

    @Slot(int)
    def selectRow(self, row_index):
        """ Selects an entire row in grid_option (corresponding to grid_day selection). """
        for col in range(24):
            self.selected_cells[row_index][col] = self.is_record_mode 
        self.selectionChanged.emit()

    @Slot()
    def startDrag(self):
        """Called when the user starts dragging."""
        self.dragging = True

    @Slot()
    def endDrag(self):
        """Called when the user releases the mouse after dragging."""
        self.dragging = False
        self.selectionChanged.emit()

    @Slot(QObject, "QVariant", "QVariant")
    def selectInRange(self, grid, start, end):
        """Selects cells within the dragged area."""
        if not self.dragging:
            return
        min_x, min_y = min(start.x(), end.x()), min(start.y(), end.y())
        max_x, max_y = max(start.x(), end.x()), max(start.y(), end.y())

        children = grid.childItems()  # 🔹 Get actual cell items
        if not children:
            print("No grid children found!")
            return

        for row in range(7):
            for col in range(24):
                index = row * 24 + col
                if index >= len(children):
                    continue  # Prevent index out of range

                item = children[index]  # Get grid cell item
                item_x, item_y = item.x(), item.y()  # No need to map anymore
                item_w, item_h = item.width(), item.height()

                # Debugging: Check grid cell positions
                # print(f"HanhLT: Checking row={row}, col={col}, item_x={item_x}, item_y={item_y}, "
                #     f"min_x={min_x}, max_x={max_x}, min_y={min_y}, max_y={max_y}")

                # Selection logic: If any part of the cell is inside the selection box
                if (item_x < max_x and item_x + item_w > min_x and
                    item_y < max_y and item_y + item_h > min_y):
                    self.selected_cells[row][col] = self.is_record_mode

        self.selectionChanged.emit()

    # FPS Value
    def get_fps_value(self):
        return self._fps_value

    def set_fps_value(self, value):
        if self._fps_value != value:
            self._fps_value = value
            self.selectionChanged.emit()

    # Archive Time
    def get_time_archieve(self):
        return self._time_archieve

    def set_time_archieve(self, value):
        if self._time_archieve != value:
            self._time_archieve = value
            self.selectionChanged.emit()  # Notify QML of changes

    # Quality Index
    def get_quality_index(self):
        return self._quality_index

    def set_quality_index(self, value):
        if self._quality_index != value:
            self._quality_index = value
            self._quality_text_value = self._list_quality_value[self._quality_index]
            print(f"HanhLT: self._list_quality_value[self._quality_index] = {self._list_quality_value[self._quality_index]}")
            self.selectionChanged.emit()

    # Time Unit Index
    def get_time_unit_index(self):
        return self._time_unit_index

    def set_time_unit_index(self, value):
        if self._time_unit_index != value:
            self._time_unit_index = value
            self.selectionChanged.emit()

    def get_quality_text_value(self):
        return self._quality_text_value
    
    def set_quality_text_value(self, value):
        
        return self._quality_text_value

    fps_value = Property(int, get_fps_value, set_fps_value, notify=selectionChanged)
    time_archieve = Property(int, get_time_archieve, set_time_archieve, notify=selectionChanged)
    quality_index = Property(int, get_quality_index, set_quality_index, notify=selectionChanged)
    time_unit_index = Property(int, get_time_unit_index, set_time_unit_index, notify=selectionChanged)
    quality_text_value = Property(str, get_quality_text_value, set_quality_text_value, notify=selectionChanged)

    # Get grid value
    @Slot()
    def getSelectedTimes(self):
        selected_times = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Satureday", "Sunday"]

        for day_index in range(7):
            selected_hours = []
            for hour in range(24):
                if self.selected_cells[day_index][hour]:
                    selected_hours.append(hour)

            # Nhóm giờ liên tục lại
            if selected_hours:
                day_schedule = {}

                start = selected_hours[0]
                for i in range(1, len(selected_hours)):
                    if selected_hours[i] != selected_hours[i - 1] + 1:
                        # Khi có khoảng trống, kết thúc đoạn trước
                        end = selected_hours[i - 1] + 1
                        day_schedule[str(start)] = "start"
                        for h in range(start + 1, end):
                            day_schedule[str(h)] = "restart"
                        day_schedule[str(end)] = "stop"

                        # Bắt đầu đoạn tiếp theo
                        start = selected_hours[i]

                # Xử lý đoạn cuối cùng
                end = selected_hours[-1] + 1
                day_schedule[str(start)] = "start"
                for h in range(start + 1, end):
                    day_schedule[str(h)] = "restart"
                day_schedule[str(end)] = "stop"

                selected_times[days[day_index]] = day_schedule

        return selected_times


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.quick_widget = QQuickWidget()
        self.selection_manager = SelectionManager()

        self.quick_widget.engine().rootContext().setContextProperty("selectionManager", self.selection_manager)

        self.quick_widget.setSource(QUrl.fromLocalFile("source_qml/ScheduleUi.qml"))

        button = QPushButton("Get value")
        button.clicked.connect(self.getAllValue)

        temp_widget = QWidget()
        temp_layout = QVBoxLayout()
        temp_layout.addWidget(self.quick_widget)
        temp_layout.addWidget(button)
        temp_widget.setLayout(temp_layout)

        self.central_layout.addWidget(temp_widget)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    @Slot()
    def getAllValue(self):
        print(f"HanhLT: value fps = {self.selection_manager.fps_value}")
        print(f"HanhLT: value quality = {self.selection_manager.quality_index}")
        print(f"HanhLT: value time archieve = {self.selection_manager.time_archieve}")
        print(f"HanhLT: value time unit = {self.selection_manager.time_unit_index}")

        times = self.selection_manager.getSelectedTimes()
        print(f"HanhLT: times = { times}")


    def closeEvent(self, event):
        self.quick_widget.setSource(QUrl())  # Unload QML
        self.quick_widget.deleteLater()  # Delete widget safely
        event.accept()


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized() 
    sys.exit(app.exec())
