from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

class ActionableTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initial_pos = None
        self.parent = parent
        self.installEventFilter(self)

    def _move(self):
        window_move = self.parent.window().windowHandle()
        window_move.startSystemMove()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            self._move()
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def eventFilter(self, watched, event):
        if watched == self:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                mouse_button = event.button()
                if mouse_button == Qt.LeftButton:
                    # Toggle between full screen and normal mode
                    print(f"HanhLT: self.parent.window() = {self.parent.window()}")
                    if self.parent.window().isMaximized():
                        self.parent.window().showNormal()
                    else:
                        self.parent.window().showMaximized()
        return super().eventFilter(watched, event)


