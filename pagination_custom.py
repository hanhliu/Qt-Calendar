from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication, QTableView,
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QWidgetAction,
    QStackedWidget, QStackedLayout
)
from PySide6.QtCore import Qt, Signal
import sys

class CustomPagination(QWidget):
    signal_update_table = Signal(tuple)

    def __init__(self, total_rows=None, rows_per_page=10):
        super().__init__()
        self.total_rows = total_rows
        self.rows_per_page = rows_per_page
        self.current_page = 1
        self.total_pages = (self.total_rows + self.rows_per_page - 1) // self.rows_per_page

        # Layouts
        self.main_layout = QVBoxLayout(self)
        self.pagination_layout = QHBoxLayout()
        self.pagination_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.pagination_layout.setSpacing(2)
        self.widget_indicator_numer = QWidget()
        self.widget_indicator_numer.setStyleSheet('background-color: lightblue')
        self.widget_indicator_numer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.layout_indicator_numer = QHBoxLayout()
        self.layout_indicator_numer.setSpacing(2)
        self.layout_indicator_numer.setContentsMargins(0, 0, 0, 0)
        self.layout_indicator_numer.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Style sheet
        self.btn_active = f'''
                            QPushButton{{
                                background-color: #B5122E;
                                color: white;
                                border-radius: 4px;
                            }}
                        '''
        self.btn_deactive = f'''
                                QPushButton{{
                                    background-color: #262626;
                                    color: #979797;
                                    border-radius: 4px;
                                }}
                            '''

        # Pagination Controls
        self.first_page_button = QPushButton("<<")
        self.first_page_button.setFixedSize(24, 24)
        self.last_page_button = QPushButton(">>")
        self.last_page_button.setFixedSize(24, 24)
        self.prev_button = QPushButton("<")
        self.prev_button.setFixedSize(24, 24)
        self.next_button = QPushButton(">")
        self.next_button.setFixedSize(24, 24)
        self.page_input = QLineEdit()
        self.page_input.setFixedWidth(30)
        self.page_input.setText(str(self.current_page))

        # Page number buttons
        self.page_buttons = []

        # Setup Stylesheet
        self.first_page_button.setStyleSheet(self.btn_deactive)
        self.last_page_button.setStyleSheet(self.btn_deactive)
        self.prev_button.setStyleSheet(self.btn_deactive)
        self.next_button.setStyleSheet(self.btn_deactive)

        # Setup UI
        self.setup_pagination()
        self.main_layout.addLayout(self.pagination_layout)

        # Connect events
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.first_page_button.clicked.connect(self.go_to_first_page)
        self.last_page_button.clicked.connect(self.go_to_last_page)
        self.page_input.returnPressed.connect(self.jump_to_page)

        # Show the first page
        self.update_table()

    def setup_pagination(self):
        """Setup pagination layout."""
        self.pagination_layout.addWidget(self.first_page_button)
        self.pagination_layout.addWidget(self.prev_button)

        # Page buttons dynamically
        self.generate_page_buttons()
        self.widget_indicator_numer.setLayout(self.layout_indicator_numer)
        self.pagination_layout.addWidget(self.widget_indicator_numer)

        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addWidget(self.last_page_button)
        self.pagination_layout.addWidget(self.page_input)

    def generate_page_buttons(self):
        """Dynamically create page number buttons for large datasets."""
        for btn_indicator in self.page_buttons:
            btn_indicator.deleteLater()

        self.page_buttons.clear()

        # Always show 7 items: "< 1 ... 5 6 7 ... 20 >"
        max_visible_pages = 7

        if self.total_pages <= max_visible_pages:
            # Show all pages if there are less than or equal to 7 pages
            pages = range(1, self.total_pages + 1)
        else:
            # Ensure 7 items always shown
            if self.current_page <= 4:
                # Near the beginning, show first 5 pages, then "..." and last page
                pages = list(range(1, 6)) + ["..."] + [self.total_pages]
            elif self.current_page >= self.total_pages - 3:
                # Near the end, show first page, then "...", then last 5 pages
                pages = [1, "..."] + list(range(self.total_pages - 4, self.total_pages + 1))
            else:
                # In the middle, show first page, "...", current page and neighbors, "...", and last page
                pages = [1, "..."] + list(range(self.current_page - 1, self.current_page + 2)) + ["..."] + [
                    self.total_pages]

        print(f"HanhLT: pages = {pages}")
        for page in pages:
            if page == "...":
                print(f"HanhLT: chay vao day may lan???")
                btn_undefined = QPushButton("...")
                btn_undefined.setFixedSize(24, 24)
                btn_undefined.setStyleSheet(self.btn_deactive)
                self.page_buttons.append(btn_undefined)
                self.layout_indicator_numer.addWidget(btn_undefined)
            else:
                btn_indicator = QPushButton(str(page))
                btn_indicator.setFixedSize(24, 24)
                btn_indicator.clicked.connect(self.page_button_clicked)
                if btn_indicator.text() == str(self.current_page):
                    btn_indicator.setStyleSheet(self.btn_active)
                else:
                    btn_indicator.setStyleSheet(self.btn_deactive)
                self.page_buttons.append(btn_indicator)
                self.layout_indicator_numer.addWidget(btn_indicator)

    def page_button_clicked(self):
        """Handle page button clicks."""
        page = int(self.sender().text())
        self.current_page = page
        self.update_table()

    def jump_to_page(self):
        """Jump to the page entered by the user."""
        page = int(self.page_input.text())
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.update_table()

    def prev_page(self):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()

    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_table()

    def go_to_first_page(self):
        """Go to the first page."""
        self.current_page = 1
        self.update_table()

    def go_to_last_page(self):
        """Go to the last page."""
        self.current_page = self.total_pages
        self.update_table()

    def update_table(self):
        # Update page number buttons
        self.generate_page_buttons()
        # Update page input field
        self.page_input.setText(str(self.current_page))
        self.signal_update_table.emit((self.current_page, self.rows_per_page))

