import sys
from PySide6.QtCore import Qt, QRect, QAbstractTableModel
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHeaderView, QCheckBox, \
    QHBoxLayout, QAbstractItemView, QPushButton, QLabel
from PySide6.QtGui import QStandardItemModel, QStandardItem

class CheckableHeader(QHeaderView):
    def __init__(self, orientation, parent=None, list_header_element: dict[int, QWidget] = None):
        super().__init__(orientation, parent)
        if list_header_element is None:
            list_header_element = {}
        self.isChecked = False
        self.list_header_element = list_header_element

        self.setSectionsClickable(True)

    def paintSection(self, painter, rect, logicalIndex):
        super().paintSection(painter, rect, logicalIndex)
        print(f"HanhLT: logicalIndex = {logicalIndex}")
        for index, widget in self.list_header_element.items():
            print(f"HanhLT: index = {index}  widget = {widget} ")
            if index == logicalIndex:
                widget.setParent(self)
                widget.setGeometry(rect)
                widget.show()

        # if logicalIndex == 0:
        #     print(f"HanhLT: rect = {rect.width()}")
        #     self.widget_checkbox.setGeometry(rect)
        # elif logicalIndex == 3:
        #     self.widget_button.setGeometry(rect)

    def check_all(self, state):
        self.parentWidget().check_all(state == Qt.CheckState.Checked)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableView with Header Checkbox Example")
        self.setGeometry(100, 100, 600, 400)

        # Create a QTableView
        self.table = QTableView(self)

        # Create a QStandardItemModel
        self.model = QStandardItemModel(4, 5)  # 4 rows, 3 columns
        self.model.setHorizontalHeaderLabels(["", "Column 2", "Column 3", "", ""])
        # Set the model for the table view
        self.table.setModel(self.model)

        # Add checkboxes to the first column and text to the other columns
        for row in range(4):
            checkbox_item = QStandardItem()
            checkbox_item.setCheckable(True)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.model.setItem(row, 0, checkbox_item)
            self.model.setItem(row, 1, QStandardItem(f"Text {row + 1}"))
            item = QStandardItem()
            item.setData(QLabel('HanhLT'), Qt.UserRole)
            self.model.setItem(row, 2, QStandardItem(f"Text {row + 1}"))
            self.model.setItem(row, 3, QStandardItem(f"Text {row + 1}"))
            self.model.setItem(row, 4, QStandardItem(f"Text {row + 1}"))

        widget_checkbox = QWidget()
        layout_checkbox = QVBoxLayout()
        layout_checkbox.setContentsMargins(0, 0, 0, 0)
        layout_checkbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(self.check_all)
        checkbox.setTristate(False)
        layout_checkbox.addWidget(checkbox)
        widget_checkbox.setLayout(layout_checkbox)

        widget_button = QWidget()
        layout_button = QHBoxLayout(widget_button)
        layout_button.setContentsMargins(0, 0, 0, 0)
        btn1 = QPushButton('BTN 1')
        btn2 = QPushButton('BTN 2')
        layout_button.addWidget(btn1)
        layout_button.addWidget(btn2)
        header_element = {0: widget_checkbox, 3: widget_button}
        # Set the custom header for the first column
        header = CheckableHeader(Qt.Orientation.Horizontal, self.table, list_header_element=header_element)
        self.table.setHorizontalHeader(header)

        button = QPushButton('ADD ITEM')
        button.clicked.connect(self.add_item_to_table)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_all(self, checked):
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item is not None:
                item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)

    def add_item_to_table(self):
        row_count = self.model.rowCount()
        self.model.insertRow(row_count)
        checkbox_item = QStandardItem()
        checkbox_item.setCheckable(True)
        checkbox_item.setCheckState(Qt.CheckState.Unchecked)
        self.model.setItem(row_count, 0, checkbox_item)
        self.model.setItem(row_count, 1, QStandardItem(f"New Text {row_count + 1}"))
        item = QStandardItem()
        item.setData(QLabel('New HanhLT'), Qt.UserRole)
        self.model.setItem(row_count, 2, item)
        self.model.setItem(row_count, 3, QStandardItem(f"New Text {row_count + 1}"))
        self.model.setItem(row_count, 4, QStandardItem(f"New Text {row_count + 1}"))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
