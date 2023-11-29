
from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QDialog
from PySide6.QtCore import Qt

from src.grid_custom.drawing_widget import DrawingWidget
from src.grid_custom.selectable_frame import SelectableFrame


class DialogTezt(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.combo_box = QComboBox()
        self.combo_box.addItems(["2x2", "3x3", "4x4", "6x6"])
        default_index = self.combo_box.findText("3x3")
        self.combo_box.setCurrentIndex(default_index)
        self.combo_box.currentIndexChanged.connect(self.onComboIndexChanged)

        self.merge_button = QPushButton("Merge")
        self.merge_button.clicked.connect(self.mergeSelected)
        self.reset_button = QPushButton("Save")
        self.reset_button.clicked.connect(self.save_click)
        # Set up a new layout with the selected size
        self.rows, self.cols = map(int, self.combo_box.currentText().split('x'))
        self.drawing_widget = DrawingWidget(size_grid=self.rows)

        self.layout_top = QHBoxLayout()
        self.layout_top.addWidget(self.combo_box)
        self.layout_top.addWidget(self.merge_button)
        self.layout_top.addWidget(self.reset_button)
        self.layout.addLayout(self.layout_top)
        self.layout.addWidget(self.drawing_widget)

        self.setLayout(self.layout)

    def save_click(self):
        self.close()

    def mergeSelected(self):
        if len(self.drawing_widget.selected_frames) >= 2:
            self.drawing_widget.paint_borders = True
            new_merged_frame = [s for i, s in enumerate(self.drawing_widget.merged_frame) if
                                not any(e in self.drawing_widget.selected_frames for e in s)]

            # Append the new set
            new_merged_frame.append(self.drawing_widget.selected_frames)

            # Update the merged_frame attribute
            self.drawing_widget.merged_frame = new_merged_frame

            print("HanhLT: self.drawing_widget.merged_frame   ", self.drawing_widget.merged_frame)

            self.drawing_widget.testFlag = True
            # Clear the drawn rectangle
            self.drawing_widget.selection_start = None
            self.drawing_widget.selection_end = None
            # self.drawing_widget.selected_frames.clear()
            self.drawing_widget.update()

    def get_selected_positions(self):
        return [(i, j) for frame in self.drawing_widget.selected_frames for i in range(self.rows) for j in range(self.cols) if self.frames[i][j] is frame]

    def onComboIndexChanged(self, index):
        self.drawing_widget.merged_frame.clear()
        selected_item = self.combo_box.currentText()

        # Clear the drawn rectangle
        self.drawing_widget.selection_start = None
        self.drawing_widget.selection_end = None
        self.drawing_widget.selected_frames.clear()
        self.drawing_widget.update()

        # Clear the red borders on selected frames
        for i in range(self.drawing_widget.grid_layout.count()):
            frame = self.drawing_widget.grid_layout.itemAt(i).widget()
            frame.is_selected = False
            frame.update()

        # Clear the existing layout
        for i in reversed(range(self.drawing_widget.grid_layout.count())):
            widgetToRemove = self.drawing_widget.grid_layout.itemAt(i).widget()
            widgetToRemove.setParent(None)

        # Set up a new layout with the selected size
        self.rows, self.cols = map(int, selected_item.split('x'))
        for i in range(self.rows):
            for j in range(self.cols):
                frame = SelectableFrame(self.drawing_widget)
                self.drawing_widget.grid_layout.addWidget(frame, i, j)

        # Update the size of the drawing widget based on the new grid size
        self.drawing_widget.setFixedSize(800, 600)