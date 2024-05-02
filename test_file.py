from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtWidgets import QApplication, QWidget, QTabBar, QVBoxLayout, QLabel, QPushButton, QTabWidget, QMainWindow, \
    QHBoxLayout, QStackedLayout, QStackedWidget, QSizePolicy, QLineEdit, QTextEdit

from src.custom_title_new.widget.actionable_title_bar import ActionableTitleBar
from src.custom_title_new.widget.button_title_bar import ButtonTitleBar


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
        # Create a set to store existing tab names
        self.existing_tab_names = set()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle('Frameless Window with Rounded Corners')
        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        self.setWindowTitle('QTabBar Example')
        self.setGeometry(100, 100, 400, 300)

        self.create_center_layout()
        # self.create_left_side_layout()
        # self.create_right_size_layout()
        # self.create_layout_button_system()

        # Create a QStackedLayout to manage content widgets
        self.stacked_widget = QStackedWidget()

        # Create a QVBoxLayout for the entire widget
        main_layout = QVBoxLayout()

        initial_tab_name = "Tab 1"
        self.add_new_tab(self.tab_bar, self.stacked_widget, initial_tab_name)
        self.add_new_tab(self.tab_bar, self.stacked_widget, "Tab 2")
        self.tab_contents = {initial_tab_name}


        # Add the QTabWidget to the main layout
        main_layout.addWidget(self.widget_tab_title)
        main_layout.addWidget(self.stacked_widget)

        # Create a QPushButton for adding new tabs
        self.add_tab_button = QPushButton("+ Add Tab")
        self.add_tab_button.clicked.connect(lambda: self.add_new_tab(self.tab_bar, self.stacked_widget))

        # Add the QPushButton to the main layout
        main_layout.addWidget(self.add_tab_button)

        # Set the main layout for the widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_left_side_layout(self):
        self.widget_left = QWidget()
        self.left_layout = QVBoxLayout()
        self.search_bar = QLineEdit("Search")
        self.treeview = QTextEdit("This is Tree View")
        self.left_layout.addWidget(self.search_bar, 10)
        self.left_layout.addWidget(self.treeview, 90)
        self.widget_left.setLayout(self.left_layout)

    def create_right_size_layout(self):
        self.widget_right = QWidget()
        self.right_layout = QVBoxLayout()
        self.eventbar = QTextEdit("This is Event Bar")
        self.right_layout.addWidget(self.eventbar)
        self.widget_right.setLayout(self.right_layout)

    def create_center_layout(self):
        # Create a QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setMaximumHeight(self.tab_widget.tabBar().height())
        self.tab_widget.tabBar().setStyleSheet("""
             QTabBar {
                alignment: left;
            }

            QTabBar::tab {
                background-color: lightblue;
                padding: 8px 12px;
                font-weight: None;
            }

            QTabBar::tab:selected {
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                background-color: lightblue;
                font-weight: bold;
            }

            QTabBar::close-button {
                subcontrol-position: right;
            }

            QTabBar::close-button:hover {
                subcontrol-position: right;
                border-radius: 2px;
                font-weight: None;
            }""")
        self.tab_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.tabBar().setExpanding(False)
        self.tab_widget.setMovable(False)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setCornerWidget(QLabel("Corner"))
        self.tab_widget.setStyleSheet("""
            QTabWidget::tab-bar {
                left: 0; 
            }
            QTabWidget::pane {
                background: transparent;
                border: none;
            }
        """)
        self.tab_bar = self.tab_widget.tabBar()
        self.tab_bar.currentChanged.connect(self.tab_changed)
        # Connect the tabCloseRequested signal to a custom slot
        self.tab_bar.tabCloseRequested.connect(self.close_tab)

        self.widget_tab_title = ActionableTitleBar(self)
        self.widget_tab_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout_tab_title = QVBoxLayout()
        layout_tab_title.setContentsMargins(0, 0, 0, 0)
        layout_tab_title.addWidget(self.tab_widget)
        self.widget_tab_title.setLayout(layout_tab_title)

    def create_layout_button_system(self):
        self.layout_button_system = QHBoxLayout()
        self.min_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/minimize_window.svg")

        # Max button
        self.max_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/maximize_window.svg")

        # Close button
        self.close_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/close.svg")
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/normal_window.svg")
        self.normal_button.setVisible(False)

        # Settings button
        self.settings_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/settings.svg")
        #
        # # Add buttons
        buttons = [
            self.settings_button,
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        self.layout_button_system.setAlignment(Qt.AlignmentFlag.AlignRight)
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(28, 28))
            self.layout_button_system.addWidget(button)


    def add_new_tab(self, tab_bar, stack_widget, tab_name=None):
        if tab_name is not None:
            new_tab_name = tab_name
        else:
            # Create a unique tab name
            new_tab_name = self.generate_unique_tab_name()

        # Add a new tab to the QTabWidget and create a corresponding content widget
        new_tab_index = tab_bar.addTab(new_tab_name)

        # Create a QLabel as the content for the new tab
        new_content_widget = QLabel(f"Content of {new_tab_name}")
        new_content_widget.hide()

        # Store the content widget in the QStackedLayout
        stack_widget.addWidget(new_content_widget)

        # Show the corresponding content widget
        stack_widget.setCurrentIndex(new_tab_index)

        # Activate the newly added tab
        tab_bar.setCurrentIndex(new_tab_index)

    def tab_changed(self, index):
        # Show the corresponding content widget when a tab is selected
        self.stacked_widget.setCurrentIndex(index)

    def add_tab(self):
        # Create a unique tab name
        new_tab_name = self.generate_unique_tab_name()

        # Add a new tab to the QTabWidget and create a corresponding content widget
        new_tab_index = self.tab_bar.addTab(new_tab_name)

        # Create a QLabel as the content for the new tab
        new_content_widget = QLabel(f"Content of {new_tab_name}")
        new_content_widget.hide()

        # Store the content widget in the QStackedLayout
        self.stacked_widget.addWidget(new_content_widget)

        # Show the corresponding content widget
        self.tab_changed(new_tab_index)

        # Activate the newly added tab
        self.tab_bar.setCurrentIndex(new_tab_index)

    def close_tab(self, index):
        # Get the tab name from the tab bar
        tab_name = self.tab_bar.tabText(index)
        self.tab_contents.remove(tab_name) # Option
        # Close the tab in the tab bar
        self.tab_bar.removeTab(index)

        self.stacked_widget.removeWidget(self.stacked_widget.widget(index))
        self.stacked_widget.setCurrentIndex(self.tab_bar.currentIndex())
        # Check if the tab name is in the set before removing it
        if tab_name in self.existing_tab_names:
            self.existing_tab_names.remove(tab_name)

    def generate_unique_tab_name(self):
        # Generate a unique tab name
        tab_name_base = "Tab"
        count = 1
        while True:
            tab_name = f"{tab_name_base} {count}"
            if tab_name not in self.tab_contents:
                break
            count += 1
        # Add the tab name to the set of existing names
        self.tab_contents.add(tab_name)
        return tab_name


if __name__ == '__main__':
    app = QApplication([])
    window = TabBarExample()
    window.show()
    app.exec()

# # Create a QTabBar
# self.tab_bar = QTabBar()
# self.tab_bar.setExpanding(False)
# self.tab_bar.setMovable(False)
# self.tab_bar.setTabsClosable(True)
#
# self.tab_bar.setStyleSheet(
#     """
#     QTabBar::pane {
#         background: transparent;
#         border: none;
#     }
#
#     QTabBar::tab {
#         background-color: lightblue;
#         padding: 8px 12px;
#         font-weight: None;
#     }
#
#     QTabBar::tab:selected {
#         border-top-left-radius: 4px;
#         border-top-right-radius: 4px;
#         background-color: lightblue;
#         font-weight: bold;
#     }
#
#     QTabBar::close-button {
#         subcontrol-position: right;
#     }
#
#     QTabBar::close-button:hover {
#         subcontrol-position: right;
#         border-radius: 2px;
#         font-weight: None;
#     }"""
# )
#
# # Connect the tabChanged signal to a custom slot
# self.tab_bar.currentChanged.connect(self.tab_changed)

''''''

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
