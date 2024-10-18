import json
import os
import pickle
import sys

import PySide6
from PySide6.QtCore import Qt, QEvent, QMimeData
from PySide6.QtGui import QStandardItem, QStandardItemModel, QAction, QKeySequence, QColor
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QTreeView, QFrame, QMenu, QHBoxLayout, \
    QStackedWidget, QLabel, QTextEdit, QPushButton, QStyledItemDelegate, QTreeWidget, QTreeWidgetItem


# class RecursiveCheckableTreeView(QTreeView):
#     def __init__(self):
#         super().__init__()
#
#         # Create a standard model for the tree view
#         self.model = QStandardItemModel()
#         self.model.setHorizontalHeaderLabels(['Items'])
#
#         # Populate the tree view with checkable items
#         self.root_item = self.model.invisibleRootItem()
#         self.root_item.setFlags(Qt.ItemFlag.ItemIsAutoTristate)
#         self.populate_tree(self.root_item)
#
#         self.setModel(self.model)
#         self.expandAll()
#         self.setEditTriggers(QTreeView.EditTrigger.DoubleClicked)
#         # self.pressed.connect(self.on_tree_view_clicked)
#
#         # Avoid using itemChanged directly to prevent recursive state changes
#         self.blocked = False
#         self.test_flag = False
#
#         # Connect the itemChanged signal to handle the checking and unchecking of items
#         # self.model.itemChanged.connect(self.handle_item_changed)
#
#     def on_tree_view_clicked(self, index):
#         print(f"HanhLT: on_tree_view_clicked")
#         item = self.model.itemFromIndex(index)
#         if item.checkState() == Qt.CheckState.Checked:
#             item.setCheckState(Qt.CheckState.Unchecked)
#         else:
#             item.setCheckState(Qt.CheckState.Checked)
#         state = item.checkState()
#         self.check_state_item(item, state)
#
#     def populate_tree(self, parent_item):
#         """Populate the tree with some checkable items and nested child items."""
#         # Example of nested checkable items
#         root_item = QStandardItem('Root')
#         root_item.setCheckable(True)
#         # root_item.setFlags(Qt.ItemFlag.ItemIsAutoTristate)
#         for i in range(1, 4):
#             subchild = QStandardItem(f'Subchild {i}')
#             subchild.setCheckable(True)
#             # subchild.setFlags(Qt.ItemFlag.ItemIsAutoTristate)
#             for j in range(1, 4):
#                 child = QStandardItem(f'Child {i}.{j}')
#                 child.setCheckable(True)
#                 subchild.appendRow(child)
#
#             root_item.appendRow(subchild)
#
#         parent_item.appendRow(root_item)
#
#     # def mousePressEvent(self, event):
#     #     """Override mousePressEvent to manually handle check state changes."""
#     #     index = self.indexAt(event.position().toPoint())
#     #     item = self.model.itemFromIndex(index)
#     #
#     #     if item and item.isCheckable():
#     #         current_state = item.checkState()
#     #         new_state = Qt.Checked if current_state == Qt.Unchecked else Qt.Unchecked
#     #         # Update the item and propagate the state
#     #         item.setCheckState(new_state)
#     #         self.check_state_item(item, new_state)
#     #     super().mousePressEvent(event)
#
#     def check_state_item(self, item: QStandardItem, check_state):
#         """Manually handle checking/unchecking an item and its child/parent propagation."""
#         if self.blocked:
#             return  # Prevent recursive calls
#
#         # Block signal handling temporarily
#         self.blocked = True
#
#         # Update child items' state
#         self.update_children_check_state(item, check_state)
#         print(f"HanhLT: chay vao day")
#         # Update parent items' state
#         # self.update_parent_check_state(item)
#
#         # Unblock signal handling
#         self.blocked = False
#
#     def update_children_check_state(self, item, check_state):
#         """Recursively set the check state for all children based on the parent item's state."""
#         for row in range(item.rowCount()):
#             child = item.child(row)
#             child.setCheckState(check_state)
#             self.update_children_check_state(child, check_state)
#
#     def update_parent_check_state(self, item):
#         """Recursively update the parent check state based on the child items' check states."""
#         parent = item.parent()
#         if not parent:
#             return  # If there's no parent, stop
#
#         checked_count = 0
#         unchecked_count = 0
#
#         # Count the number of checked and unchecked children
#         for row in range(parent.rowCount()):
#             sibling = parent.child(row)
#             if sibling.checkState() == Qt.Checked:
#                 checked_count += 1
#             elif sibling.checkState() == Qt.Unchecked:
#                 unchecked_count += 1
#         print(f"HanhLT: unchecked_count = {unchecked_count} == parent.rowCount() = {parent.rowCount()} ==== {unchecked_count == parent.rowCount()}")
#         # Update parent's check state based on the children's states
#         # if checked_count == parent.rowCount():
#         #     parent.setCheckState(Qt.Checked)  # All children are checked
#         # elif unchecked_count == parent.rowCount():
#         #     print(f"HanhLT: here")
#         #     parent.setCheckState(Qt.Unchecked)  # All children are unchecked
#         # else:
#         #     parent.setCheckState(Qt.PartiallyChecked)  # Mixed check state
#
#         # Recursively update the parent's parent
#         # self.update_parent_check_state(parent)
#
#     def handle_item_changed(self, item):
#         """Handle checking/unchecking the item and its children."""
#         state = item.checkState()
#         print(f"HanhLT: item state = {state}")
#
#         self.check_state_item(item, state)
#
#     def check_state_item_2(self, item: QStandardItem, check_state):
#         # Check state for child item
#         for row in range(item.rowCount()):
#             child = item.child(row)
#             child.setCheckState(check_state)
#
#         parent: QStandardItem = item.parent()
#         if parent is not None:
#             parent.setCheckState(Qt.CheckState.PartiallyChecked)
#
#         # parent_of_parent: QStandardItem = parent.parent()
#         # if parent_of_parent is not None:
#         #     pass
#         # else:
#         #     pass
#
#         # print(f"HanhLT: parent text = {parent.text()}       parent_of_parent = {parent_of_parent.text()}")
#
#         # Change state for parent and parent of parent
#         # TH1: check single box
#         # TH2: check full children box
#         # TH3: clear single box
#         # Th4: clear all box


