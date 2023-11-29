import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView
from PyQt5.QtCore import Qt

def item_clicked(index):
    item = model.itemFromIndex(index)
    if item is not None:
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Clickable and Disableable List')

my_list = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10']

model = QStandardItemModel()
for item_text in my_list:
    item = QStandardItem(item_text)
    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # Allow clicking
    item.setCheckState(Qt.Unchecked)  # Initially, all items are enabled
    model.appendRow(item)

list_view = QListView()
list_view.setModel(model)
list_view.clicked.connect(item_clicked)

window.setCentralWidget(list_view)
window.show()

sys.exit(app.exec_())
