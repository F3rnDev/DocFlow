from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

class Window(QWidget):
    def __init__(self, content, title, w, h):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(w, h)

        self.content = content
        self.content.setParent(self)
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(e)