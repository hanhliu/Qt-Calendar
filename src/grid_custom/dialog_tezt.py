import math

from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QDialog, QWidget, QFrame, QLineEdit, \
    QLabel
from PySide6.QtCore import Qt

from src.grid_custom.drawing_widget import DrawingWidget
from src.grid_custom.item_grid_model import ItemGridModel
from src.grid_custom.list_grid_custom import ListGridCustom
from src.grid_custom.selectable_frame import SelectableFrame


class DialogTezt(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.load_ui_button()
        self.load_ui_list_grid()
        self.load_ui_grid_custom()
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.layout_button)

        self.body_layout = QHBoxLayout()
        self.body_layout.addLayout(self.layout_list_grid)
        self.body_layout.addWidget(self.widget_right_content)
        self.layout.addLayout(self.body_layout)
        self.check_enable_ui()
        self.setLayout(self.layout)

    def load_ui_button(self):
        self.layout_button = QHBoxLayout()
        self.layout_button.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.show_create_dialog)
        self.button_add.setFixedWidth(100)
        self.button_delete = QPushButton("Delete")
        self.button_delete.setFixedWidth(100)
        self.layout_button.addWidget(self.button_add)
        self.layout_button.addWidget(self.button_delete)

    def show_create_dialog(self):
        self.dialog_create = QDialog(self)
        self.dialog_create.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.dialog_create.setFixedSize(280, 120)
        self.dialog_create.setWindowTitle('Add Custom Window Division')

        dialog_layout = QVBoxLayout()

        label_title = QLabel("Add Custom Window Division")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dialog_layout.addWidget(label_title)

        layout_content = QHBoxLayout()
        self.label_name = QLabel("Name: ")
        self.line_edit = QLineEdit()
        layout_content.addWidget(self.label_name)
        layout_content.addWidget(self.line_edit)

        layout_footer = QHBoxLayout()
        layout_footer.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.save_create = QPushButton("Create")
        self.save_create.clicked.connect(self.on_create_custom_grid_click)
        self.save_create.setFixedSize(60, 40)
        self.cancel_create = QPushButton("Cancel")
        self.cancel_create.clicked.connect(self.on_cancel_create_click)
        self.cancel_create.setFixedSize(60, 40)
        layout_footer.addWidget(self.save_create)
        layout_footer.addWidget(self.cancel_create)

        dialog_layout.addLayout(layout_content)
        dialog_layout.addLayout(layout_footer)
        self.dialog_create.setLayout(dialog_layout)

        self.dialog_create.exec_()

    def on_cancel_create_click(self):
        self.check_enable_ui()
        self.dialog_create.close()

    def on_create_custom_grid_click(self):
        new_item = ItemGridModel(name=self.line_edit.text(), data=[], grid_size=9)
        self.list_item_grid.add_newest_item_grid(new_item)
        '''Chưa biết là lưu local hay lưu global nên note lại để nhớ cần phải 
        add vào list_grid_custom để sau khi mở lại app sẽ có các list đã tạo'''
        self.list_item_grid.list_grid_custom.append(new_item)
        self.check_enable_ui()
        '''change combobox here, viet 1 ham change'''
        self.dialog_create.close()

        current_item_list_idx = self.list_item_grid.currentIndex()  # Assuming currentItem() returns the selected item
        item = self.list_item_grid.list_view_model.itemFromIndex(current_item_list_idx)
        model_current_item: ItemGridModel = item.model
        self.setComboIndexByGridSize(model_current_item.grid_size)
        self.name_input_view_only.setText(model_current_item.name)

    def load_ui_list_grid(self):
        self.layout_list_grid = QVBoxLayout()
        self.list_item_grid = ListGridCustom()
        self.list_item_grid.signal_item_click.connect(self.connect_data_item_click)
        self.layout_list_grid.addWidget(self.list_item_grid)

    def connect_data_item_click(self, data: ItemGridModel):
        '''update model ben grid o day luon'''
        print("HanhLT: data   ", data.grid_size)
        self.drawing_widget.set_grid_size(data.grid_size)
        self.drawing_widget.update()
        self.setComboIndexByGridSize(data.grid_size)
        self.name_input_view_only.setText(data.name)

    def onNameInputTextChanged(self, new_text):
        current_item_list_idx = self.list_item_grid.currentIndex()  # Assuming currentItem() returns the selected item
        item = self.list_item_grid.list_view_model.itemFromIndex(current_item_list_idx)
        model_current_item: ItemGridModel = item.model
    def setComboIndexByGridSize(self, grid_size):
        sqrt_size = int(math.sqrt(grid_size))
        # Find the index in the combo box based on the grid size
        index = self.combo_box.findText(f"{sqrt_size}x{sqrt_size}")
        if index != -1:
            # Set the combo box index to the found index
            self.combo_box.setCurrentIndex(index)

    def load_ui_grid_custom(self):
        self.layout_right_content = QVBoxLayout()
        self.widget_right_content = QWidget()
        label_name = QLabel("Name: ")
        self.name_input_view_only = QLineEdit()
        self.name_input_view_only.textChanged.connect(self.onNameInputTextChanged)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["2x2", "3x3", "4x4", "6x6"])
        default_index = self.combo_box.findText("3x3")
        self.combo_box.setCurrentIndex(default_index)
        self.combo_box.currentIndexChanged.connect(self.onComboIndexChanged)

        self.merge_button = QPushButton("Merge")
        self.merge_button.clicked.connect(self.mergeSelected)
        self.reset_button = QPushButton("Save")
        self.reset_button.clicked.connect(self.save_data)
        # Set up a new layout with the selected size
        self.rows, self.cols = map(int, self.combo_box.currentText().split('x'))
        self.drawing_widget = DrawingWidget(size_grid=self.rows*self.rows)

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.HLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)

        self.layout_top = QHBoxLayout()
        self.layout_top.addWidget(label_name)
        self.layout_top.addWidget(self.name_input_view_only)
        self.layout_top.addWidget(self.combo_box)
        self.layout_top.addWidget(self.merge_button)
        self.layout_top.addWidget(self.reset_button)

        self.layout_right_content.addWidget(self.divider)
        self.layout_right_content.addLayout(self.layout_top)
        self.layout_right_content.addWidget(self.drawing_widget)

        self.widget_right_content.setLayout(self.layout_right_content)

    def check_enable_ui(self):
        if not self.list_item_grid.list_grid_custom:
            self.widget_right_content.setDisabled(True)
        else:
            self.widget_right_content.setDisabled(False)

    def save_data(self):
        # self.close()
        current_item_list_idx = self.list_item_grid.currentIndex()  # Assuming currentItem() returns the selected item
        item = self.list_item_grid.list_view_model.itemFromIndex(current_item_list_idx)
        model_current_item: ItemGridModel = item.model

        selected_item = self.combo_box.currentText()
        row, col = map(int, selected_item.split('x'))
        model_current_item.update_data(grid_size=row * row, name=self.name_input_view_only.text(), data=self.data)

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
            self.drawing_widget.update()

    def onComboIndexChanged(self, index):
        print("HanhLT: chay vao day ")
        self.drawing_widget.merged_frame.clear()
        selected_item = self.combo_box.currentText()

        current_item_list_idx = self.list_item_grid.currentIndex()
        item = self.list_item_grid.list_view_model.itemFromIndex(current_item_list_idx)
        model_current_item: ItemGridModel = item.model
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

        model_current_item.update_data(grid_size=self.rows*self.rows)

        # Update the size of the drawing widget based on the new grid size
        self.drawing_widget.setFixedSize(800, 600)
