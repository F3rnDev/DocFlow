from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class SideBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setParent(parent)
        self.setup()
    
    def setup(self):
        self.collapsed = True

        self.widgetWidth = 450
        self.setFixedWidth(self.widgetWidth)

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.collapseArrow = QPushButton('<', self)
        self.collapseArrow.setFixedSize(40, 40)
        self.collapseArrow.clicked.connect(self.toggleCollapse)
        self.layout.addWidget(self.collapseArrow, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.stepInfoUI = StepInfoUI(self)
        self.layout.addWidget(self.stepInfoUI)
    
    def toggleCollapse(self, canToggle = False):
        if not self.collapsed:
            self.animateCollapse(self.x() + self.widgetWidth - self.collapseArrow.width(), self.y())
            self.collapseArrow.setText('<')
        else:
            self.animateCollapse(self.x() - self.widgetWidth + self.collapseArrow.width(), self.y())
            self.collapseArrow.setText('>')
        
        if not canToggle:
            self.collapsed = not self.collapsed
    
    def animateCollapse(self, posx, posy):
        self.animation = QPropertyAnimation(self, b'pos')
        self.animation.setDuration(300)
        self.animation.setStartValue(QPoint(self.x(), self.y()))
        self.animation.setEndValue(QPoint(posx, posy))
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.start()
    
    def responsiveResize(self, w, h, toolbarH):
        self.setGeometry(w - self.width(), toolbarH, self.width(), h - toolbarH)
        self.stepInfoUI.setFixedSize(self.width() - self.collapseArrow.width(), self.height())

        if self.collapsed:
            self.move(w - self.collapseArrow.width(), self.y())

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

class StepInfoUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setParent(parent)
        self.setup()
    
    def setup(self):
        self.setStyleSheet('''
                           background-color: #ffffff;
                           border-left: 2px solid #d0d0d0;
        ''')

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel('Step Information', self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.stepInfo = QLabel('Step 1', self)
        self.stepInfo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.stepInfo)

        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)