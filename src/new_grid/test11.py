import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QPushButton

class MyWidget(QWidget):
    def __init__(self, rows=4, cols=4):
        super().__init__()

        self.rows = rows
        self.cols = cols

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        self.frames = [[QFrame() for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                self.frames[i][j].setFrameShape(QFrame.StyledPanel)
                grid_layout.addWidget(self.frames[i][j], i, j)
                self.frames[i][j].mousePressEvent = lambda event, row=i, col=j: self.onFrameClick(event, row, col)

        merge_button = QPushButton('Merge')
        merge_button.clicked.connect(self.mergeSelected)
        grid_layout.addWidget(merge_button, self.rows, 0, 1, self.cols)

        self.selected_frames = set()

        self.setLayout(grid_layout)

        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('Merge Grid')
        self.show()

    def onFrameClick(self, event, row, col):
        frame = self.frames[row][col]
        if frame in self.selected_frames:
            frame.setStyleSheet('')
            self.selected_frames.remove(frame)
        else:
            frame.setStyleSheet('border: 1px solid red;')
            self.selected_frames.add(frame)
    def mergeSelected(self):
        if len(self.selected_frames) >= 2:
            merged_frame = QFrame()
            merged_frame.setFrameShape(QFrame.StyledPanel)
            row1, col1 = min((i, j) for i, j in self.get_selected_positions())
            row2, col2 = max((i, j) for i, j in self.get_selected_positions())

            for frame in self.selected_frames:
                frame.setStyleSheet('')
                frame.setParent(None)
            self.layout().addWidget(merged_frame, row1, col1, row2 - row1 + 1, col2 - col1 + 1)

            self.selected_frames.clear()
            self.selected_frames.add(merged_frame)

    def get_selected_positions(self):
        return [(i, j) for frame in self.selected_frames for i in range(self.rows) for j in range(self.cols) if self.frames[i][j] is frame]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget(rows=4, cols=4)
    sys.exit(app.exec_())