class ItemWithCloseButton(QWidget):

    def __init__(self, parent=None, title=None):
        super().__init__(parent)
        self.title = title
        self.load_ui()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget = QWidget()
        self.stacked_layout = QHBoxLayout(self.stacked_widget)
        self.stacked_layout.setContentsMargins(8, 14, 0, 0)

        self.widget_title = QWidget()
        self.widget_title.setStyleSheet('background-color: lightblue; color: white; border-radius: 4px')
        self.layout_title = QHBoxLayout()

        self.label_title = QLabel(self.title)
        self.layout_title.addWidget(self.label_title)
        self.widget_title.setLayout(self.layout_title)

        layout_content = QHBoxLayout()
        layout_content.setSpacing(4)
        layout_content.setContentsMargins(0, 0, 0, 0)
        widget_content = QWidget()
        widget_content.setObjectName('main_widget')
        self.stacked_layout.addWidget(self.widget_title)

        self.close_btn = QSvgWidget()
        self.close_btn.mousePressEvent = self.click_close_item
        self.close_btn.load('/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/remove_item_btn.svg')
        self.close_btn.setFixedSize(18, 18)
        self.widget_close_btn = QWidget(self.stacked_widget)
        self.layout_close_btn = QHBoxLayout()
        self.layout_close_btn.setContentsMargins(8, 4, 0, 0)
        self.layout_close_btn.setContentsMargins(0, 0, 0, 0)
        self.layout_close_btn.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout_close_btn.addWidget(self.close_btn)
        self.widget_close_btn.setLayout(self.layout_close_btn)

        layout_content.addWidget(self.stacked_widget)
        widget_content.setLayout(layout_content)

        self.main_layout.addWidget(widget_content)
        self.setLayout(self.main_layout)
        self.setStyleSheet('background-color: transparent')

    def click_close_item(self, event):
        print(f"HanhLT: click_close_item")


