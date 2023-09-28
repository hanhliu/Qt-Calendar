import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QLabel, QPushButton, QWidget, \
    QWidgetAction, QGridLayout


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Custom Widget in QMenu Example")
    central_widget = QWidget(window)
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    label = QLabel("Right-click to open the menu with a custom widget.")
    layout.addWidget(label)

    button = QPushButton("Dummy Button")
    layout.addWidget(button)

    button.setContextMenuPolicy(Qt.CustomContextMenu)
    button.clicked.connect(lambda pos: show_menu_with_custom_widget(button, pos, 3))

    window.show()
    sys.exit(app.exec())

def show_menu_with_custom_widget(parent, pos, item_count):
    menu = QMenu(parent)

    # Create a custom widget
    custom_widget = QWidget(menu)
    grid_layout = QGridLayout()
    grid_layout.setContentsMargins(2, 0, 2, 0)
    index = 1
    for row in range(item_count):
        for col in range(item_count):
            label = QPushButton(f"{index}")
            label.setStyleSheet(
                """
                QPushButton {
                    background-color: #4CAF50; /* Green background */
                    color: white; /* White text */
                    border: 2px solid #008CBA; /* Dark blue border */
                    border-radius: 5px; /* Rounded corners */
                    padding: 10px 20px; /* Padding inside the button */
                    font-size: 16px; /* Font size */
                }

                QPushButton:hover {
                    background-color: #45a049; /* Darker green on hover */
                }

                QPushButton:pressed {
                    background-color: #0078a3; /* Dark blue on press */
                }
                """
            )
            grid_layout.addWidget(label, row, col)
            grid_layout.setSpacing(2)
            index += 1

    custom_widget.setLayout(grid_layout)

    # Create a QWidgetAction to add the custom widget to the QMenu
    custom_action = QWidgetAction(menu)
    custom_action.setDefaultWidget(custom_widget)
    menu.addAction(custom_action)
    pos = QPoint(500, 500)

    menu.exec(pos)

if __name__ == "__main__":
    main()
