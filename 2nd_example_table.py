import sys
from PySide6.QtCore import Qt, QRect, QModelIndex
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHeaderView,
    QCheckBox, QStyledItemDelegate, QHBoxLayout, QPushButton, QStyleOptionButton, QStyle
)
from PySide6.QtCore import QAbstractTableModel


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            return Qt.CheckState.Checked if self._data[index.row()][index.column()] else Qt.CheckState.Unchecked

        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            self._data[index.row()][index.column()] = value == Qt.CheckState.Checked
            self.dataChanged.emit(index, index, [role])
            return True

        return super().setData(index, value, role)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]

        if orientation == Qt.Orientation.Vertical:
            return section + 1

        return None

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable
        return Qt.ItemFlag.ItemIsEnabled


class CustomHeader(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setStretchLastSection(True)
        self.setSectionsClickable(True)
        self.checkbox = QCheckBox(self)
        self.checkbox.setTristate(False)
        self.checkbox.stateChanged.connect(self.check_all)
        self.setStyleSheet("QCheckBox { margin-left: 5px; }")

    def paintSection(self, painter, rect, logicalIndex):
        super().paintSection(painter, rect, logicalIndex)
        if logicalIndex == 0:  # Assuming checkbox is only for the first column
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + 3, rect.y() + 2, 20, 20)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.checkbox.isChecked():
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter, self.checkbox)

    def check_all(self, state):
        parent = self.parentWidget()
        for row in range(parent.model().rowCount()):
            index = parent.model().index(row, 0)
            parent.model().setData(index,
                                   Qt.CheckState.Checked if state == Qt.CheckState.Checked else Qt.CheckState.Unchecked,
                                   Qt.ItemDataRole.CheckStateRole)


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 2:
            editor = QWidget()
            layout = QHBoxLayout(editor)
            btn1 = QPushButton('BTN 1')
            btn2 = QPushButton('BTN 2')
            layout.addWidget(btn1)
            layout.addWidget(btn2)
            layout.setContentsMargins(0, 0, 0, 0)
            editor.setGeometry(option.rect)
            editor.render(painter, option.rect.topLeft())
        else:
            super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        # Prevent the editor from being created
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QAbstractTableModel with Header Checkbox and Cell Widgets")
        self.setGeometry(100, 100, 600, 400)

        # Sample data
        data = [
            [False, "Alice", ""],
            [False, "Bob", ""],
            [False, "Charlie", ""],
            [False, "David", ""],
        ]
        headers = ["", "Name", "Actions"]

        # Create and set the model
        self.model = CustomTableModel(data, headers)

        # Create QTableView and set the model
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # Set the custom header for the first column
        header = CustomHeader(Qt.Orientation.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(header)

        # Set the custom delegate for the third column
        delegate = CustomDelegate()
        self.table_view.setItemDelegateForColumn(2, delegate)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
