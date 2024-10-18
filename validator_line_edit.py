import os
import sys

from PySide6.QtCore import QRegularExpression
from pydantic import AnyUrl
import re
from typing import Optional
from PySide6.QtGui import Qt, QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton, QGridLayout, \
    QDialog, QLineEdit, QMessageBox


class IPLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        ip_regex = QRegularExpression(r'^(\d{1,3}\.){0,3}\d{0,3}$')
        self.setValidator(QRegularExpressionValidator(ip_regex, self))

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_0, Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3,
                           Qt.Key.Key_4, Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7,
                           Qt.Key.Key_8, Qt.Key.Key_9]:
            current_text = self.text()
            segments = current_text.split('.')
            last_segment = segments[-1]

            if len(last_segment) == 2 and len(segments) < 4:
                super().keyPressEvent(event)
                self.setText(self.text() + '.')
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()
        self.updating = False
        self.block_signal = False

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("IP/RTSP link")

        self.from_IP= IPLineEdit("0.0.0.0", self)
        self.from_IP.setFixedWidth(200)
        self.from_IP.setPlaceholderText("0.0.0.0")

        self.to_IP = IPLineEdit("0.0.0.255")
        self.to_IP.setFixedWidth(200)
        self.to_IP.setPlaceholderText("0.0.0.255")

        self.label = QLabel('HanhLT')
        self.label.setFixedHeight(20)
        self.btn_1 = QPushButton('Validate Line Edit')
        self.btn_1.clicked.connect(self.validate_input)
        self.btn_2 = QPushButton('Button 2')
        self.btn_2.setFixedWidth(200)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        largest_item = QWidget()
        largest_item.setStyleSheet('background-color: lightblue;')
        grid_layout.addWidget(largest_item, 1, 1, 2, 2)  # Span 3 rows and 3 columns, starting from row 1 and column 1
        self.add_position_label(largest_item, 1, 1)
        for row in range(0, 4):
            for col in range(0, 4):
                if row == 1 and col == 1:
                    continue  # Skip the center item
                item = QWidget()
                item.setStyleSheet('background-color: lightblue;')
                grid_layout.addWidget(item, row, col)

        self.central_layout.addWidget(self.line_edit)
        self.central_layout.addWidget(self.label)
        self.central_layout.addWidget(self.btn_1)
        self.central_layout.addWidget(self.from_IP)
        self.central_layout.addWidget(self.to_IP)
        self.central_layout.addWidget(self.btn_2)
        self.central_layout.addLayout(grid_layout)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # Connect the textChanged signals to the appropriate slots
        self.from_IP.textChanged.connect(self.sync_from_ip_to_ip)
        self.to_IP.textChanged.connect(self.sync_to_ip_to_from_ip)

    def sync_from_ip_to_ip(self, text):
        if self.block_signal:
            return
        self.block_signal = True

        from_segments = text.split('.')
        to_segments = self.to_IP.text().split('.')

        # Update segments in to_ip based on from_ip
        for i in range(len(from_segments)):
            if i < len(to_segments):
                to_segments[i] = from_segments[i]
            else:
                to_segments.append(from_segments[i])

        while len(to_segments) < 4:
            to_segments.append('0')

        to_segments[-1] = '255'
        self.to_IP.setText('.'.join(to_segments[:4]))
        self.block_signal = False

    def sync_to_ip_to_from_ip(self, text):
        if self.block_signal:
            return
        self.block_signal = True

        to_segments = text.split('.')
        from_segments = self.from_IP.text().split('.')

        # Ensure from_segments has at least 4 segments
        while len(from_segments) < 4:
            from_segments.append('0')

        # Update the first three segments of from_ip based on to_ip
        for i in range(3):
            if i < len(to_segments):
                from_segments[i] = to_segments[i]

        # Preserve the last segment of from_ip
        # The last segment of from_ip should not be overwritten
        self.from_IP.setText('.'.join(from_segments[:4]))
        self.block_signal = False

    def add_position_label(self, item, row, col):
        if row == 1 and col == 1:  # Add label only to the largest item
            label = QLabel(f"Position: ({row}, {col})")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout = QVBoxLayout(item)
            layout.addWidget(label)

    def text_to_IP_change(self):
        pass

    def validate_input(self):
        text = self.line_edit.text().strip()
        if self.is_valid_ip(text):
            print(f"HanhLT: IP ADDRESS = {text}")
        else:
            rtsp = AnyUrl(text)
            password = rtsp.password
            username = rtsp.username
            ip_address = rtsp.host
            port = rtsp.port
            path = rtsp.path
            query = rtsp.query
            print(f"HanhLT: username={username}   password={password}  ip_address={ip_address}  port={port}    path={path}     query = {query}")

    def is_valid_ip(self, ip):
        ip_regex = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
        return ip_regex.match(ip) is not None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
