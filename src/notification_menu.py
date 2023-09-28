import sys
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QAction, QStandardItem, QStandardItemModel, QPainter
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMenu, QMainWindow, \
    QWidgetAction, QListView, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QFrame, QSizePolicy, QScrollArea


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
        menu = QMenu(self)
        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        custom_widgetttt = QWidget(self)
        # custom_widgetttt.setFixedHeight(700)
        custom_widget = QWidget()
        custom_widget.setFixedHeight(700)
        layout_notification = QVBoxLayout()
        layout_notification.setAlignment(Qt.AlignmentFlag.AlignTop)
        '''*********'''
        self.layout_button = QHBoxLayout()
        self.button_all = QPushButton("All")
        self.button_all.clicked.connect(self.add_items_to_list)
        self.button_unread = QPushButton("Unread")
        self.layout_button.addWidget(self.button_all)
        self.layout_button.addWidget(self.button_unread)
        self.warning_list_view = WarningListView()
        self.warning_list_view1 = WarningListView()

        self.today_label = QLabel("Today")
        self.yesterday_label = QLabel("Yesterday")

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.HLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)
        self.divider2 = QFrame()
        self.divider2.setFrameShape(QFrame.Shape.HLine)
        self.divider2.setFrameShadow(QFrame.Shadow.Sunken)


        layout_notification.addWidget(self.today_label)
        layout_notification.addWidget(self.divider)
        layout_notification.addWidget(self.warning_list_view)
        # layout_notification.addWidget(self.yesterday_label)
        # layout_notification.addWidget(self.divider2)
        # layout_notification.addWidget(self.warning_list_view1)
        custom_widget.setLayout(layout_notification)
        scroll_area.setWidget(custom_widget)
        scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.test_layout = QVBoxLayout()
        self.test_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.test_layout.addLayout(self.layout_button)
        self.test_layout.addWidget(scroll_area)

        custom_widgetttt.setLayout(self.test_layout)
        custom_action = QWidgetAction(self)
        custom_action.setDefaultWidget(custom_widgetttt)
        # Add actions to the menu
        menu.addAction(custom_action)
        menu.exec(self.show_menu_button.mapToGlobal(self.show_menu_button.rect().bottomRight()))

    def add_items_to_list(self):
        print("HanhLT: add item to list")
        # Add one item to the list view
        item_widget = ItemNotification()
        self.warning_list_view.add_item(item_widget)
class WarningListView(QListView):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(320)
        self.setup_ui()

    def setup_ui(self):
        # Hide vertical scroll bar
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Hide horizontal scroll bar
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.list_view_model = QStandardItemModel()
        self.setModel(self.list_view_model)

        item_widget = ItemNotification()
        self.list_view_model.appendRow(item_widget)
        self.setIndexWidget(self.list_view_model.indexFromItem(item_widget), item_widget.main_widget)

    def add_item(self, item_widget):
        # Add a new item to the model and update the height
        self.list_view_model.appendRow(item_widget)
        self.setIndexWidget(self.list_view_model.indexFromItem(item_widget), item_widget.main_widget)
        self.setFixedHeight(self.sizeHintForRow(0) * self.list_view_model.rowCount())

    def sizeHintForRow(self, row):
        # Calculate the size hint for each row (item)
        index = self.list_view_model.index(row, 0)
        item_widget = self.indexWidget(index)
        if item_widget:
            return item_widget.sizeHint().height()
        return super().sizeHintForRow(row)
    def wheelEvent(self, event):
        # Disable vertical scrolling by ignoring the wheel event
        event.ignore()

    def scrollContentsBy(self, dx, dy):
        # Disable horizontal scrolling by preventing content scrolling
        pass

class ItemNotification(QStandardItem):
    def __init__(self):
        super().__init__()
        self.load_ui()
    def load_ui(self):
        self.main_widget = QWidget()
        self.main_widget.setFixedWidth(300)
        self.main_layout = QHBoxLayout(self.main_widget)

        # self.widget_state_read = QWidget()
        self.layout_state_read = QVBoxLayout()
        svg_state_read = QSvgWidget()
        svg_state_read.load("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/state_read.svg")
        svg_state_read.setFixedSize(10, 10)
        self.layout_state_read.addWidget(svg_state_read)

        self.layout_image_event = QVBoxLayout()
        self.layout_image_event.setContentsMargins(0, 0, 0, 0)
        svg_image_event = QSvgWidget()
        svg_image_event.load("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/state_read.svg")
        svg_image_event.setFixedSize(60, 60)
        self.label_time = QLabel("10:10:10")
        self.layout_image_event.addWidget(svg_image_event)
        self.layout_image_event.addWidget(self.label_time)

        self.layout_content_event = QVBoxLayout()
        self.layout_content_event.setContentsMargins(0, 0, 0, 0)
        self.layout_title = QHBoxLayout()
        self.layout_title.setContentsMargins(0, 0, 0, 0)
        self.object_name = QLabel("Alex Hoang")
        self.label_blacklist = QPushButton("Blacklist")
        self.layout_title.addWidget(self.object_name)
        self.layout_title.addWidget(self.label_blacklist)
        self.label_warning_context = QLabel("Warning Context: Frequency")
        self.label_method = QLabel("Appear 5 times within 1 hour")
        self.label_method.setStyleSheet("background-color: yellow; color: black")
        self.layout_content_event.addLayout(self.layout_title)
        self.layout_content_event.addWidget(self.label_warning_context)
        self.layout_content_event.addWidget(self.label_method)

        self.main_layout.addLayout(self.layout_state_read)
        self.main_layout.addLayout(self.layout_image_event)
        self.main_layout.addLayout(self.layout_content_event)

        self.setSizeHint(self.main_widget.sizeHint())
        self.setData(self.main_widget, Qt.UserRole)

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
