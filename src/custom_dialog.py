import sys

from PySide6.QtGui import QImage, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QMainWindow, QDialog, \
    QPushButton, QFrame


class CustomDialog(QDialog):
    def __init__(self, parent=None, title=None, width=None, height=None, content=None):
        super().__init__(parent)
        self.title = title
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.load_ui()

    def load_ui(self):
        self.create_title_bar()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        # button Cancel
        self.select_button_layout = QHBoxLayout()

        self.button_cancel = QPushButton(self.tr("Cancel"))
        # border-radius: 5px; border color red, text color red, background color transparent

        self.button_cancel.clicked.connect(self.close)
        self.select_button_layout.addWidget(self.button_cancel)
        # align right
        self.select_button_layout.setAlignment(self.button_cancel, Qt.AlignRight)
        self.select_button_layout.setContentsMargins(0, 0, 20, 20)

        self.ai_widget = QWidget()

        self.main_layout.addWidget(self.title_bar_widget, 5)
        # add layout
        # self.main_layout.addWidget(self.image_result_widget, 30)
        # create divider
        self.divider = QFrame()
        self.divider.setFixedHeight(1)
        self.main_layout.addWidget(self.divider)
        self.main_layout.addWidget(self.ai_widget, 80)
        self.main_layout.addLayout(self.select_button_layout, 10)

        # set layout
        self.setLayout(self.main_layout)
        self.setFixedSize(800, 700)
        self.setModal(False)
        QApplication.instance().installEventFilter(self)

    def create_title_bar(self):
        # layout
        self.title_bar_widget = QWidget()
        self.title_bar_widget.setObjectName("title_bar")
        # set background Style.Color.primary
        self.title_bar_widget.setStyleSheet(f"background-color: red; border-top-left-radius: 10px; border-top-right-radius: 10px;")

        self.title_bar_layout = QHBoxLayout()
        # event name
        self.title_name_label = QLabel(f"{self.title}")
        self.title_name_label.setStyleSheet(f"color: white; font-weight: bold")
        close_icon = QIcon("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/left.png")
        self.close_button = QPushButton(close_icon, "")
        self.close_button.setIconSize(QSize(15, 15))
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("background-color: transparent")
        self.close_button.clicked.connect(self.close)
        # add widget
        self.title_bar_layout.addWidget(self.title_name_label, 90)
        self.title_bar_layout.addWidget(self.close_button, 10)
        self.title_bar_widget.setLayout(self.title_bar_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            # Kiểm tra xem vị trí của sự kiện chuột có nằm trong vùng của cửa sổ cha hay không

            global_pos = event.globalPosition().toPoint()
            if not self.geometry().contains(global_pos):
                QApplication.instance().removeEventFilter(self)
                self.close()
        return super().eventFilter(source, event)

class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.custom_menu = QPushButton("Show Dialog")
        self.custom_menu.clicked.connect(self.show_dialog)
        self.layout.addWidget(self.custom_menu)
        self.central_widget.setLayout(self.layout)

    def show_dialog(self):
        self.dialog = CustomDialog(title="HanhLT")
        self.dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = VideoPlayerApp()
    main_window.show()
    sys.exit(app.exec())
