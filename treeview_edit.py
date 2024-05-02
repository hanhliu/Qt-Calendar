import json
import os
import pickle
import sys

import PySide6
from PySide6.QtCore import Qt, QEvent, QMimeData
from PySide6.QtGui import QStandardItem, QStandardItemModel, QAction, QKeySequence, QColor
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QTreeView, QFrame, QMenu, QHBoxLayout, \
    QStackedWidget, QLabel, QTextEdit, QPushButton, QStyledItemDelegate


class EditableTreeView(QTreeView):
    def __init__(self, parent=None, model_data=None, callback_keyPressEvent=None):
        super().__init__(parent)
        self.setEditTriggers(QTreeView.NoEditTriggers)
        # self.setFocusPolicy(Qt.NoFocus)
        self.model_data = model_data
        self.callback_keyPressEvent = callback_keyPressEvent

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up or key == Qt.Key.Key_Down or key == Qt.Key.Key_Right or key == Qt.Key.Key_Left:
            event.ignore()  # Ngăn chặn xử lý sự kiện phím mũi tên lên xuống
        else:
            super().keyPressEvent(event)

class CustomStandardItemModel(QStandardItemModel):
    def mimeData(self, indexes):
        print(f"HanhLT: len(indexes) = {len(indexes)}")
        mime_data = super(CustomStandardItemModel, self).mimeData(indexes)
        text_list = []
        object_name_list = []
        text_and_userRole_dict = {}
        for index in indexes:
            if index.isValid():
                text_data = index.data()
                userRole_data = index.data(Qt.UserRole)
                text_list.append(text_data)
                object_name_list.append(userRole_data)
                text_and_userRole_dict[text_data] = userRole_data

        mime_data.setText("\n".join(text_list))
        mime_text = mime_data.text()
        text_list = mime_text.split('\n')
        print(f"HanhLT: mime_data.text() = {text_list}")
        json_data = pickle.dumps(text_and_userRole_dict)
        print(f"HanhLT: json_data = {json_data}")
        # byte_array = json_data.encode('utf-8')
        mime_data.setData("application/multidata", json_data)

        data = mime_data.data("application/multidata")
        retrieved_byte_array = mime_data.data("application/multidata")
        retrieved_data_dict = pickle.loads(retrieved_byte_array)

        # # Convert QByteArray to Python bytes object
        # byte_data = bytes(retrieved_byte_array)
        #
        # # Decode the byte array and deserialize JSON back into a dictionary
        # retrieved_data_dict = pickle.loads(byte_data.decode('utf-8'))
        print(f"HanhLT: retrieved_data_list = {retrieved_data_dict}")


        return mime_data
        # mimedata = super(CustomStandardItemModel, self).mimeData(indexes)
        # if indexes:
        #     mimedata.setText(indexes[0].data())
        #     mimedata.setObjectName(indexes[0].data(Qt.UserRole))
        # return mimedata
class CustomItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if index.data(Qt.UserRole) == "highlighted":
            option.palette.setColor(option.palette.Base, Qt.red)  # Change the background color to red
        super().paint(painter, option, index)
class TreeViewEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.model = CustomStandardItemModel()
        self.model.invisibleRootItem()
        # Create root item
        self.root_item = QStandardItem("Root")
        self.root_item.setData("root_item", Qt.UserRole)
        self.model.appendRow(self.root_item)

        # Create child items
        child_item1 = QStandardItem("Child 1")
        child_item1.setData("child_item", Qt.UserRole)
        child_item2 = QStandardItem("Child 2")
        child_item2.setData("child_item", Qt.UserRole)
        self.root_item.appendRow(child_item1)
        self.root_item.appendRow(child_item2)

        # Create a subchild item
        group_1 = QStandardItem("Group Camera 1")
        group_1.setData("group_camera", Qt.UserRole)
        # Create sub-subchild items
        camera_1 = QStandardItem("Camera 1")
        camera_2 = QStandardItem("Camera 2")
        camera_3 = QStandardItem("Camera 3")
        camera_4 = QStandardItem("Camera 4")
        camera_1.setData("camera_item", Qt.UserRole)
        camera_2.setData("camera_item", Qt.UserRole)
        camera_3.setData("camera_item", Qt.UserRole)
        camera_4.setData("camera_item", Qt.UserRole)
        group_1.appendRow(camera_1)
        group_1.appendRow(camera_2)
        group_1.appendRow(camera_3)
        group_1.appendRow(camera_4)

        group_2 = QStandardItem("Group Camera 2")
        group_2.setData("group_camera", Qt.UserRole)
        camera_5 = QStandardItem("Camera 5")
        camera_5.setData("camera_item", Qt.UserRole)
        camera_6 = QStandardItem("Camera 6")
        camera_6.setData("camera_item", Qt.UserRole)
        group_2.appendRow(camera_5)
        group_2.appendRow(camera_6)

        group_3 = QStandardItem("Group Camera 3")
        group_3.setData("group_camera", Qt.UserRole)
        camera_7 = QStandardItem("Camera 7")
        camera_7.setData("camera_item", Qt.UserRole)
        camera_8 = QStandardItem("Camera 8")
        camera_8.setData("camera_item", Qt.UserRole)
        camera_9 = QStandardItem("Camera 9")
        camera_9.setData("camera_item", Qt.UserRole)
        camera_10 = QStandardItem("Camera 10")
        camera_10.setData("camera_item", Qt.UserRole)
        group_3.appendRow(camera_7)
        group_3.appendRow(camera_8)
        group_3.appendRow(camera_9)
        group_3.appendRow(camera_10)

        child_item1.appendRow(group_1)
        child_item1.appendRow(group_2)
        child_item1.appendRow(group_3)

        # Create the tree view and set the model
        self.tree_view = EditableTreeView()
        self.tree_view.setItemDelegate(CustomItemDelegate())
        self.tree_view.setObjectName("Treeview")
        self.tree_view.installEventFilter(self)
        self.tree_view.setFixedHeight(300)
        self.tree_view.setModel(self.model)

        self.tree_view.viewport().setAcceptDrops(False)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setFrameShape(QTreeView.Shape.NoFrame)
        self.tree_view.setFrameShadow(QFrame.Shadow.Plain)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setDragDropMode(QTreeView.DragDropMode.DragOnly)
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.tree_view.setDragDropOverwriteMode(True)
        self.tree_view.setDropIndicatorShown(True)
        # Connect context menu event to custom slot
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_view.dragLeaveEvent = self.dragLeaveEvent
        self.tree_view.expandAll()
        # self.tree_view.dragMoveEvent = self.drag_leave_event
        # self.tree_view.startDrag = self.start_Drag

        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.tree_view)
        self.setLayout(self.layout)

    def show_context_menu(self, pos):
        # Get the global position of the context menu
        global_pos = self.tree_view.viewport().mapToGlobal(pos)

        selected_indexes = self.tree_view.selectedIndexes()
        if len(selected_indexes) == 1:
            item = self.model.itemFromIndex(selected_indexes[0])
        else:
            pass
        unique_data_values = set()
        selected_items = []
        list_camera = []

        # Iterate over selected items
        for index in selected_indexes:
            item = self.model.itemFromIndex(index)
            if item is not None:
                # Get item data
                item_data = item.data(Qt.UserRole)
                if item_data is not None:
                    unique_data_values.add(item_data)
                    selected_items.append(item)

        # Check if all selected items have the same item data or different item data
        if len(unique_data_values) == 1:
            item_data = unique_data_values.pop()
            # Add actions based on the item data
            if item_data == "camera_item":
                list_camera = selected_items
            elif item_data == "group_camera":
                for group in selected_items:
                    if group.rowCount() > 0:
                        for camera_index in range(group.rowCount()):
                            camera = group.child(camera_index)
                            list_camera.append(camera)
        else:
            for item in selected_items:
                item_data = item.data(Qt.UserRole)
                if item_data not in ["camera_item", "group_camera"]:
                    return

            group_items = [item for item in selected_items if item.data(Qt.UserRole) == "group_camera"]
            camera_items = [item for item in selected_items if item.data(Qt.UserRole) == "camera_item"]

            for group in group_items:
                if group.rowCount() > 0:
                    for camera_index in range(group.rowCount()):
                        camera = group.child(camera_index)
                        list_camera.append(camera)
            for camera_item in camera_items:
                if camera_item not in list_camera:
                    list_camera.append(camera_item)

        # Create a context menu
        menu = QMenu(self)
        action_create_group = QAction(text=self.tr("Create group"), parent=menu)
        action_delete = QAction(text=self.tr("Delete"), parent=menu)
        menu.addAction(action_create_group)
        menu.addAction(action_delete)
        menu.exec(global_pos)

    def action_for_root_item(self):
        print("Action for root item")

    def action_for_child_item(self):
        print("Action for child item")

    def common_action(self):
        print("Common Action")

    def check_selected_items(self):
        selected_indexes = self.tree_view.selectedIndexes()
        unique_data_values = set()

        # Iterate over selected items
        for index in selected_indexes:
            item = self.model.itemFromIndex(index)
            if item is not None:
                # Get item data
                item_data = item.data(Qt.UserRole)
                if item_data is not None:
                    unique_data_values.add(item_data)

        # Check if all selected items have the same item data or different item data
        if len(unique_data_values) == 1:
            print("All selected items have the same item data:", unique_data_values.pop())
        else:
            print("Selected items have different item data:", unique_data_values)

class CustomWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.load_ui()

    def load_ui(self):
        self.setStyleSheet('background-color: lightblue')
        self.addWidget(QLabel('HANHLT'))

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasText():
            text = mime_data.text()
            obj_name = mime_data.objectName()
            event.acceptProposedAction()
        event.accept()
        
    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dragLeaveEvent(self, event):
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout()
        self.treeview_widget = TreeViewEdit()
        custom_widget = CustomWidget()
        custom_widget.setFixedSize(100, 100)
        self.button_custom = QPushButton("Press")
        self.button_custom.clicked.connect(self.button_clicked)
        self.central_layout.addWidget(self.treeview_widget)
        self.central_layout.addWidget(custom_widget)
        self.central_layout.addWidget(self.button_custom)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def find_item_by_name(self, item, name):
        if item.text() == name:
            return item

        # Recursively search through children
        for row in range(item.rowCount()):
            child = item.child(row)
            found_item = self.find_item_by_name(child, name)
            if found_item:
                return found_item

        return None

    def change_item_color(self, item_name, color):
        # Start searching from the root item
        root_item = self.model.invisibleRootItem()
        item = self.find_item_by_name(root_item, item_name)
        if item:
            # Apply custom stylesheet to change the item's color
            item.setStyleSheet(f"color: {color};")
    def button_clicked(self):
        # Start searching from the root item
        item_name = "Camera 3"
        root_item = self.treeview_widget.model.invisibleRootItem()
        item = self.find_item_by_name(root_item, item_name)
        if item:
            # Apply custom stylesheet to change the item's color
            item.setBackground(QColor(255, 0, 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())