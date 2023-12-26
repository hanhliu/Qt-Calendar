import math

from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QDialog, QWidget, QFrame, QLineEdit, \
    QLabel, QSpinBox
from PySide6.QtCore import Qt, QSize, Signal

from src.common_controller.common_qsettings import CommonQSettings
from src.grid_custom.drawing_widget import DrawingWidget
from src.grid_custom.item_grid_model import ItemGridModel
from src.grid_custom.list_grid_custom import ListGridCustom, ItemGridCustom
from src.grid_custom.selectable_frame import SelectableFrame


class DialogTezt(QDialog):
    signal_save_trigger = Signal(object)
    def __init__(self, parent=None, list_divisions=None):
        super().__init__(parent)
        self.setModal(False)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.list_divisions = list_divisions
        self.create_title_bar()
        self.load_ui_grid_custom()
        self.load_ui_list_grid()
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

        self.body_widget = QWidget()
        self.body_widget.setObjectName("body_widget")
        self.body_layout = QVBoxLayout(self.body_widget)

        self.body_layout.addLayout(self.layout_top)
        self.body_layout.addWidget(self.widget_right_content)

        self.footer_widget = QWidget()
        self.footer_widget.setStyleSheet("background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        footer_layout = QHBoxLayout(self.footer_widget)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(120, 40)
        self.save_button.setStyleSheet(f'''QPushButton {{background-color: #B5122E; color: #FFFFFF;border-radius: 6px;margin-right: 0px;margin-left: 0px;
                margin-top: 0px;
                margin-bottom: 0px;}}
                QPushButton:hover {{background-color: #CC5051;margin-right: 0px;margin-left: 0px;
                margin-top: 0px;
                margin-bottom: 0px;}}
                QPushButton:pressed {{background-color: #CC5051;margin-right: 1px;margin-left: 1px;
                margin-top: 1px;
                margin-bottom: 1px;}}''')
        self.save_button.clicked.connect(self.on_handle_save_data)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(120, 40)
        self.cancel_button.setStyleSheet(f'''
                QPushButton {{background-color: #FFFFFF; color: #B5122E;border: 2px solid #B5122E;border-radius: 6px;margin-right: 0px;margin-left: 0px;
                margin-top: 0px;
                margin-bottom: 0px;}}
                QPushButton:hover {{background-color: #dfdfdf;margin-right: 0px;margin-left: 0px;
                margin-top: 0px;
                margin-bottom: 0px;}}
                QPushButton:pressed {{background-color: #dfdfdf;margin-right: 1px;margin-left: 1px;
                margin-top: 1px;
                margin-bottom: 1px;}}
                ''')
        self.cancel_button.clicked.connect(self.on_handle_cancel_change)
        footer_layout.addWidget(self.save_button)
        footer_layout.addWidget(self.cancel_button)

        self.layout.addWidget(self.title_bar_widget)
        self.layout.addWidget(self.body_widget)
        self.layout.addWidget(self.footer_widget)
        self.setStyleSheet("#body_widget { background-color: white; }")
        self.setLayout(self.layout)

    def create_title_bar(self):
        # layout
        self.title_bar_widget = QWidget()
        self.title_bar_widget.setObjectName("title_bar")
        # set background Style.Color.primary
        self.title_bar_widget.setStyleSheet(
            f"background-color: #B5122E; border-top-left-radius: 10px; border-top-right-radius: 10px;")

        self.title_bar_layout = QHBoxLayout()
        # event name
        self.title_name_label = QLabel(self.tr("Camera Configuration"))
        self.title_name_label.setStyleSheet(
            f"color: white; font-weight: bold")
        close_icon = QIcon("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-down.png")
        self.close_button = QPushButton(close_icon, "")
        self.close_button.setIconSize(QSize(15, 15))
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("background-color: transparent")
        self.close_button.clicked.connect(self.close)
        # add widget
        self.title_bar_layout.addWidget(self.title_name_label, 90)
        self.title_bar_layout.addWidget(self.close_button, 10)
        self.title_bar_widget.setLayout(self.title_bar_layout)

    def load_ui_list_grid(self):
        self.layout_top = QHBoxLayout()
        self.layout_top.setContentsMargins(0, 0, 0, 0)

        label_columns = QLabel("Columns: ")
        label_rows = QLabel("Rows: ")

        self.columns_spinbox = QSpinBox()
        self.columns_spinbox.setStyleSheet(
            """
            QSpinBox {
                background-color: white;
                border: 1px solid #707070;
                padding: 2px;
                min-width: 2em;
            }

            QSpinBox::up-button {
                image:url(/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-up.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }

            QSpinBox::down-button {
                image:url(/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-down.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }
            """
        )
        self.columns_spinbox.setMinimum(3)
        self.columns_spinbox.setMaximum(8)
        self.columns_spinbox.setValue(self.current_model.column)
        self.columns_spinbox.valueChanged.connect(self.handle_value_column_change)
        self.rows_spinbox = QSpinBox()
        self.rows_spinbox.setStyleSheet(
            """
            QSpinBox {
                background-color: white;
                border: 1px solid #707070;
                padding: 2px;
                min-width: 2em;
            }

            QSpinBox::up-button {
                image:url(/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-up.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }

            QSpinBox::down-button {
                image:url(/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-down.png);
                width:10px;
                height:10px;
                padding:2px 5px 0px 0px;
            }
            """
        )
        self.rows_spinbox.setMinimum(3)
        self.rows_spinbox.setMaximum(8)
        self.rows_spinbox.setValue(self.current_model.row)
        self.rows_spinbox.valueChanged.connect(self.handle_value_row_change)


        layout_columns_spinbox = QHBoxLayout()
        layout_columns_spinbox.setSpacing(4)
        layout_columns_spinbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_columns_spinbox.addWidget(label_columns)
        layout_columns_spinbox.addWidget(self.columns_spinbox)

        layout_rows_spinbox = QHBoxLayout()
        layout_rows_spinbox.setSpacing(4)
        layout_rows_spinbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_rows_spinbox.addWidget(label_rows)
        layout_rows_spinbox.addWidget(self.rows_spinbox)

        self.layout_spinbox = QHBoxLayout()
        self.layout_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_spinbox.setSpacing(40)
        self.layout_spinbox.addLayout(layout_columns_spinbox)
        self.layout_spinbox.addLayout(layout_rows_spinbox)

        self.rows, self.cols = self.rows_spinbox.value(), self.columns_spinbox.value()

        title_layouts = QLabel("Layouts:")
        layout_title = QHBoxLayout()
        layout_title.addWidget(title_layouts)
        self.layout_top.addLayout(layout_title, 20)
        self.layout_top.addLayout(self.layout_spinbox, 80)

    def load_ui_grid_custom(self):
        self.layout_right_content = QHBoxLayout()
        self.layout_right_content.setContentsMargins(0, 0, 0, 0)
        self.layout_right_content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.widget_right_content = QWidget()

        self.layout_list_grid = QVBoxLayout()
        self.layout_list_grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.list_item_grid = ListGridCustom(divisions_list=self.list_divisions)
        self.list_item_grid.signal_item_click.connect(self.connect_data_item_click)

        self.reset_button = QPushButton("Restore to Default")
        self.reset_button.setStyleSheet(f'''
                        QPushButton {{background-color: #FFFFFF; color: #B5122E;border: 2px solid #B5122E;border-radius: 6px;margin-right: 0px;margin-left: 0px;
                        margin-top: 0px;
                        margin-bottom: 0px;}}
                        QPushButton:hover {{background-color: #dfdfdf;margin-right: 0px;margin-left: 0px;
                        margin-top: 0px;
                        margin-bottom: 0px;}}
                        QPushButton:pressed {{background-color: #dfdfdf;margin-right: 1px;margin-left: 1px;
                        margin-top: 1px;
                        margin-bottom: 1px;}}
                        ''')
        self.reset_button.setFixedHeight(40)
        self.reset_button.clicked.connect(self.on_handle_reset_to_default)
        self.layout_list_grid.addWidget(self.list_item_grid)
        self.layout_list_grid.addWidget(self.reset_button)

        self.current_model = self.get_current_item_model()
        self.drawing_widget = DrawingWidget(data_model=self.current_model)
        self.drawing_widget.signal_update_data.connect(self.connect_update_data_model)

        self.layout_right_content.addLayout(self.layout_list_grid, 20)
        self.layout_right_content.addWidget(self.drawing_widget, 80)

        self.widget_right_content.setLayout(self.layout_right_content)

    def connect_data_item_click(self, data: ItemGridModel):
        '''update model ben grid o day luon'''
        print("HanhLT: data   ", data.data, "  grid_count = ", data.grid_count, "  row  ", data.row, "  col ", data.column)
        '''cần tính lại grid_count và update model ở đây, update model chưa đúng nên grid_count sẽ bị tính sai'''
        self.drawing_widget.merged_frame = data.data
        self.drawing_widget.update()

        self.columns_spinbox.setValue(data.column)
        self.rows_spinbox.setValue(data.row)

    def connect_update_data_model(self, data):
        # name: str = None
        # data: List[Set[Tuple[int, int]]] = None
        # grid_count: int = None
        # row: int = None
        # column: int = None
        # image_url: str = None
        self.new_model = ItemGridModel(data=data[0], grid_count=data[1], row=data[2], column=data[3])

        self.update_current_model(data=data[0], grid_count=data[1], new_row=data[2], new_column=data[3])

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
        for item in self.list_item_grid.divisions_list:
            print("HanhLT: item.data = ", item.data, "  item.grid_count = ",item.grid_count)
        CommonQSettings.get_instance().save_data_grid(self.list_item_grid.divisions_list)
        self.signal_save_trigger.emit(self.list_item_grid.divisions_list)
        self.close()

    def on_handle_cancel_change(self):
        self.close()

    def on_handle_reset_to_default(self):
        CommonQSettings.get_instance().clear_all()
        new_list = CommonQSettings.get_instance().get_data_grid()
        self.list_item_grid.update_grid_items(new_list)
        self.current_model = self.get_current_item_model()
        self.columns_spinbox.setValue(self.current_model.column)
        self.rows_spinbox.setValue(self.current_model.row)
        self.drawing_widget.update_data_model(self.current_model)

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

