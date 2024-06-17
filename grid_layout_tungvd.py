import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup

class GridWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('3x3 Grid Layout with Animations')
        self.layout = QGridLayout()
        self.labels = [[None for _ in range(3)] for _ in range(3)]
        self.create_grid()
        self.setLayout(self.layout)

    def create_grid(self):
        for row in range(3):
            for col in range(3):
                label = QLabel(f'({row}, {col})')
                label.setStyleSheet("border: 1px solid black;")
                label.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(label, row, col)
                self.labels[row][col] = label

        self.swap_button = QPushButton('Swap (0,0) with (1,1)')
        self.swap_button.clicked.connect(self.animate_swap)
        self.layout.addWidget(self.swap_button, 3, 0)

        self.fade_button = QPushButton('Fade (0,0)')
        self.fade_button.clicked.connect(lambda: self.animate_fade(0, 0))
        self.layout.addWidget(self.fade_button, 3, 1)

        self.zoom_button = QPushButton('Zoom (0,0)')
        self.zoom_button.clicked.connect(lambda: self.animate_zoom(0, 0))
        self.layout.addWidget(self.zoom_button, 3, 2)

    def animate_swap(self):
        self.swap_cells(0, 0, 1, 1)

    def swap_cells(self, row1, col1, row2, col2):
        label1 = self.labels[row1][col1]
        label2 = self.labels[row2][col2]

        pos1 = self.layout.cellRect(row1, col1).topLeft()
        pos2 = self.layout.cellRect(row2, col2).topLeft()

        animation1 = QPropertyAnimation(label1, b"pos")
        animation1.setDuration(500)
        animation1.setStartValue(label1.pos())
        animation1.setEndValue(pos2)

        animation2 = QPropertyAnimation(label2, b"pos")
        animation2.setDuration(500)
        animation2.setStartValue(label2.pos())
        animation2.setEndValue(pos1)

        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(animation1)
        self.animation_group.addAnimation(animation2)
        self.animation_group.finished.connect(lambda: self.finalize_swap(row1, col1, row2, col2))

        self.animation_group.start()

    def finalize_swap(self, row1, col1, row2, col2):
        label1 = self.labels[row1][col1]
        label2 = self.labels[row2][col2]

        self.layout.removeWidget(label1)
        self.layout.removeWidget(label2)

        self.layout.addWidget(label1, row2, col2)
        self.layout.addWidget(label2, row1, col1)

        self.labels[row1][col1], self.labels[row2][col2] = self.labels[row2][col2], self.labels[row1][col1]

    def animate_fade(self, row, col):
        label = self.labels[row][col]
        opacity_effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(opacity_effect)

        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(1000)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.setEasingCurve(QEasingCurve.OutCubic)

        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(1000)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.setEasingCurve(QEasingCurve.InCubic)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(fade_out)
        self.animation_group.addAnimation(fade_in)
        self.animation_group.start()

    def animate_zoom(self, row, col):
        label = self.labels[row][col]
        zoom_in = QPropertyAnimation(label, b"geometry")
        zoom_in.setDuration(500)
        zoom_in.setStartValue(label.geometry())
        zoom_in.setEndValue(label.geometry().adjusted(-10, -10, 10, 10))

        zoom_out = QPropertyAnimation(label, b"geometry")
        zoom_out.setDuration(500)
        zoom_out.setStartValue(label.geometry().adjusted(-10, -10, 10, 10))
        zoom_out.setEndValue(label.geometry())

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(zoom_in)
        self.animation_group.addAnimation(zoom_out)
        self.animation_group.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GridWindow()
    window.show()
    sys.exit(app.exec())
