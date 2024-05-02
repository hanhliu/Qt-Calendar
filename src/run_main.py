import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QVBoxLayout, QPushButton
from login_title_bar import LoginTitleBar
from home_title_bar import HomeTitleBar




class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(400, 200)

        central_widget = QWidget()
        self.title_bar = HomeTitleBar(parent=self)

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(0, -9, 0, 0)
        work_space_layout.addWidget(QLabel("Hello, World!", self))
        button1 = QPushButton("Button 1")
        button1.clicked.connect(self.button1_click)
        button2 = QPushButton("Button 2")
        button2.clicked.connect(self.button2_click)
        button3 = QPushButton("Button 3")
        button3.clicked.connect(self.button3_click)

        work_space_layout.addWidget(button1)
        work_space_layout.addWidget(button2)
        work_space_layout.addWidget(button3)

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, -20, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        centra_widget_layout.addLayout(work_space_layout)

        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)
        self.showMaximized()

    def button1_click(self):
        new_layout = QVBoxLayout()
        new_layout.addWidget(QPushButton("New button"))
        self.title_bar.stacked_search.setCurrentIndex(1)
        # self.title_bar.widget_search.repaint()

    def button2_click(self):
        # Toggle visibility of widget_search
        self.title_bar.widget_search.setVisible(not self.title_bar.widget_search.isVisible())

    def button3_click(self):
        # Restore visibility of widget_search
        self.title_bar.widget_search.setVisible(True)

    # def changeEvent(self, event):
    #     if event.type() == QEvent.Type.WindowStateChange:
    #         self.title_bar.window_state_changed(self.windowState())
    #     super().changeEvent(event)
    #     event.accept()
    #
    # def window_state_changed(self, state):
    #     self.title_bar.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
    #     self.title_bar.max_button.setVisible(state != Qt.WindowState.WindowMaximized)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
