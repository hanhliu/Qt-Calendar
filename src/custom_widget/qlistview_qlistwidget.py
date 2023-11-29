import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListView, QPushButton


class NotificationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notification UI")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.notification_list = QListView()
        self.notification_model = QStandardItemModel()
        self.notification_list.setModel(self.notification_model)
        self.button = QPushButton("Button")
        older_items = ["Notification 3", "Notification 4", "Notification 5"]
        self.button.clicked.connect(self.add_to_list)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.notification_list)

        self.today_label = None  # Store a reference to the "Today" label item
        self.today_index = None

        self.populate_notifications()

    def populate_notifications(self):
        # Add "Today" and "Older" labels
        self.today_label = QStandardItem("Today")
        self.today_label.setFlags(self.today_label.flags() & ~Qt.ItemIsSelectable)  # Make label unselectable
        self.older_label = QStandardItem("Older")
        self.older_label.setFlags(self.older_label.flags() & ~Qt.ItemIsSelectable)

        # Add sample notifications
        today_items = ["Notification 1", "Notification 2"]
        older_items = ["Notification 3", "Notification 4", "Notification 5"]

        # Add labels to the model
        self.today_index = self.notification_model.rowCount()

        # Add labels and items to the model
        self.notification_model.appendRow(self.today_label)
        self.add_items_to_list(today_items)
        self.notification_model.appendRow(self.older_label)
        self.add_items_to_list(older_items)

    def add_items_to_list(self, items):
        for item_text in items:
            item = QStandardItem(item_text)
            self.notification_model.appendRow(item)

    def add_to_list(self):
        print("HanhLT: chay vao day")
        today_items = ["Notification 9", "Notification 000"]
        if self.today_index is not None:
            # Add items below the "Today" label
            for item_text in today_items:
                item = QStandardItem(item_text)
                self.notification_model.insertRow(self.today_index + 1, item)
                self.today_index += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = NotificationApp()
    main_window.show()
    sys.exit(app.exec_())


