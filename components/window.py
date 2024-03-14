from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget

class Window(QWidget):
    def __init__(self, content, title, w, h, fixedSize = False):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(w, h)

        self.content = content
        self.content.setParent(self)

        if fixedSize:
            self.setFixedSize(w, h)
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.closeWindow()
        else:
            super().keyPressEvent(e)
    
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.content.resize(self.width(), self.height())
    
    def closeWindow(self):
        self.close()