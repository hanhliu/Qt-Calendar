from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout
from src.custom_widget.layer_selection_widget import LayersSelectorWidget

class LeftSideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        screen = QGuiApplication.primaryScreen()
        full_screen_size = screen.geometry()
        desktop_screen_size = screen.availableGeometry()
        screen_size = screen.size()
        width_screen = screen_size.width()
        height_screen = screen_size.height()
        self.setFixedWidth(width_screen * 0.2)

        # set background
        self.setStyleSheet("background-color: #B2D3C2;")

        my_widget = LayersSelectorWidget()

        # create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(my_widget)
        self.setLayout(self.layout)
