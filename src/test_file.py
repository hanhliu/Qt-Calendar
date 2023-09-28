import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap, QPalette, QGuiApplication, QColor, QPainter, QFont
from PySide6.QtCore import Qt

from pathlib import Path

basedir = os.path.dirname(__file__)


class ClickableQLabel(QLabel):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.setText(self.title)

    def enterEvent(self, event):
        f = QFont()
        f.setUnderline(True)
        self.setFont(f)

    def leaveEvent(self, event):
        f = QFont()
        f.setUnderline(False)
        self.setFont(f)

    def mousePressEvent(self, ev):
        print("HanhLT: mouse press click ")


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        screen = QGuiApplication.primaryScreen()
        desktop_screen_size = screen.availableGeometry()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setFixedSize(632, desktop_screen_size.height() - 30)
        # sshFile = os.path.join(basedir, "assets/qss", "login_form.qss")
        self.setStyleSheet(
            Path("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/qss/login_form.qss").read_text())

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 8, 0, 8)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignHCenter)
        self.central_widget.setLayout(self.central_layout)

        pixmap = QPixmap("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/logo_login.png")
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setPixmap(pixmap)
        self.label_image.resize(pixmap.width(), pixmap.height())

        intro_label = QLabel("Intelligent Video Analystics")
        intro_label.setStyleSheet('''
            QLabel
                {
                    font-size: 20px;
                    font-weight: 200;
                }
        ''')
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro_label.setObjectName("intro_label")

        self.username_edit = QLineEdit()
        self.username_edit.setFixedSize(360, 34)
        self.username_edit.setPlaceholderText("Username")

        self.password_edit = QLineEdit()
        self.password_edit.setFixedSize(360, 34)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Password")

        self.hBoxlayout = QHBoxLayout()
        self.hBoxlayout.setContentsMargins(0, 0, 0, 0)
        self.h_widget = QWidget()
        self.h_widget.setFixedWidth(360)
        self.h_widget.setLayout(self.hBoxlayout)
        self.forgot_label = ClickableQLabel("Forgot your password")
        # self.forgot_label.setStyleSheet('''
        #     QLabel:hover {
        #         background-color: #f0f0f0; /* Background color when hovering */
        #         color: #0000ff; /* Text color when hovering */
        #         text-decoration: underline; /* Text underline when hovering */
        #     }
        # ''')
        self.sso_label = ClickableQLabel("Sign in with SSO")
        self.hBoxlayout.addWidget(self.forgot_label)
        self.hBoxlayout.addStretch()
        self.hBoxlayout.addWidget(self.sso_label)

        login_button = QPushButton("LOGIN")
        login_button.setFixedSize(148, 34)
        self.central_layout.addStretch(4)
        self.central_layout.addWidget(self.label_image)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(intro_label)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(self.username_edit)
        self.central_layout.addWidget(self.password_edit)
        self.central_layout.addWidget(self.h_widget)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.central_layout.addStretch(4)

        layout.addWidget(self.central_widget)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the background image
        image = QPixmap("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/frame_login.png")
        painter.drawPixmap(self.rect(), image)

        # Call the base implementation of paintEvent
        super().paintEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        screen = QGuiApplication.primaryScreen()
        desktop_screen_size = screen.availableGeometry()

        primary_screen = QGuiApplication.primaryScreen()
        available_geometry = primary_screen.availableGeometry()
        full_geometry = primary_screen.geometry()
        title_bar_height = full_geometry.height() - available_geometry.height()

        print("Title bar height:", title_bar_height)
        self.setGeometry(desktop_screen_size)

        layout = QHBoxLayout()
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        # Set the background image
        self.set_background_image("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/login.png")

        # Create and center the login form widget
        login_form = LoginForm()
        # Add spacer item to push login form to the right
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)
        layout.addWidget(login_form)
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the background color to black
        pal = QPalette()
        pal.setColor(QPalette.Window, Qt.black)
        self.setPalette(pal)

    def set_background_image(self, image_path):
        # Apply style sheet to stretch the background image
        self.setStyleSheet("QMainWindow { background-image: url('" + image_path + "'); "
                                                                                  "background-repeat: no-repeat; background-position: center center; "
                                                                                  "background-attachment: fixed; }")


app = QApplication(sys.argv)
window = MainWindow()
window.show()

# Get the height of the title bar
frame_height = window.frameSize().height()
client_height = window.geometry().height()
title_bar_height = frame_height - client_height

print("Title bar height window :", title_bar_height)
sys.exit(app.exec())
