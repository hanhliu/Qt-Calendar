from PySide6.QtWidgets import QFrame


class SelectableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFrameShape(QFrame.Panel)
        self.is_selected = False