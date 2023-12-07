import math

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QDialog, QWidget, QFrame, QLineEdit, \
    QLabel, QSpinBox
from PySide6.QtCore import Qt

from src.grid_custom.drawing_widget import DrawingWidget
from src.grid_custom.item_grid_model import ItemGridModel
from src.grid_custom.list_grid_custom import ListGridCustom, ItemGridCustom
from src.grid_custom.selectable_frame import SelectableFrame


class DialogTezt(QDialog):
    def __init__(self, parent=None, list_divisions=None):
        super().__init__(parent)
        self.list_divisions = list_divisions
        self.load_ui_list_grid()
        self.load_ui_grid_custom()
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.body_layout = QHBoxLayout()
        self.body_layout.addLayout(self.layout_list_grid)
        self.body_layout.addWidget(self.widget_right_content)
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_handle_save_data)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_handle_cancel_change)
        footer_layout.addWidget(self.save_button)
        footer_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.body_layout)
        self.layout.addLayout(footer_layout)
        self.setLayout(self.layout)

    def load_ui_list_grid(self):
        self.layout_list_grid = QVBoxLayout()
        self.list_item_grid = ListGridCustom(divisions_list=self.list_divisions)
        self.list_item_grid.signal_item_click.connect(self.connect_data_item_click)

        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.on_handle_reset_to_default)

        self.layout_list_grid.addWidget(self.list_item_grid)
        self.layout_list_grid.addWidget(self.reset_button)

    def connect_data_item_click(self, data: ItemGridModel):
        '''update model ben grid o day luon'''
        print("HanhLT: data   ", data.data, "  grid_count = ", data.grid_count, "  row  ", data.row, "  col ", data.column)
        '''cần tính lại grid_count và update model ở đây, update model chưa đúng nên grid_count sẽ bị tính sai'''
        self.drawing_widget.merged_frame = data.data
        self.drawing_widget.update()

        self.columns_spinbox.setValue(data.column)
        self.rows_spinbox.setValue(data.row)

    def load_ui_grid_custom(self):
        self.layout_right_content = QVBoxLayout()
        self.widget_right_content = QWidget()
        label_columns = QLabel("Columns: ")
        label_rows = QLabel("Rows: ")

        current_model = self.get_current_item_model()

        self.columns_spinbox = QSpinBox()
        self.columns_spinbox.setMinimum(3)
        self.columns_spinbox.setMaximum(8)
        self.columns_spinbox.setValue(current_model.column)
        self.columns_spinbox.valueChanged.connect(self.handle_value_column_change)
        self.rows_spinbox = QSpinBox()
        self.rows_spinbox.setMinimum(3)
        self.rows_spinbox.setMaximum(8)
        self.rows_spinbox.setValue(current_model.row)
        self.rows_spinbox.valueChanged.connect(self.handle_value_row_change)

        layout_columns_spinbox = QHBoxLayout()
        layout_columns_spinbox.addWidget(label_columns)
        layout_columns_spinbox.addWidget(self.columns_spinbox)

        layout_rows_spinbox = QHBoxLayout()
        layout_rows_spinbox.addWidget(label_rows)
        layout_rows_spinbox.addWidget(self.rows_spinbox)

        self.rows, self.cols = self.rows_spinbox.value(), self.columns_spinbox.value()
        self.drawing_widget = DrawingWidget(data_model=current_model)
        self.drawing_widget.signal_update_data.connect(self.connect_update_data_model)

        self.layout_top = QHBoxLayout()
        self.layout_top.addLayout(layout_columns_spinbox)
        self.layout_top.addLayout(layout_rows_spinbox)

        self.layout_right_content.addLayout(self.layout_top)
        self.layout_right_content.addWidget(self.drawing_widget)

        self.widget_right_content.setLayout(self.layout_right_content)

    def connect_update_data_model(self, data):
        # name: str = None
        # data: List[Set[Tuple[int, int]]] = None
        # grid_count: int = None
        # row: int = None
        # column: int = None
        # image_url: str = None
        self.new_model = ItemGridModel(data=data[0], grid_count=data[1], row=data[2], column=data[3])

        self.update_current_model(data=data[0], grid_count=data[1], new_row=data[2], new_column=data[3])
        for idx, i in enumerate(self.list_item_grid.divisions_list):
            print("HanhLT: data init ",idx, "   ", i.data)

        for idxx, j in enumerate(self.list_item_grid.list_grid_custom):
            print("HanhLT: data edit  ", idxx, "   ", j.data)

    def handle_value_row_change(self, new_value):
        self.rows = new_value
        self.drawing_widget.set_row_count(new_value)
        remain_item = self.drawing_widget.calculate_remaining_items()
        self.update_current_model(new_row=new_value, grid_count=remain_item)
        self.drawing_widget.update()

    def handle_value_column_change(self, new_value):
        self.cols = new_value
        self.drawing_widget.set_column_count(new_value)
        remain_item = self.drawing_widget.calculate_remaining_items()
        self.update_current_model(new_column=new_value, grid_count=remain_item)
        self.drawing_widget.update()

    def update_current_model(self, new_row=None, new_column=None, data=None, grid_count=None):
        current_model = self.get_current_item_model()
        if current_model:
            current_model.update_data(row=new_row, column=new_column, data=data, grid_count=grid_count)
            if grid_count is not None:
                self.update_name_grid(f"{current_model.grid_count} Divisions")

    def update_name_grid(self, name):
        # Get the current selected index
        current_item_list_idx = self.list_item_grid.currentIndex()
        # Get the item from the model at the selected index
        item: ItemGridCustom = self.list_item_grid.list_view_model.itemFromIndex(current_item_list_idx)
        item.label_name_grid.setText(name)

    def on_handle_save_data(self):

        self.close()
        model_current_item: ItemGridModel = self.get_current_item_model()

    def on_handle_cancel_change(self):
        self.close()

    def on_handle_reset_to_default(self):
        pass

    def get_current_item_model(self):
        # Get the current selected index
        current_item_list_idx = self.list_item_grid.currentIndex()
        # Check if there is a selected index
        if current_item_list_idx.isValid():
            # Get the item from the model at the selected index
            item = self.list_item_grid.list_view_model.itemFromIndex(current_item_list_idx)
            # Assuming ItemGridModel is the type of model used in your code
            model_current_item: ItemGridModel = item.model
            return model_current_item
        else:
            return None  # Return None if there is no selected item

