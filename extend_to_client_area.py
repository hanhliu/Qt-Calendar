from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Central Widget
        central_widget = QTextEdit()
        self.setCentralWidget(central_widget)

        # Dock Widget
        dock_widget = QDockWidget("Dock Widget", self)
        dock_widget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        dock_widget_content = QTextEdit()
        dock_widget.setWidget(dock_widget_content)

        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        # Window setup
        self.setWindowTitle("QDockWidget Example")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec()