class CustomInputWithCloseItem(QWidget):
    signal_update_table = Signal(tuple)

    def __init__(self, parent=None, limit_length: int = 50, title=None, is_required_fields=False, use_ui_custom=False):
        super().__init__(parent)
        self.limit_length = limit_length
        self.title = title
        self.is_required_fields = is_required_fields
        if use_ui_custom:
            self.load_new_ui()
        else:
            self.load_ui()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(4)
        self.label_title = QLabel()
        if self.is_required_fields:
            title_text = self.title
            html_title = f'<span style="color: white;">{title_text} </span><span style="color: red;">*</span>'
        else:
            html_title = self.title
        self.label_title.setText(html_title)

        self.layout_content = QHBoxLayout()

        layout_content = QHBoxLayout()
        layout_content.setSpacing(4)
        layout_content.setContentsMargins(4, 4, 4, 4)

        self.line_edit = QLineEdit()
        self.line_edit.setMaxLength(self.limit_length)
        self.line_edit.setFixedHeight(32)
        self.line_edit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.line_edit.textChanged.connect(self.line_edit_text_change)

        widget_content = QWidget()
        widget_content.setObjectName('main_widget')


        item = ItemWithCloseButton(title='HanhLT')
        item2 = ItemWithCloseButton(title='Nhom system administrator')
        item3 = ItemWithCloseButton(title='HanhLT')

        ly = QHBoxLayout()
        ly.setSpacing(2)
        ly.addWidget(item)
        ly.addWidget(item2)
        ly.addWidget(item3)
        widget_content.setLayout(ly)

        self.main_layout.addWidget(widget_content)

        self.setLayout(self.main_layout)
        self.setup_stylesheet()

    def load_new_ui(self):
        pass

    def line_edit_text_change(self, text):
        print(f"HanhLT: on text change = {len(text)} ")
        self.label_amount.setText(f'{len(text)}')

    def enter_event_svg_widget(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enter_event_widget_numer(self, event):
        self.setCursor(Qt.CursorShape.IBeamCursor)

    def mousePressEvent(self, event):
        self.line_edit.setFocus()
        print(f"HanhLT: mouse click")

    def clear_click(self, event):
        self.line_edit.clear()
        self.label_amount.setText(f'0')

    def setup_stylesheet(self):
        self.setStyleSheet(
            f'''
                QWidget#main_widget {{
                    background-color: white;
                    color: black;
                    border-radius: 4px;
                }}

                QLineEdit:disabled {{
                    color: gray;
                    background-color: lightgray;
                }}

                QLineEdit {{
                    color: gray;
                    background-color: white;
                    border: none;
                    border-radius: 4px;
                }}

                QLineEdit:focus {{
                    color: white;
                    background-color: green;
                    border: none;
                    border-radius: 4px;
                }}

                QCheckBox:disabled {{
                    color: gray;
                }}
                QComboBox:disabled {{
                    color: gray;
                    background-color: lightgray;
                }}
        ''')

class CustomInput(QWidget):
    signal_update_table = Signal(tuple)

    def __init__(self, parent=None, limit_length: int = 50, title=None, is_required_fields=False, use_ui_custom=False):
        super().__init__(parent)
        self.limit_length = limit_length
        self.title = title
        self.is_required_fields = is_required_fields
        if use_ui_custom:
            self.load_new_ui()
        else:
            self.load_ui()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(4)
        self.label_title = QLabel()
        if self.is_required_fields:
            title_text = self.title
            html_title = f'<span style="color: white;">{title_text} </span><span style="color: red;">*</span>'
        else:
            html_title = self.title
        self.label_title.setText(html_title)

        self.layout_content = QHBoxLayout()

        layout_content = QHBoxLayout()
        layout_content.setSpacing(4)
        layout_content.setContentsMargins(4, 4, 4, 4)

        self.line_edit = QLineEdit()
        self.line_edit.setMaxLength(self.limit_length)
        self.line_edit.setFixedHeight(32)
        self.line_edit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.line_edit.textChanged.connect(self.line_edit_text_change)

        widget_number = QWidget()
        layout_numer = QHBoxLayout()
        layout_numer.setSpacing(2)
        layout_numer.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_numer.setContentsMargins(0, 0, 0, 0)
        svg_widget = QSvgWidget()
        svg_widget.enterEvent = self.enter_event_svg_widget
        svg_widget.mousePressEvent = self.clear_click
        svg_widget.load('/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/close.svg')
        svg_widget.setFixedSize(12, 12)
        self.label_limit = QLabel(f'/{str(self.limit_length)}')
        self.label_limit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)

        self.label_amount = QLabel('0')
        self.label_amount.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.label_amount.setFixedWidth(16)

        layout_amount = QHBoxLayout()
        layout_amount.setContentsMargins(0, 0, 0, 0)
        layout_amount.setSpacing(0)
        layout_amount.addWidget(self.label_amount)
        layout_amount.addWidget(self.label_limit)
        widget_amount = QWidget()
        widget_amount.enterEvent = self.enter_event_widget_numer
        widget_amount.setLayout(layout_amount)

        layout_numer.addWidget(svg_widget)
        layout_numer.addWidget(widget_amount)
        widget_number.setLayout(layout_numer)

        layout_content.addWidget(self.line_edit, 90)
        layout_content.addWidget(widget_number, 10)

        widget_content = QWidget()
        widget_content.setObjectName('main_widget')
        widget_content.setLayout(layout_content)

        item = ItemWithCloseButton(title='HanhLT')
        item2 = ItemWithCloseButton(title='Nhom system administrator')
        item3 = ItemWithCloseButton(title='HanhLT')

        ly=QHBoxLayout()
        ly.setSpacing(2)
        ly.addWidget(item)
        ly.addWidget(item2)
        ly.addWidget(item3)

        self.main_layout.addLayout(ly)

        self.main_layout.addWidget(self.label_title)
        self.main_layout.addWidget(widget_content)
        self.setLayout(self.main_layout)
        self.setup_stylesheet()

    def focus_event(self, QFocusEvent):
        print(f"HanhLT: hereeee")

    def focus_out(self, QFocusEvent):
        print(f"HanhLT: hereeee  33333")

    def load_new_ui(self):
       pass

    def line_edit_text_change(self, text):
        print(f"HanhLT: on text change = {len(text)} ")
        self.label_amount.setText(f'{len(text)}')

    def enter_event_svg_widget(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enter_event_widget_numer(self, event):
        self.setCursor(Qt.CursorShape.IBeamCursor)

    def mousePressEvent(self, event):
        self.line_edit.setFocus()
        print(f"HanhLT: mouse click")

    def clear_click(self, event):
        self.line_edit.clear()
        self.label_amount.setText(f'0')

    def setup_stylesheet(self):
        self.setStyleSheet(
            f'''
                QWidget#main_widget {{
                    background-color: transparent;
                    color: black;
                    border-radius: 4px;
                    border: 1px solid red;
                }}
                
                QLineEdit:disabled {{
                    color: gray;
                    background-color: lightgray;
                }}
                
                QLineEdit {{
                    color: gray;
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }}
                
                QLineEdit:focus {{
                    color: white;
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }}
                
                QCheckBox:disabled {{
                    color: gray;
                }}
                QComboBox:disabled {{
                    color: gray;
                    background-color: lightgray;
                }}
        ''')

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        # Table
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        # Set the model to the table view
        self.table_view.setModel(self.model)

        self.pagination = CustomPagination(total_rows=200)
        self.pagination.signal_update_table.connect(self.update_table)

        # Custom Line Edit
        self.line_edit = QLineEdit()
        self.showPassAction = QAction(QIcon('/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/close.svg'), self.tr("Show password"), self)
        self.showPassAction = QAction(QIcon('/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/close.svg'),
                                      self.tr("Show password"), self)
        # self.showPassAction.triggered.connect(self.togglePasswordVisibility)

        label_test = QLabel("0/10")
        btn = QPushButton('jhhh')
        btn.setFixedWidth(24)
        custom_widget = QWidget()
        grid_layout = QHBoxLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        svg_widget = QSvgWidget()
        svg_widget.load('/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/close.svg')
        svg_widget.setFixedSize(24, 24)
        grid_layout.addWidget(label_test)
        grid_layout.addWidget(btn)
        custom_widget.setLayout(grid_layout)

        # Create and set the custom action
        self.custom_action = QWidgetAction(self.line_edit)
        self.custom_action.setDefaultWidget(custom_widget)
        self.line_edit.addAction(self.custom_action, QLineEdit.ActionPosition.TrailingPosition)

        custom_input = CustomInput(title='Username', is_required_fields=True)
        custom_input_close_item = CustomInputWithCloseItem(title='System user group', is_required_fields=True)
        self.main_layout.addWidget(custom_input_close_item)
        self.main_layout.addWidget(custom_input)
        self.main_layout.addWidget(self.line_edit)
        self.main_layout.addWidget(self.table_view)
        self.main_layout.addWidget(self.pagination)
        self.pagination.update_table()

        self.setLayout(self.main_layout)

    def update_table(self, data):
        current_page, rows_per_page = data
        # Clear current table data
        self.model.clear()

        # Add data for the current page
        start_row = (current_page - 1) * rows_per_page
        end_row = min(start_row + rows_per_page, 200)

        for row in range(start_row, end_row):
            items = [QStandardItem(f"Item {row+1} - {col+1}") for col in range(3)]
            self.model.appendRow(items)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec())
