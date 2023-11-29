import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QItemDelegate
from PySide6.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel


class ComboBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ComboBox with Icons Example')
        self.setGeometry(100, 100, 400, 200)

        # Create a QComboBox widget
        combo_box = QComboBox(self)
        combo_box.setGeometry(50, 50, 200, 30)

        # Create a QStandardItemModel
        model = QStandardItemModel()

        # Create items with icons and text
        item1 = QStandardItem(QIcon('/assets/sort-down.png'), "Option 1")
        item2 = QStandardItem(QIcon('/assets/sort-down.png'), "Option 2")
        item3 = QStandardItem(QIcon('/assets/sort-down.png'), "Option 3")

        # Add items to the model
        model.appendRow(item1)
        model.appendRow(item2)
        model.appendRow(item3)

        # Set the model for the ComboBox
        combo_box.setModel(model)

        # Create a delegate to display icons and text
        delegate = QItemDelegate(combo_box)
        combo_box.setItemDelegate(delegate)

        # Set a style sheet for the ComboBox
        combo_box.setStyleSheet(f'''
            QComboBox {{ 
                background-color: white; 
                border: 2px solid #B5122E; border-radius: 4px;
            }}
            QComboBox::drop-down {{
                 width: 30px; 
                 background-color: lightgray; 
             }}
            QComboBox::down-arrow {{ 
                image: url(/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/sort-up.png); 
            }}
        ''')

        # Connect the ComboBox to a function that handles item selection
        combo_box.activated.connect(self.comboBoxItemSelected)

    def comboBoxItemSelected(self, index):
        # Get the selected item text
        selected_item = self.sender().currentText()
        print(f"Selected Item: {selected_item}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ComboBoxExample()
    window.show()
    sys.exit(app.exec_())
