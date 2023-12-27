import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QDate

from src.grid_custom.grid_main import MainGrid


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Custom Grid')

        layout = QVBoxLayout()
        self.mainwindow = MainGrid()
        layout.addWidget(self.mainwindow)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())


'''13 item with 1 biggest item in center'''
# # Largest item in the center
# largest_item = QWidget()
# largest_item.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(largest_item, 1, 1, 3, 3)  # Span 3 rows and 3 columns, starting from row 1 and column 1
#
# # Twelve items surrounding the largest item
# for row in range(0, 5):
#     for col in range(0, 5):
#         if row == 1 and col == 1:
#             continue  # Skip the center item
#         item = QWidget()
#         item.setStyleSheet('background-color: lightblue;')
#         grid_layout.addWidget(item, row, col)

# '''8 item with 1 item biggest'''
# # Large item
# large_item = QWidget()
# large_item.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(large_item, 0, 0, 3, 3)  # Span 3 rows and 3 columns
#
# # Three items below the large item
# item_below_1 = QWidget()
# item_below_1.setStyleSheet('background-color: lightblue;')
# item_below_2 = QWidget()
# item_below_2.setStyleSheet('background-color: lightblue;')
# item_below_3 = QWidget()
# item_below_3.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(item_below_1, 3, 0)
# grid_layout.addWidget(item_below_2, 3, 1)
# grid_layout.addWidget(item_below_3, 3, 2)
#
# # Four items to the right of the large item
# item_right_1 = QWidget()
# item_right_1.setStyleSheet('background-color: lightblue;')
# item_right_2 = QWidget()
# item_right_2.setStyleSheet('background-color: lightblue;')
# item_right_3 = QWidget()
# item_right_3.setStyleSheet('background-color: lightblue;')
# item_right_4 = QWidget()
# item_right_4.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(item_right_1, 0, 3)
# grid_layout.addWidget(item_right_2, 1, 3)
# grid_layout.addWidget(item_right_3, 2, 3)
# grid_layout.addWidget(item_right_4, 3, 3)
#
# '''6 item with 1 item biggest'''
# # Large item
# large_item = QWidget()
# large_item.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(large_item, 0, 0, 2, 2)  # Span 2 rows and 2 columns
#
# # Two items below the large item
# item_below_1 = QWidget()
# item_below_1.setStyleSheet('background-color: lightblue;')
# item_below_2 = QWidget()
# item_below_2.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(item_below_1, 2, 0)
# grid_layout.addWidget(item_below_2, 2, 1)
#
# # Three items to the right of the large item
# item_right_1 = QWidget()
# item_right_1.setStyleSheet('background-color: lightblue;')
# item_right_2 = QWidget()
# item_right_2.setStyleSheet('background-color: lightblue;')
# item_right_3 = QWidget()
# item_right_3.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(item_right_1, 0, 2)
# grid_layout.addWidget(item_right_2, 1, 2)
# grid_layout.addWidget(item_right_3, 2, 2)

'''6 item with 2 item biggest'''
# # Two largest items in the center
# largest_item_1 = QWidget()
# largest_item_1.setStyleSheet('background-color: lightblue;')
# largest_item_2 = QWidget()
# largest_item_2.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(largest_item_1, 0, 0, 2, 2)  # Span 2 rows and 2 columns, starting from row 0 and column 0
# grid_layout.addWidget(largest_item_2, 0, 2, 2, 2)  # Span 2 rows and 2 columns, starting from row 0 and column 2
#
# # Four items below the two largest items
# item_below_1 = QWidget()
# item_below_1.setStyleSheet('background-color: lightblue;')
# item_below_2 = QWidget()
# item_below_2.setStyleSheet('background-color: lightblue;')
# item_below_3 = QWidget()
# item_below_3.setStyleSheet('background-color: lightblue;')
# item_below_4 = QWidget()
# item_below_4.setStyleSheet('background-color: lightblue;')
# grid_layout.addWidget(item_below_1, 2, 0)  # Starting from row 2 and column 0
# grid_layout.addWidget(item_below_2, 2, 1)  # Starting from row 2 and column 1
# grid_layout.addWidget(item_below_3, 2, 2)  # Starting from row 2 and column 2
# grid_layout.addWidget(item_below_4, 2, 3)  # Starting from row 2 and column 3

'''7 item with 4 bigger item'''
# # Four biggest items in a 2x2 grid
# biggest_item_1 = QWidget()
# biggest_item_1.setStyleSheet('background-color: lightblue;')
# biggest_item_2 = QWidget()
# biggest_item_2.setStyleSheet('background-color: lightblue;')
# biggest_item_3 = QWidget()
# biggest_item_3.setStyleSheet('background-color: lightblue;')
# biggest_item_4 = QWidget()
# biggest_item_4.setStyleSheet('background-color: lightblue;')
#
# grid_layout.addWidget(biggest_item_1, 0, 0)  # Row 0, Column 0
# grid_layout.addWidget(biggest_item_2, 0, 1)  # Row 0, Column 1
# grid_layout.addWidget(biggest_item_3, 1, 0)  # Row 1, Column 0
# grid_layout.addWidget(biggest_item_4, 1, 1)  # Row 1, Column 1
#
# # Three items to the right of the biggest items
# right_item_1 = QWidget()
# right_item_1.setStyleSheet('background-color: lightblue;')
# right_item_2 = QWidget()
# right_item_2.setStyleSheet('background-color: lightblue;')
# right_item_3 = QWidget()
# right_item_3.setStyleSheet('background-color: lightblue;')
#
# grid_layout.addWidget(right_item_1, 0, 2)  # Row 0, Column 2
# grid_layout.addWidget(right_item_2, 1, 2)  # Row 1, Column 2
# grid_layout.addWidget(right_item_3, 2, 2)  # Row 2, Column 2