# Create and display the tree view

class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, item_model=None, server_ip=None):
        super().__init__(parent)
        self.server_ip = server_ip
        self.item_model = item_model

class RecursiveCheckableTreeView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a standard model for the tree view
        # self.model = QStandardItemModel()
        # self.model.setHorizontalHeaderLabels(['Items'])
        #
        # # Populate the tree view with checkable items
        # self.root_item = self.model.invisibleRootItem()
        # self.root_item.setFlags(Qt.ItemFlag.ItemIsAutoTristate)
        # self.populate_tree(self.root_item)
        #
        # self.setModel(self.model)
        # self.expandAll()
        # self.setEditTriggers(QTreeView.EditTrigger.DoubleClicked)
        # self.pressed.connect(self.on_tree_view_clicked)
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.parent_item = QTreeWidgetItem(self.tree_widget)
        self.parent_item.setText(0, 'ALL')
        self.parent_item.setFlags(self.parent_item.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.populate_tree(self.parent_item)

        # for i in range(3):
        #
        #     parent.setText(0, "Parent {}".format(i))
        #     parent.setFlags(parent.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        #     for x in range(5):
        #         child = QTreeWidgetItem(parent)
        #         child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
        #         child.setText(0, "Child {}".format(x))
        #         child.setCheckState(0, Qt.Unchecked)
        # self.tree_widget.setHeaderItem(self.parent_item)
        root_index = self.tree_widget.indexFromItem(self.parent_item)
        self.tree_widget.setExpanded(root_index, True)
        self.tree_widget.itemClicked.connect(self.item_clicked)

        # Avoid using itemChanged directly to prevent recursive state changes
        self.blocked = False
        self.test_flag = False

        self.btn_test = QPushButton('Test')
        self.btn_test.clicked.connect(self.btn_clicked)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tree_widget)
        self.main_layout.addWidget(self.btn_test)
        self.setLayout(self.main_layout)

    def populate_tree(self, parent_item):
        for i in range(3):
            parent = CustomQTreeWidgetItem(parent=parent_item, item_model="Modelll", server_ip='192.168')
            parent.setText(0, "Parent {}".format(i))
            parent.setData(0, Qt.UserRole, f"Parent {i}")
            parent.setFlags(parent.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemIsUserCheckable)
            for x in range(5):
                child = CustomQTreeWidgetItem(parent, item_model="Modelll", server_ip='192.168')
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, "Child {}".format(x))
                child.setData(0, Qt.UserRole, f"Child {x}")
                child.setCheckState(0, Qt.Unchecked)

    def btn_clicked(self):
        print(f"HanhLT: test")
        for i in range(self.tree_widget.topLevelItemCount()):
            top_level_item = self.tree_widget.topLevelItem(i)
            self.print_item_data(top_level_item)

    def print_item_data(self, item, indent=0):
        # Print the item data
        indent_str = "  " * indent  # for hierarchical visualization
        if hasattr(item, 'item_model'):
            if item.item_model is not None:
                print(f"HanhLT: item model = {item.item_model}")
        print(
            f"{indent_str}Item Text: {item.text(0)}, Data: {item.data(0, Qt.UserRole)}, State: {item.checkState(0)}")

        # Recursively print the data of child items
        for i in range(item.childCount()):
            child_item = item.child(i)
            self.print_item_data(child_item, indent + 1)

    def item_clicked(self, item: CustomQTreeWidgetItem):
        print(f"HanhLT: data = {item}")
        state = item.checkState(0)
        print(f"HanhLT: state = {state}")
        item.setCheckState(0, Qt.CheckState.Checked if state != Qt.CheckState.Checked else Qt.CheckState.Unchecked)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.treeview = RecursiveCheckableTreeView()
        self.central_layout.addWidget(self.treeview)

        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


