import sys

from PyQt5.QtSvg import QGraphicsSvgItem
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QGraphicsView, QGraphicsScene
from PySide6.QtCore import QDate, Qt

from src.common_controller.common_qsettings import CommonQSettings
from src.common_controller.main_controller import MainController
from src.grid_custom.grid_main import MainGrid
from src.grid_custom.grid_main_two import MainGridTwo

class ButtonTitleBar(QWidget):
    def __init__(self, parent=None, svg_path=None):
        super().__init__(parent)
        self.svg_path = svg_path
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        # Create a QGraphicsView to display the SVG
        svg_view = QGraphicsView(self)
        svg_scene = QGraphicsScene()
        svg_view.setScene(svg_scene)

        # Create a QGraphicsSvgItem to load and display the SVG file
        svg_item = QGraphicsSvgItem(self.svg_path)
        svg_scene.addItem(svg_item)

        self.layout.addWidget(svg_view)
        self.setLayout(self.layout)

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass

    def mousePressEvent(self, ev):
        pass



class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)




        self.setLayout(self.layout)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.showFullScreen()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.CustomizeWindowHint)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.main_controller = MainController()
        self.common_qsettings = CommonQSettings()
        self.main_controller.list_divisions = self.common_qsettings.get_data_grid()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Custom Grid')

        layout = QVBoxLayout()
        self.mainwindow = MainGridTwo()
        layout.addWidget(self.mainwindow)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())
