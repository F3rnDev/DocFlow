from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyleOption, QStyle, QGridLayout
from src.main.resource import Resource
from PyQt6.QtGui import QEnterEvent, QMouseEvent, QPixmap, QPainter, QPen, QFont
from PyQt6.QtCore import QRect, QSize, Qt, pyqtSignal
import qtawesome
import textwrap

class FlowStep(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, name, icon, id, hasStep = False):
        super().__init__()

        self.id = id
        self.selected = False
        self.curIcon = icon
        self.hasStep = False

        self.defaultArrowIcon = qtawesome.icon('mdi.chevron-triple-right', color='#174077')

        self.layout = QGridLayout(self)

        self.flowImg = QLabel()
        self.flowImg.setPixmap(self.curIcon.pixmap(150, 150))
        self.flowImg.setFixedSize(200, 200)
        self.flowImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowImg.setStyleSheet('''
            background-color: white;
            border-radius: 30px;
            border: 5px solid #174077;
        ''')

        self.flowTxt = QLabel()
        self.flowTxt.setWordWrap(True)
        self.flowTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowTxt.setFixedWidth(270)
        self.flowTxt.setStyleSheet('''
            font-size: 32px;
            background-color: transparent;
            color: #174077;
            font-family: Roboto, sans-serif; 
            font-weight: bold;                                              
        ''')
        self.setName(name)

        self.arrow = QLabel()

        self.arrowImg = QPixmap(150, 150)
        self.arrowImg.fill(Qt.GlobalColor.transparent)

        if hasStep:
            self.arrowImg = QPixmap(self.defaultArrowIcon.pixmap(150, 150))
            self.hasStep = True
        
        self.arrow.setPixmap(self.arrowImg)

        self.layout.addWidget(self.arrow, 0, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.flowImg, 0, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.flowTxt, 1, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)

        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(20)
    
    def setSelected(self, selected):
        self.selected = selected

    def setName(self, name):
        self.curName = name
        self.flowTxt.setText(textwrap.fill(self.curName))
    
    def generateImage(self):
        wasSelected = False

        if self.selected == True:
            wasSelected = True
            self.setSelected(False)

        # desired_width = 700
        # desired_height = 700

        # scale_width = desired_width / self.width()
        # scale_height = desired_height / self.height()
        # scale = min(scale_width, scale_height)

        scale = 1.5

        self.resizeWidget(scale)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)

        self.render(pixmap)

        self.resizeWidget(1)

        if wasSelected:
            self.setSelected(True)

        return pixmap.toImage()
    

    def resizeWidget(self, scale):
        self.setStyleSheet('background-color: transparent;')

        self.flowImg.setPixmap(self.curIcon.pixmap(int(150*scale), int(150*scale)))
        self.flowImg.setFixedSize(int(200*scale), int(200*scale))
        self.flowImg.setStyleSheet(f'''
            background-color: white;
            border-radius: {int(30*scale)}px;
            border: {int(5*scale)}px solid #174077;
        ''')

        self.flowTxt.setFixedWidth(int(270*scale))
        self.flowTxt.setStyleSheet(f'''
            font-size: {int(32*scale)}px;
            background-color: transparent;
            color: #174077;
            font-family: Roboto, sans-serif; 
            font-weight: bold;                                              
        ''')

        self.layout.setVerticalSpacing(int(20*scale))

        if self.hasStep:
            self.arrowImg = self.defaultArrowIcon.pixmap(int(150*scale), int(150*scale))
            self.arrow.setPixmap(self.arrowImg)
        else:
            self.arrowImg = QPixmap(150, 150)
            self.arrowImg.fill(Qt.GlobalColor.transparent)
        
        self.resize(((self.size() * scale)) + QSize(self.layout.spacing(), 0))
    
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

        if self.selected:
            outlinePainter = QPainter(self)
            outlinePainter.setRenderHint(QPainter.RenderHint.Antialiasing)

            pen = QPen(Qt.PenStyle.DashLine)
            outlinePainter.setPen(pen)

            # Desenha um quadrado ao redor do widget
            square_rect = self.rect()
            outlinePainter.drawRect(square_rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.id)
