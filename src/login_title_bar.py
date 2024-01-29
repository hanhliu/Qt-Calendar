from PyQt5.QtSvg import QSvgWidget
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from custom_title_new.widget.actionable_title_bar import ActionableTitleBar
from custom_title_new.widget.button_title_bar import ButtonTitleBar

class LoginTitleBar(ActionableTitleBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.load_ui()

    def load_ui(self):
        # self.installEventFilter(self)

        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(2)


        # Min button /Users/hanhluu/Documents/Project/Qt/calendar_project/assets/minimize_window.svg
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
        self.layout_button = QHBoxLayout()
        self.layout_button.setAlignment(Qt.AlignmentFlag.AlignRight)
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(28, 28))
            self.layout_button.addWidget(button)
        #
        self.layout_main = QHBoxLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        # layout_main.setAlignment(Qt.AlignTop)
        # svg_widget = QSvgWidget("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/logo_vms.svg")
        # layout_main.addWidget(svg_widget)
        self.layout_title = QHBoxLayout()
        # self.layout_main.addWidget(QLabel("HanhLT"))
        self.layout_main.addLayout(self.layout_title, 80)
        self.layout_main.addLayout(self.layout_button, 10)
        #
        self.widget_main = QWidget()
        self.widget_main.setLayout(self.layout_main)
        # title_bar_layout.addLayout(layout_main)
        title_bar_layout.addWidget(self.widget_main)
        self.set_style_sheet()
        self.setLayout(title_bar_layout)

    def set_style_sheet(self):
        self.setStyleSheet(f"background-color: #1C2039;")

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.window_state_changed(self.parent.window().windowState())
        super().changeEvent(event)
        event.accept()

