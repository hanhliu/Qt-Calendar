from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QApplication

from custom_title_new.widget.button_title_bar import ButtonTitleBar


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        # self.setBackgroundRole(QPalette.ColorRole.Highlight)
        # Install the event filter on this widget
        self.installEventFilter(self)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)

        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(2)

        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setStyleSheet(
            """font-weight: bold;
               border: 2px solid black;
               border-radius: 12px;
               margin: 2px;
            """
        )
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if title := parent.windowTitle():
            self.title.setText(title)
        # Min button
        self.min_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/minimize_window.svg")
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/maximize_window.svg")
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/close.svg")
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/normal_window.svg")
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)

        # Settings button
        self.settings_button = ButtonTitleBar(self, svg_path="/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/settings.svg")

        # Add buttons
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

        self.layout_main = QHBoxLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setAlignment(Qt.AlignTop)

        self.layout_title = QHBoxLayout()
        svg_widget = QSvgWidget("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/logo_vms.svg")

        self.layout_title.addWidget(self.title)
        self.layout_main.addWidget(svg_widget)
        self.layout_main.addLayout(self.layout_title, 80)
        self.layout_main.addLayout(self.layout_button, 10)

        self.widget_main = QWidget()
        self.widget_main.setLayout(self.layout_main)
        title_bar_layout.addWidget(self.widget_main)
        self.set_style_sheet()

    def set_style_sheet(self):
        self.setStyleSheet(f"background-color: #1C2039;")

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            # self.window().move(
            #     self.window().x() + delta.x(),
            #     self.window().y() + delta.y(),
            # )
            self._move()
        super().mouseMoveEvent(event)
        event.accept()

    def _move(self):
        window_move = self.window().windowHandle()
        window_move.startSystemMove()

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
                    if self.window().isMaximized():
                        self.window().showNormal()
                    else:
                        self.window().showMaximized()
        return super().eventFilter(watched, event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        central_widget = QWidget()
        self.title_bar = CustomTitleBar(self)

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(11, 11, 11, 11)
        work_space_layout.addWidget(QLabel("Hello, World!", self))

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, 0, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        centra_widget_layout.addLayout(work_space_layout)

        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)
        self.showMaximized()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

    def window_state_changed(self, state):
        self.title_bar.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
        self.title_bar.max_button.setVisible(state != Qt.WindowState.WindowMaximized)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()