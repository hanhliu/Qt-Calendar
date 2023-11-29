import sys

import PySide6
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QAction, QStandardItem, QStandardItemModel, QPainter, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMenu, QMainWindow, \
    QWidgetAction, QListView, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QFrame, QSizePolicy, QScrollArea, \
    QDialog


class CustomMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.show_menu_button = QPushButton("Show menu", self)
        self.show_menu_button.clicked.connect(self.show_menu)
        self.layout.addWidget(self.show_menu_button)
        self.setLayout(self.layout)

    def show_menu(self):
        self.main_menu = QMenu(self)
        custom_widget = QWidget()
        custom_widget.setStyleSheet("background-color: white; border-radius: 4px;")
        custom_widget.setFixedHeight(700)
        layout_notification = QVBoxLayout()
        layout_notification.setAlignment(Qt.AlignmentFlag.AlignTop)
        '''*********'''
        self.layout_button = QHBoxLayout()
        self.button_all = ButtonFilterNotification(title=self.tr("All"), type_button="All")
        self.button_all.click = self.add_items_today
        self.button_unread = ButtonFilterNotification(title=self.tr("Unread"), type_button="Unread")
        self.button_unread.click = self.add_items_older
        self.layout_button.addWidget(self.button_all)
        self.layout_button.addWidget(self.button_unread)
        self.warning_list_view = WarningListView()

        layout_notification.addLayout(self.layout_button)
        layout_notification.addWidget(self.warning_list_view)
        custom_widget.setLayout(layout_notification)

        custom_action = QWidgetAction(self)
        custom_action.setDefaultWidget(custom_widget)
        # Add actions to the menu
        self.main_menu.addAction(custom_action)
        self.main_menu.setAttribute(Qt.WA_TranslucentBackground)
        self.main_menu.setWindowFlag(Qt.FramelessWindowHint)
        self.main_menu.setStyleSheet("""
             QMenu {
                font-size: 14px;
                background-color: white;
                border-radius: 8px;
                margin-top: 0px;
                margin-bottom: 0px;
                }
        """)
        self.main_menu.exec(self.show_menu_button.mapToGlobal(self.show_menu_button.rect().bottomRight()))

    def add_items_today(self, event):
        self.warning_list_view.add_to_list_today()

    def add_items_older(self, event):
        self.warning_list_view.add_to_list_older()


class WarningListView(QListView):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(320)
        self.list_alert_today = []
        self.list_alert_older = []
        self.today_label = None  # Store a reference to the "Today" label item
        self.today_index = None
        self.older_label = None
        self.older_index = None
        self.setup_ui()

    def setup_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_view_model = QStandardItemModel()
        self.setModel(self.list_view_model)
        self.populate_notifications()
        self.set_style_sheet()

    def set_style_sheet(self):
        self.setStyleSheet("QListView { background-color: transparent; }")

    def populate_notifications(self):
        # Add "Today" and "Older" labels
        self.today_label = ItemDateName("Today")
        self.today_label.setFlags(self.today_label.flags() & ~Qt.ItemIsSelectable)  # Make label unselectable
        self.older_label = ItemDateName("Yesterday")
        self.older_label.setFlags(self.older_label.flags() & ~Qt.ItemIsSelectable)

        # Create and append ItemNotification instances to the list
        for i in range(5):  # Create 5 items as an example; you can adjust the range as needed
            item = ItemNotification()
            self.list_alert_today.append(item)

        self.today_index = self.list_view_model.rowCount()
        self.label_no_warning_today = QStandardItem("No warnings")
        self.label_no_warning_today.setFlags(self.label_no_warning_today.flags() & ~Qt.ItemIsSelectable)  # Make label unselectable
        self.label_no_warning = QStandardItem("No warnings")
        self.label_no_warning.setFlags(self.label_no_warning.flags() & ~Qt.ItemIsSelectable)  # Make label unselectable

        # Add labels and items to the model
        self.list_view_model.appendRow(self.today_label)
        self.setIndexWidget(self.list_view_model.indexFromItem(self.today_label), self.today_label.main_widget)
        if self.list_alert_today:
            self.add_items_to_list(self.list_alert_today)
        else:
            self.list_view_model.appendRow(self.label_no_warning_today)
        self.list_view_model.appendRow(self.older_label)
        self.setIndexWidget(self.list_view_model.indexFromItem(self.older_label), self.older_label.main_widget)
        if self.list_alert_older:
            self.add_items_to_list(self.list_alert_older)
        else:
            self.list_view_model.appendRow(self.label_no_warning)

    def add_items_to_list(self, list_items):
        for item_text in list_items:
            self.list_view_model.appendRow(item_text)
            self.setIndexWidget(self.list_view_model.indexFromItem(item_text), item_text.main_widget)

    def add_to_list_today(self):
        if self.today_index is not None:
            # Add items below the "Today" label
            item_widget = ItemNotification()
            self.list_view_model.insertRow(self.today_index + 1, item_widget)
            self.setIndexWidget(self.list_view_model.indexFromItem(item_widget), item_widget.main_widget)
            self.today_index += 1
        self.label_no_warning_today.setData("", Qt.DisplayRole)

    def add_to_list_older(self):
        self.older_index = self.list_view_model.indexFromItem(self.older_label).row()
        if self.older_index is not None:
            # Add items below the "Older" label
            item = ItemNotification()
            self.list_view_model.insertRow(self.older_index + 1, item)
            self.setIndexWidget(self.list_view_model.indexFromItem(item), item.main_widget)
            self.older_index += 1

        self.label_no_warning.setData("", Qt.DisplayRole)

