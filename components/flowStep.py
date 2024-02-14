from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyleOption, QStyle
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

        self.defaultArrowIcon = qtawesome.icon('mdi.chevron-triple-right', color='#174077').pixmap(150, 150)

        self.curIcon = icon
        self.curName = name
        self.hasStep = False

        self.layout = QHBoxLayout(self)

        self.content = QWidget(self)
        self.content.setGeometry(QRect(0, 0, 800, 800))
        self.content.setStyleSheet('background-color: transparent;')

        self.flowImg = QLabel()
        self.flowImg.setPixmap(qtawesome.icon('fa5s.cog', color='#174077').pixmap(150, 150))
        self.flowImg.setFixedSize(200, 200)
        self.flowImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowImg.setStyleSheet('''background-color: white;
                                    border-radius: 20px;
                                    border: 5px solid #174077;
                                   ''')

        self.flowTxt = QLabel()
        self.flowTxt.setWordWrap(True)
        self.flowTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowTxt.setFixedWidth(270)
        self.flowTxt.setStyleSheet('''
            font-size: 35px;
            background-color: transparent;
            color: #174077;
            font-family: Roboto, sans-serif; 
            font-weight: bold;                                              
        ''')
        self.updateText()

        self.contentLayout = QVBoxLayout(self.content)
        self.layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.contentLayout.setSpacing(20)
        self.contentLayout.addWidget(self.flowImg, 0, Qt.AlignmentFlag.AlignCenter)
        self.contentLayout.addWidget(self.flowTxt, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.layout.addWidget(self.content)

        self.arrow = QLabel()
        self.arrow.setStyleSheet('background-color: transparent;')

        self.arrowImg = QPixmap(150, 150)
        self.arrowImg.fill(Qt.GlobalColor.transparent)

        if hasStep:
            self.arrowImg = QPixmap(self.defaultArrowIcon)
            self.hasStep = True
        
        self.arrow.setPixmap(self.arrowImg)
        self.layout.addWidget(self.arrow, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        self.content.resize(270, 0)
    
    def setSelected(self, selected):
        self.selected = selected

    def setName(self, name):
        self.curName = name
        self.updateText()
    
    def updateText(self):
        self.flowTxt.setText(textwrap.fill(self.curName, 14))
    
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

        self.flowImg.setPixmap(self.curIcon.scaled(int(200*scale), int(200*scale)))

        self.flowTxt.setStyleSheet(f'''
            font-size: {int(25*scale)}px;
        ''')
        self.flowTxt.setFixedWidth(int(200*scale))

        self.layout.setSpacing(int(50*scale))

        if self.hasStep:
            self.arrowImg = QPixmap(self.defaultArrowIcon).scaled(int(100*scale), int(100*scale))
            self.arrow.setPixmap(self.arrowImg)
        else:
            self.arrowImg = QPixmap(100, 100)
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