# class EditableTreeView(QTreeView):
#     def __init__(self, parent=None, model_data=None, callback_keyPressEvent=None):
#         super().__init__(parent)
#         self.setEditTriggers(QTreeView.NoEditTriggers)
#         # self.setFocusPolicy(Qt.NoFocus)
#         self.model_data = model_data
#         self.callback_keyPressEvent = callback_keyPressEvent
#
#     def keyPressEvent(self, event):
#         key = event.key()
#         if key == Qt.Key.Key_Up or key == Qt.Key.Key_Down or key == Qt.Key.Key_Right or key == Qt.Key.Key_Left:
#             event.ignore()  # Ngăn chặn xử lý sự kiện phím mũi tên lên xuống
#         else:
#             super().keyPressEvent(event)
#
# class CustomStandardItemModel(QStandardItemModel):
#     def mimeData(self, indexes):
#         print(f"HanhLT: len(indexes) = {len(indexes)}")
#         mime_data = super(CustomStandardItemModel, self).mimeData(indexes)
#         text_list = []
#         object_name_list = []
#         text_and_userRole_dict = {}
#         for index in indexes:
#             if index.isValid():
#                 text_data = index.data()
#                 userRole_data = index.data(Qt.UserRole)
#                 text_list.append(text_data)
#                 object_name_list.append(userRole_data)
#                 text_and_userRole_dict[text_data] = userRole_data
#
#         mime_data.setText("\n".join(text_list))
#         mime_text = mime_data.text()
#         text_list = mime_text.split('\n')
#         print(f"HanhLT: mime_data.text() = {text_list}")
#         json_data = pickle.dumps(text_and_userRole_dict)
#         print(f"HanhLT: json_data = {json_data}")
#         # byte_array = json_data.encode('utf-8')
#         mime_data.setData("application/multidata", json_data)
#
#         data = mime_data.data("application/multidata")
#         retrieved_byte_array = mime_data.data("application/multidata")
#         retrieved_data_dict = pickle.loads(retrieved_byte_array)
#
#         # # Convert QByteArray to Python bytes object
#         # byte_data = bytes(retrieved_byte_array)
#         #
#         # # Decode the byte array and deserialize JSON back into a dictionary
#         # retrieved_data_dict = pickle.loads(byte_data.decode('utf-8'))
#         print(f"HanhLT: retrieved_data_list = {retrieved_data_dict}")
#
#
#         return mime_data
#         # mimedata = super(CustomStandardItemModel, self).mimeData(indexes)
#         # if indexes:
#         #     mimedata.setText(indexes[0].data())
#         #     mimedata.setObjectName(indexes[0].data(Qt.UserRole))
#         # return mimedata
# class CustomItemDelegate(QStyledItemDelegate):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#     def paint(self, painter, option, index):
#         if index.data(Qt.UserRole) == "highlighted":
#             option.palette.setColor(option.palette.Base, Qt.red)  # Change the background color to red
#         super().paint(painter, option, index)
# class TreeViewEdit(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.load_ui()
#
#     def load_ui(self):
#         self.model = CustomStandardItemModel()
#         self.model.invisibleRootItem()
#         # Create root item
#         self.root_item = QStandardItem("Root")
#         self.root_item.setData("root_item", Qt.UserRole)
#         self.model.appendRow(self.root_item)
#
#         # Create child items
#         child_item1 = QStandardItem("Child 1")
#         child_item1.setData("child_item", Qt.UserRole)
#         child_item2 = QStandardItem("Child 2")
#         child_item2.setData("child_item", Qt.UserRole)
#         self.root_item.appendRow(child_item1)
#         self.root_item.appendRow(child_item2)
#
#         # Create a subchild item
#         group_1 = QStandardItem("Group Camera 1")
#         group_1.setData("group_camera", Qt.UserRole)
#         # Create sub-subchild items
#         camera_1 = QStandardItem("Camera 1")
#         camera_2 = QStandardItem("Camera 2")
#         camera_3 = QStandardItem("Camera 3")
#         camera_4 = QStandardItem("Camera 4")
#         camera_1.setData("camera_item", Qt.UserRole)
#         camera_2.setData("camera_item", Qt.UserRole)
#         camera_3.setData("camera_item", Qt.UserRole)
#         camera_4.setData("camera_item", Qt.UserRole)
#         group_1.appendRow(camera_1)
#         group_1.appendRow(camera_2)
#         group_1.appendRow(camera_3)
#         group_1.appendRow(camera_4)
#
#         group_2 = QStandardItem("Group Camera 2")
#         group_2.setData("group_camera", Qt.UserRole)
#         camera_5 = QStandardItem("Camera 5")
#         camera_5.setData("camera_item", Qt.UserRole)
#         camera_6 = QStandardItem("Camera 6")
#         camera_6.setData("camera_item", Qt.UserRole)
#         group_2.appendRow(camera_5)
#         group_2.appendRow(camera_6)
#
#         group_3 = QStandardItem("Group Camera 3")
#         group_3.setData("group_camera", Qt.UserRole)
#         camera_7 = QStandardItem("Camera 7")
#         camera_7.setData("camera_item", Qt.UserRole)
#         camera_8 = QStandardItem("Camera 8")
#         camera_8.setData("camera_item", Qt.UserRole)
#         camera_9 = QStandardItem("Camera 9")
#         camera_9.setData("camera_item", Qt.UserRole)
#         camera_10 = QStandardItem("Camera 10")
#         camera_10.setData("camera_item", Qt.UserRole)
#         group_3.appendRow(camera_7)
#         group_3.appendRow(camera_8)
#         group_3.appendRow(camera_9)
#         group_3.appendRow(camera_10)
#
#         child_item1.appendRow(group_1)
#         child_item1.appendRow(group_2)
#         child_item1.appendRow(group_3)
#
#         # Create the tree view and set the model
#         self.tree_view = EditableTreeView()
#         self.tree_view.setItemDelegate(CustomItemDelegate())
#         self.tree_view.setObjectName("Treeview")
#         self.tree_view.installEventFilter(self)
#         self.tree_view.setFixedHeight(300)
#         self.tree_view.setModel(self.model)
#
#         self.tree_view.viewport().setAcceptDrops(False)
#         self.tree_view.setDragEnabled(True)
#         self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
#         self.tree_view.setHeaderHidden(True)
#         self.tree_view.setFrameShape(QTreeView.Shape.NoFrame)
#         self.tree_view.setFrameShadow(QFrame.Shadow.Plain)
#         self.tree_view.setAlternatingRowColors(True)
#         self.tree_view.setDragDropMode(QTreeView.DragDropMode.DragOnly)
#         self.tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
#         self.tree_view.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
#         self.tree_view.setDragDropOverwriteMode(True)
#         self.tree_view.setDropIndicatorShown(True)
#         # Connect context menu event to custom slot
#         self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
#         self.tree_view.customContextMenuRequested.connect(self.show_context_menu)
#         self.tree_view.dragLeaveEvent = self.dragLeaveEvent
#         self.tree_view.expandAll()
#         # self.tree_view.dragMoveEvent = self.drag_leave_event
#         # self.tree_view.startDrag = self.start_Drag
#
#         # create layout
#         self.layout = QVBoxLayout()
#         self.layout.setAlignment(Qt.AlignTop)
#         self.layout.addWidget(self.tree_view)
#         self.setLayout(self.layout)
#
#     def show_context_menu(self, pos):
#         # Get the global position of the context menu
#         global_pos = self.tree_view.viewport().mapToGlobal(pos)
#
#         selected_indexes = self.tree_view.selectedIndexes()
#         if len(selected_indexes) == 1:
#             item = self.model.itemFromIndex(selected_indexes[0])
#         else:
#             pass
#         unique_data_values = set()
#         selected_items = []
#         list_camera = []
#
#         # Iterate over selected items
#         for index in selected_indexes:
#             item = self.model.itemFromIndex(index)
#             if item is not None:
#                 # Get item data
#                 item_data = item.data(Qt.UserRole)
#                 if item_data is not None:
#                     unique_data_values.add(item_data)
#                     selected_items.append(item)
#
#         # Check if all selected items have the same item data or different item data
#         if len(unique_data_values) == 1:
#             item_data = unique_data_values.pop()
#             # Add actions based on the item data
#             if item_data == "camera_item":
#                 list_camera = selected_items
#             elif item_data == "group_camera":
#                 for group in selected_items:
#                     if group.rowCount() > 0:
#                         for camera_index in range(group.rowCount()):
#                             camera = group.child(camera_index)
#                             list_camera.append(camera)
#         else:
#             for item in selected_items:
#                 item_data = item.data(Qt.UserRole)
#                 if item_data not in ["camera_item", "group_camera"]:
#                     return
#
#             group_items = [item for item in selected_items if item.data(Qt.UserRole) == "group_camera"]
#             camera_items = [item for item in selected_items if item.data(Qt.UserRole) == "camera_item"]
#
#             for group in group_items:
#                 if group.rowCount() > 0:
#                     for camera_index in range(group.rowCount()):
#                         camera = group.child(camera_index)
#                         list_camera.append(camera)
#             for camera_item in camera_items:
#                 if camera_item not in list_camera:
#                     list_camera.append(camera_item)
#
#         # Create a context menu
#         menu = QMenu(self)
#         action_create_group = QAction(text=self.tr("Create group"), parent=menu)
#         action_delete = QAction(text=self.tr("Delete"), parent=menu)
#         menu.addAction(action_create_group)
#         menu.addAction(action_delete)
#         menu.exec(global_pos)
#
#     def action_for_root_item(self):
#         print("Action for root item")
#
#     def action_for_child_item(self):
#         print("Action for child item")
#
#     def common_action(self):
#         print("Common Action")
#
#     def check_selected_items(self):
#         selected_indexes = self.tree_view.selectedIndexes()
#         unique_data_values = set()
#
#         # Iterate over selected items
#         for index in selected_indexes:
#             item = self.model.itemFromIndex(index)
#             if item is not None:
#                 # Get item data
#                 item_data = item.data(Qt.UserRole)
#                 if item_data is not None:
#                     unique_data_values.add(item_data)
#
#         # Check if all selected items have the same item data or different item data
#         if len(unique_data_values) == 1:
#             print("All selected items have the same item data:", unique_data_values.pop())
#         else:
#             print("Selected items have different item data:", unique_data_values)
#
# class CustomWidget(QStackedWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAcceptDrops(True)
#         self.load_ui()
#
#     def load_ui(self):
#         self.setStyleSheet('background-color: lightblue')
#         self.addWidget(QLabel('HANHLT'))
#
#     def dropEvent(self, event):
#         mime_data = event.mimeData()
#         if mime_data.hasText():
#             text = mime_data.text()
#             obj_name = mime_data.objectName()
#             event.acceptProposedAction()
#         event.accept()
#
#     def dragEnterEvent(self, event):
#         event.accept()
#
#     def dragMoveEvent(self, event):
#         event.accept()
#
#     def dragLeaveEvent(self, event):
#         event.accept()
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.load_ui()
#
#     def load_ui(self):
#         self.central_widget = QWidget()
#         self.central_layout = QHBoxLayout()
#         self.treeview_widget = TreeViewEdit()
#         custom_widget = CustomWidget()
#         custom_widget.setFixedSize(100, 100)
#         self.button_custom = QPushButton("Press")
#         self.button_custom.clicked.connect(self.button_clicked)
#         self.central_layout.addWidget(self.treeview_widget)
#         self.central_layout.addWidget(custom_widget)
#         self.central_layout.addWidget(self.button_custom)
#         self.central_widget.setLayout(self.central_layout)
#         self.setCentralWidget(self.central_widget)
#
#     def find_item_by_name(self, item, name):
#         if item.text() == name:
#             return item
#
#         # Recursively search through children
#         for row in range(item.rowCount()):
#             child = item.child(row)
#             found_item = self.find_item_by_name(child, name)
#             if found_item:
#                 return found_item
#
#         return None
#
#     def change_item_color(self, item_name, color):
#         # Start searching from the root item
#         root_item = self.model.invisibleRootItem()
#         item = self.find_item_by_name(root_item, item_name)
#         if item:
#             # Apply custom stylesheet to change the item's color
#             item.setStyleSheet(f"color: {color};")
#     def button_clicked(self):
#         # Start searching from the root item
#         item_name = "Camera 3"
#         root_item = self.treeview_widget.model.invisibleRootItem()
#         item = self.find_item_by_name(root_item, item_name)
#         if item:
#             # Apply custom stylesheet to change the item's color
#             item.setBackground(QColor(255, 0, 0))
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())