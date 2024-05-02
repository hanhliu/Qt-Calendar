import sys

from PySide6 import QtCore
from PySide6.QtCore import QPoint, QVariantAnimation, QEasingCurve, QEventLoop, QTimer
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QSplitter, QTextEdit, QVBoxLayout, QToolButton, QApplication, QSizePolicy, \
    QLabel, QPushButton


class AnimationLabel(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        self.setText("HanhLT")
        self.animation = QVariantAnimation()
        self.animation.valueChanged.connect(self.changeColor)
        self.animation.finished.connect(self.toggleFade)

    def changeColor(self, color):
        self.setStyleSheet(f'''
            QLabel {{
                background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});
            }}
        ''')

    def startFadeIn(self):
        self.animation.stop()
        self.animation.setStartValue(QColor(0, 0, 0, 0))
        self.animation.setEndValue(QColor(255, 255, 0, 255))
        self.animation.setDuration(500)  # Set duration to 5 seconds for fade-in
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def startFadeOut(self):
        self.animation.stop()
        self.animation.setStartValue(QColor(255, 255, 0, 255))
        self.animation.setEndValue(QColor(0, 0, 0, 0))
        self.animation.setDuration(500)  # Set duration to 5 seconds for fade-out
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def startAnimation(self):
        self.startFadeIn()

    def toggleFade(self):
        if self.animation.endValue().alpha() == 255:  # If fading in
            self.startFadeOut()
        else:
            self.startFadeIn()


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        self.greeting_text = AnimationLabel()
        lay.addWidget(self.greeting_text)
        btnFadeIn = QPushButton("fade in")
        btnFadeOut = QPushButton("fade out")
        btnAnimation = QPushButton("animation")
        btnStop = QPushButton("Stop")
        lay.addWidget(btnFadeIn)
        lay.addWidget(btnFadeOut)
        lay.addWidget(btnAnimation)
        lay.addWidget(btnStop)
        btnFadeIn.clicked.connect(self.greeting_text.startFadeIn)
        btnFadeOut.clicked.connect(self.greeting_text.startFadeOut)
        btnAnimation.clicked.connect(self.greeting_text.startAnimation)
        # btnStop.clicked.connect(self.greeting_text.stopAnimation)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec())

# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.mouse_pressed = False
#         self.is_collapse1 = True
#         self.is_collapse = True
#         self.splitter = QSplitter(self)
#
#         widget1 = QTextEdit("Widget 1")
#         widget2 = QTextEdit("Widget 2")
#         widget3 = QTextEdit("Widget 3")
#         widget3.setMaximumWidth(200)
#         widget3.setMinimumWidth(100)
#
#         # Set size policies
#         # widget1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#         # widget2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#         widget3.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
#
#         self.splitter.addWidget(widget1)
#         self.splitter.addWidget(widget2)
#         self.splitter.addWidget(widget3)
#
#         # self.splitter.setChildrenCollapsible(False)
#         self.splitter.splitterMoved.connect(self.handle_splitter_moved)
#
#
#
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.splitter)
#         self.handle = self.splitter.handle(1)
#
#         layout = QVBoxLayout()
#         layout.setContentsMargins(0, 0, 0, 0)
#         self.button = QToolButton(self.handle)
#         self.button.setArrowType(QtCore.Qt.LeftArrow)
#         self.button.clicked.connect(
#             lambda: self.handleSplitterButton(True))
#         self.button.mouseMoveEvent = self.mouse_move_event
#         layout.addWidget(self.button)
#         self.handle.setLayout(layout)
#
#         handle2 = self.splitter.handle(2)
#
#         layout2 = QVBoxLayout()
#         layout2.setContentsMargins(0, 0, 0, 0)
#         button3 = QToolButton(handle2)
#         button3.setArrowType(QtCore.Qt.RightArrow)
#         button3.clicked.connect(
#             lambda: self.handleSplitterButtonff(True))
#         layout2.addWidget(button3)
#         handle2.setLayout(layout2)
#
#
#     def mouse_move_event(self, event):
#         # global_position = self.button.mapToGlobal(event.pos())
#         # Get the position of the button
#         button_pos = self.button.mapToGlobal(event.position())
#
#         # Get the position of the handle
#         handle_pos = self.handle.mapToGlobal(self.handle.rect().center())
#
#         # Calculate the movement
#         move_delta = button_pos.x() - handle_pos.x()
#
#         # Update the position of the handle
#         new_x = handle_pos.x() + move_delta
#         new_pos = QPoint(new_x, handle_pos.y())
#
#         # Convert QPoint to int
#         int_pos = int(new_pos.x())
#         self.splitter.moveSplitter(int_pos, 1)
#
#         # Update the position of the handle
#         new_pos = self.handle.mapFromGlobal(QPoint(handle_pos.x() + move_delta, handle_pos.y()))
#
#         # self.handle.move(new_pos)
#         # self.handle.pos()
#         print(f"HanhLT: event position = {int_pos}")
#         pass
#
#     def handle_splitter_moved(self, pos, index):
#         print(f"HanhLT: pos = {pos}")
#         sizes = self.splitter.sizes()
#         if self.mouse_pressed and index == 1 and sizes[0] < 100:  # Handle 1 and size smaller than 100
#             print(f"HanhLT: chay vao day")
#             sizes[0] = 0
#             self.splitter.setSizes(sizes)
#
#     def handleSplitterButton(self, left=True):
#         if not all(self.splitter.sizes()):
#             if self.splitter.sizes()[2] == 0:
#                 if self.splitter.sizes()[0] == 0:
#                     self.splitter.setSizes([1, 5, 0])
#                 else:
#                     self.splitter.setSizes([0, 6, 0])
#             else:
#                 self.splitter.setSizes([1, 4, 1])
#         elif left:
#             self.splitter.setSizes([0, 5, 1])
#         else:
#             self.splitter.setSizes([1, 4, 1])
#
#     def handleSplitterButtonff(self, left=True):
#         if not all(self.splitter.sizes()):
#             if self.splitter.sizes()[0] == 0:
#                 if self.splitter.sizes()[2] == 0:
#                     self.splitter.setSizes([0, 5, 1])
#                 else:
#                     self.splitter.setSizes([0, 6, 0])
#             else:
#                 self.splitter.setSizes([1, 4, 1])
#         elif left:
#             self.splitter.setSizes([1, 5, 0])
#         else:
#             self.splitter.setSizes([1, 4, 1])
#
#
# if __name__ == '__main__':
#
#     import sys
#     app = QApplication(sys.argv)
#     window = Window()
#     window.showMaximized()
#     window.show()
#     sys.exit(app.exec())
