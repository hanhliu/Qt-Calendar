from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QPushButton, \
    QStackedLayout, QSizePolicy

from custom_title_new.widget.actionable_title_bar import ActionableTitleBar
from custom_title_new.widget.button_title_bar import ButtonTitleBar


class HomeTitleBar(ActionableTitleBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.widget_icon_app = QWidget()
        self.widget_icon_app.setFixedSize(45, 28)
        self.widget_icon_app.setStyleSheet("background-color: lightblue")

        self.widget_search = QWidget()
        self.widget_search.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.widget_search.setStyleSheet("background-color: lightblue")
        self.layout_search = QHBoxLayout(self.widget_search)
        self.layout_search.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stacked_search = QStackedLayout()
        self.stacked_search.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("HANHHHHH")
        label.setFixedHeight(28)
        button_new_search = QPushButton("NEW SEARCH")
        button_new_search.setFixedHeight(28)
        self.stacked_search.addWidget(button_new_search)
        self.stacked_search.addWidget(label)
        self.layout_search.addLayout(self.stacked_search)

        self.widget_tab_bar = QWidget()

        self.layout_tab_bar = QHBoxLayout(self.widget_tab_bar)
        self.layout_tab_bar.addWidget(QLabel("TAB"), 8)
        self.layout_tab_bar.addWidget(QLabel("BUTTON GRID"), 1)

        self.layout_button_system = QHBoxLayout()
        self.min_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/minimize_window.svg")

        # Max button
        self.max_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/maximize_window.svg")

        # Close button
        self.close_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/close.svg")
        self.close_button.clicked.connect(self.parent.window().close)

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

        self.layout.addWidget(self.widget_icon_app, 1)
        self.layout.addWidget(self.widget_search, 2)
        self.layout.addWidget(self.widget_tab_bar, 6)
        self.layout.addLayout(self.layout_button_system, 1)

        self.setLayout(self.layout)

