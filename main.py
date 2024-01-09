from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit, QWidget, QVBoxLayout, QPushButton


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.splitter = QSplitter(self)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: #99aabb; }")
        self.splitter.setHandleWidth(1)

        # Create two widgets
        self.widget1 = QTextEdit("Widget 1")
        widget2 = QTextEdit("Widget 2")
        widget3 = QTextEdit("Widget 3")

        # Calculate the maximum width for widget1 (30% of the total width)
        total_width = self.width()
        max_width_widget1 = int(total_width * 0.4)
        min_width_widget1 = int(total_width * 0.2)

        # Set maximum width for widget1
        self.widget1.setMaximumWidth(max_width_widget1)
        self.widget1.setMinimumWidth(min_width_widget1)

        widget3.setMaximumWidth(max_width_widget1)
        widget3.setMinimumWidth(min_width_widget1)

        # Create a button to toggle the sidebar visibility
        self.toggle_sidebar_button = QPushButton("T")
        self.toggle_sidebar_button.setFixedWidth(10)
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)

        # Create a container widget for the button
        button_container_widget = QWidget(self.splitter)
        button_container_widget.setFixedWidth(10)
        button_container_widget.setMinimumWidth(10)
        button_layout = QVBoxLayout(button_container_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(self.toggle_sidebar_button)

        # Create a button to toggle the sidebar visibility
        self.toggle_eventbar_button = QPushButton("T")
        self.toggle_eventbar_button.setFixedWidth(10)
        self.toggle_eventbar_button.clicked.connect(self.toggle_event_bar)

        # Create a container widget for the button
        widget_button_event_bar = QWidget(self.splitter)
        widget_button_event_bar.setFixedWidth(10)
        widget_button_event_bar.setMinimumWidth(10)
        button_event_bar_layout = QVBoxLayout(widget_button_event_bar)
        button_event_bar_layout.setContentsMargins(0, 0, 0, 0)
        button_event_bar_layout.addWidget(self.toggle_eventbar_button)

        # Add widgets to the splitter
        self.splitter.addWidget(self.widget1)
        self.splitter.addWidget(button_container_widget)
        self.splitter.addWidget(widget2)
        self.splitter.addWidget(widget_button_event_bar)
        self.splitter.addWidget(widget3)

        self.splitter.setStretchFactor(0, 2)  # 20%
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 5)  # 80%
        self.splitter.setStretchFactor(3, 1)  # 80%
        self.splitter.setStretchFactor(4, 2)  # 80%

        # Set the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.showMaximized()

    def toggle_sidebar(self):
        # Toggle the visibility of the sidebar
        is_visible = not self.splitter.widget(0).isVisible()
        self.splitter.widget(0).setVisible(is_visible)

        # Update the splitter handle
        self.splitter.handle(0).setEnabled(is_visible)

    def toggle_event_bar(self):
        # Toggle the visibility of the sidebar
        is_visible = not self.splitter.widget(4).isVisible()
        self.splitter.widget(4).setVisible(is_visible)

        # Update the splitter handle
        self.splitter.handle(3).setEnabled(is_visible)


if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec()
