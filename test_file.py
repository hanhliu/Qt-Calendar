from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QApplication, QWidget, QTabBar, QVBoxLayout, QLabel, QPushButton, QTabWidget, QMainWindow, \
    QHBoxLayout, QStackedLayout, QStackedWidget


class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initial_pos = None
        self.installEventFilter(self)
        self.parent = parent
        self.setStyleSheet(
            f"""
            QTabBar::pane#tab_bar_device_screen {{
                background: transparent;
                border: none;
                font-size: 12px;
            }}
            QTabBar::tab#tab_bar_custom {{
                background-color: lightblue;
                color: black;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: None;
            }}
            QTabBar::tab:selected#tab_bar_custom {{
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                background-color: blue;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }}
            
            """
        )

    def _move(self):
        window_move = self.parent.window().windowHandle()
        window_move.startSystemMove()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            self._move()
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def eventFilter(self, watched, event):
        if watched == self:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                mouse_button = event.button()
                if mouse_button == Qt.LeftButton:
                    # Toggle between full screen and normal mode
                    if self.parent.window().isMaximized():
                        self.parent.window().showNormal()
                    else:
                        self.parent.window().showMaximized()
        return super().eventFilter(watched, event)


class CustomTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setTabBar(CustomTabBar(parent=self.parent))

    def tabBarClicked(self, index):
        # Custom actions when a tab is clicked
        print(f"Tab {index} clicked")
        super().tabBarClicked(index)


class TabBarExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('QTabBar Example')
        self.setGeometry(100, 100, 400, 300)

        # Create a QTabWidget
        self.tab_widget = QTabWidget()

        # Create a QStackedLayout to manage content widgets
        self.stacked_layout = QStackedWidget()

        # Create a QVBoxLayout for the entire widget
        main_layout = QVBoxLayout()

        # Create a QTabBar
        self.tab_bar = self.tab_widget.tabBar()
        self.tab_bar.setObjectName("tab_bar_custom")
        self.tab_bar.setStyleSheet(
            """
            QTabBar::tab#tab_bar_custom {{
                background-color: lightblue;
                padding: 8px 12px;
                font-weight: None;
            }}
            QTabBar::tab:selected#tab_bar_custom {{
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                background-color: lightblue;
                font-weight: bold;
            }}
            QTabBar::close-button#tab_bar_custom {{
                subcontrol-position: right;
            }}
            QTabBar::close-button:hover#tab_bar_custom {{
                subcontrol-position: right;
                border-radius: 2px;
                font-weight: None;
            }}
            """
        )

        # set tab bar can be closed
        self.tab_widget.setTabsClosable(True)

        # Connect the tabChanged signal to a custom slot
        self.tab_bar.currentChanged.connect(self.tab_changed)

        # Connect the tabCloseRequested signal to a custom slot
        self.tab_bar.tabCloseRequested.connect(self.close_tab)

        # Add the QTabWidget to the main layout
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.stacked_layout)

        # Create a QPushButton for adding new tabs
        self.add_tab_button = QPushButton("+ Add Tab")
        self.add_tab_button.clicked.connect(self.add_tab)

        # Add the QPushButton to the main layout
        main_layout.addWidget(self.add_tab_button)

        # Set the main layout for the widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def tab_changed(self, index):
        # Show the corresponding content widget when a tab is selected
        self.stacked_layout.setCurrentIndex(index)

    def add_tab(self):
        # Add a new tab to the QTabWidget and create a corresponding content widget
        new_tab_index = self.tab_bar.addTab(f"Tab {self.tab_bar.count() + 1}")

        # Create a QLabel as the content for the new tab
        new_content_widget = QLabel(f"Content of Tab {self.tab_bar.count()}")
        new_content_widget.hide()

        # Store the content widget in the QStackedLayout
        self.stacked_layout.addWidget(new_content_widget)

        # Show the corresponding content widget
        self.tab_changed(new_tab_index)

    def close_tab(self, index):
        # Remove the tab and its corresponding content widget
        self.tab_bar.removeTab(index)
        self.stacked_layout.removeWidget(self.stacked_layout.widget(index))
        self.stacked_layout.setCurrentIndex(self.tab_bar.currentIndex())


if __name__ == '__main__':
    app = QApplication([])
    window = TabBarExample()
    window.show()
    app.exec()

# def __init__(self):
#        super().__init__()
#
#        self.setWindowTitle('QTabBar Example')
#        self.setGeometry(100, 100, 400, 300)
#
#        # Create a vertical layout for the entire widget
#        main_layout = QVBoxLayout(self)
#
#        # Create a QTabBar
#        self.tab_bar = QTabBar(self)
#
#        # Add tabs to the QTabBar
#        self.tab_bar.addTab("Tab 1")
#        self.tab_bar.addTab("Tab 2")
#        self.tab_bar.addTab("Tab 3")
#
#        # Connect the tabChanged signal to a custom slot
#        self.tab_bar.currentChanged.connect(self.tab_changed)
#
#        # Create a dictionary to store content widgets for each tab
#        self.tab_contents = {}
#
#        # Create a QPushButton for adding new tabs
#        self.add_tab_button = QPushButton("+ Add Tab")
#        self.add_tab_button.clicked.connect(self.add_tab)
#
#        # Add the QTabBar, button, and an initial content widget to the main layout
#        main_layout.addWidget(self.tab_bar)
#        main_layout.addWidget(self.add_tab_button)
#
#        # Set the main layout for the widget
#        self.setLayout(main_layout)
#
#    def tab_changed(self, index):
#        # Show the corresponding content widget when a tab is selected
#        for tab_index, content_widget in self.tab_contents.items():
#            content_widget.setVisible(tab_index == index)
#
#    def add_tab(self):
#        # Add a new tab to the QTabBar and create a corresponding content widget
#        new_tab_index = self.tab_bar.addTab(f"Tab {self.tab_bar.count() + 1}")
#
#        # Create a QLabel as the content for the new tab
#        new_content_widget = QLabel(f"Content of Tab {self.tab_bar.count()}")
#        new_content_widget.hide()
#
#        # Store the content widget in the dictionary
#        self.tab_contents[new_tab_index] = new_content_widget
#
#        # Add the content widget to the main layout
#        self.layout().addWidget(new_content_widget)
#
#        # Show the corresponding content widget
#        self.tab_changed(new_tab_index)