class ItemDateName(QStandardItem):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.load_ui()

    def load_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(1)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet('''
            QLabel { 
                color: #B5122E; 
                font-size: 16px; 
            }''')

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.HLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)
        self.divider.setFixedHeight(2)
        self.divider.setStyleSheet("background-color: black;")
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.divider)

        self.setSizeHint(self.main_widget.sizeHint())
        self.setData(self.main_widget, Qt.UserRole)


class ItemNotification(QStandardItem):
    def __init__(self,):
        super().__init__()
        self.load_ui()

    def load_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setSpacing(2)
        # self.widget_state_read = QWidget()
        self.layout_state_read = QVBoxLayout()
        svg_state_read = QSvgWidget()
        svg_state_read.load("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/state_read.svg")
        svg_state_read.setFixedSize(10, 10)
        self.layout_state_read.addWidget(svg_state_read)

        self.layout_image_event = QVBoxLayout()
        self.layout_image_event.setContentsMargins(0, 0, 0, 0)
        self.layout_image_event.setSpacing(0)
        self.layout_image_event.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Load an image using QPixmap
        self.image_label = QLabel()
        pixmap = QPixmap("/assets/image_event.png")  # Replace with the actual image file path
        self.image_label.setPixmap(pixmap)
        self.label_time = QLabel("10:10:10")
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_image_event.addWidget(self.image_label)
        self.layout_image_event.addWidget(self.label_time)

        self.layout_content_event = QVBoxLayout()
        self.layout_content_event.setContentsMargins(0, 0, 0, 0)
        self.layout_content_event.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_title = QHBoxLayout()
        self.layout_title.setContentsMargins(0, 0, 0, 0)
        self.layout_title.setSpacing(5)
        self.object_name = QLabel("Alex Hoang")
        self.object_name.setStyleSheet("font-weight: bold")
        self.label_blacklist = QLabel("Blacklist")
        self.label_blacklist.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_blacklist.setFixedHeight(28)
        self.label_blacklist.setStyleSheet("color: white; background-color: red; border-radius: 4px")
        self.layout_title.addWidget(self.object_name)
        self.layout_title.addWidget(self.label_blacklist)
        self.label_warning_context = QLabel("Warning Context: Frequency")
        self.label_method = QLabel("Appear 5 times within 1 hour")
        self.layout_content_event.addLayout(self.layout_title)
        self.layout_content_event.addWidget(self.label_warning_context)
        self.layout_content_event.addWidget(self.label_method)

        self.main_layout.addLayout(self.layout_state_read)
        self.main_layout.addLayout(self.layout_image_event)
        self.main_layout.addLayout(self.layout_content_event)

        self.setSizeHint(self.main_widget.sizeHint())
        self.setData(self.main_widget, Qt.UserRole)

        # create listen click to item
        self.main_widget.mousePressEvent = self.on_item_click

    def on_item_click(self, event):
        if event.button() == Qt.LeftButton:
            print("HanhLT: click to item")
            # self.dialog = QDialog()
            # self.dialog.setEnabled(False)
            # self.dialog.repaint()
            # self.dialog.setEnabled(True)
            # self.dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
            # self.dialog.exec()

class ButtonFilterNotification(QPushButton):
    def __init__(self, title=None, type_button=None, click=None):
        super().__init__()
        self.title = title
        self.click = click
        self.type_button = type_button
        self.load_ui()

    def load_ui(self):
        self.setFixedHeight(30)
        self.setText(self.title)
        if self.type_button == "All":
            self.setStyleSheet('''
                QPushButton { 
                    background-color: #B5122E; 
                    color: white; 
                    border-radius: 4px; 
                    border: 1px solid #B5122E
                }
            ''')
        else:
            self.setStyleSheet('''
                QPushButton { 
                    background-color: white; 
                    color: #B5122E; 
                    border-radius: 4px; 
                    border: 1px solid #B5122E
                }
            ''')

    def mousePressEvent(self, e: PySide6.QtGui.QMouseEvent):
        print("HanhLT: chay vao day")
        if self.click is not None:
            self.click(e)


class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.custom_menu = CustomMenu()
        self.layout.addWidget(self.custom_menu)
        self.central_widget.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = VideoPlayerApp()
    main_window.show()
    sys.exit(app.exec())
