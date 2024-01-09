from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit, QWidget, QVBoxLayout, QPushButton, \
    QSizePolicy


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.splitter = QSplitter(self)

        # Create widgets for the main area and sidebar
        main_widget = QTextEdit("Main Area")
        sidebar_widget = QTextEdit("Sidebar")

        # Add widgets to the splitter
        self.splitter.addWidget(main_widget)

        # Create a button to toggle the sidebar visibility
        self.toggle_sidebar_button = QPushButton("Toggle Sidebar")
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)

        # Create a container widget for the button
        button_container_widget = QWidget(self.splitter)
        button_layout = QVBoxLayout(button_container_widget)
        button_layout.addWidget(self.toggle_sidebar_button)

        # Set the minimum size for the button container widget
        # Set the minimum size policy for the button container widget
        button_container_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add the container widget to the splitter
        self.splitter.addWidget(button_container_widget)

        # Set the sidebar widget as the second widget in the splitter
        self.splitter.addWidget(sidebar_widget)

        # Set stretch factors (main area takes 80%, button container takes 20%, sidebar takes 0%)
        self.splitter.setStretchFactor(0, 8)  # 80%
        self.splitter.setStretchFactor(1, 2)  # 20%
        self.splitter.setStretchFactor(2, 0)  # 0%

        # Set the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)

        main_container_widget = QWidget()
        main_container_widget.setLayout(layout)
        self.setCentralWidget(main_container_widget)

        self.setGeometry(100, 100, 800, 600)

    def toggle_sidebar(self):
        # Toggle the visibility of the sidebar
        is_visible = not self.splitter.widget(2).isVisible()
        self.splitter.widget(2).setVisible(is_visible)

        # Update the splitter handle
        self.splitter.handle(1).setEnabled(is_visible)


if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec()
