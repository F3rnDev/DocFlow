from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt
from src.main.resource import Resource
from PIL import Image
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QRect, QSize

class FlowStep(QWidget):
    def __init__(self, name, icon, hasStep = False):
        super().__init__()

        self.defaultArrowIcon = Resource.resource_path('assets/nextFlowStep.png')

        self.curIcon = icon
        self.curName = name
        self.hasStep = False

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(50)

        self.content = QWidget(self)
        self.content.setGeometry(QRect(0, 0, 800, 800))

        self.flowImg = QLabel()
        self.flowImg.setPixmap(self.curIcon.scaled(200, 200))

        self.flowTxt = QLabel(self.curName)
        self.flowTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowTxt.setStyleSheet('''
            font-size: 50px;
        ''')

        self.contentLayout = QVBoxLayout(self.content)
        self.contentLayout.addWidget(self.flowImg)
        self.contentLayout.addWidget(self.flowTxt)

        self.layout.addWidget(self.content)
        self.arrow = QLabel()

        self.arrowImg = QPixmap(100, 100)
        self.arrowImg.fill(Qt.GlobalColor.transparent)

        if hasStep:
            self.arrowImg = QPixmap(self.defaultArrowIcon).scaled(100, 100)
            self.hasStep = True

        self.arrow.setPixmap(self.arrowImg)
        self.layout.addWidget(self.arrow)
    
    def generateImage(self):
        # desired_width = 700
        # desired_height = 700

        # scale_width = desired_width / self.width()
        # scale_height = desired_height / self.height()
        # scale = min(scale_width, scale_height)

        scale = 1.5

        self.resizeWidget(scale)
        
        pixmap = QPixmap(self.size())
        self.render(pixmap)

        self.resetWidget()

        return pixmap.toImage()
    

    def resetWidget(self):
        self.layout.setSpacing(50)

        self.flowImg.setPixmap(self.curIcon.scaled(200, 200))
        self.flowTxt.setStyleSheet('''
            font-size: 50px;
        ''')

        if self.hasStep:
            self.arrowImg = QPixmap(self.defaultArrowIcon).scaled(100, 100)
            self.arrow.setPixmap(self.arrowImg)
    

    def resizeWidget(self, scale):
        self.setStyleSheet('background-color: #ffffff;')

        self.flowImg.setPixmap(self.curIcon.scaled(int(self.flowImg.width()*scale), int(self.flowImg.height()*scale)))
        self.flowTxt.setStyleSheet(f'''
            font-size: {int(50*scale)}px;
        ''')

        self.layout.setSpacing(int(50*scale))

        if self.hasStep:
            self.arrowImg = QPixmap(self.defaultArrowIcon).scaled(int(100*scale), int(100*scale))
            self.arrow.setPixmap(self.arrowImg)
        else:
            self.arrowImg = QPixmap(100, 100)
            self.arrowImg.fill(Qt.GlobalColor.transparent)
        
        self.resize(((self.size() * scale)) + QSize(self.layout.spacing(), 0))