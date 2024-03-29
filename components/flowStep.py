from PyQt6.QtWidgets import QWidget, QLabel, QStyleOption, QStyle, QGridLayout
from PyQt6.QtGui import QEnterEvent, QMouseEvent, QPixmap, QPainter, QPen
from PyQt6.QtCore import QRect, QSize, Qt, pyqtSignal
import qtawesome
import textwrap
from enum import Enum

class FlowStatus(Enum):
    # NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2

class FlowStep(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, name, icon, id, hasStep = False):
        super().__init__()

        self.id = id
        self.selected = False
        self.curIcon = icon
        self.hasStep = hasStep
        self.defaultSize = None

        self.defaultArrowIcon = qtawesome.icon('mdi.chevron-triple-right')

        self.setStyleSheet('''
            QWidget {
                background-color: transparent;
            }

            QWidget::hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        ''')

        self.flowImg = QLabel()
        self.flowImg.setFixedSize(200, 200)
        self.flowImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowImg.setStyleSheet('''
            background-color: white;
            border-radius: 30px;
            border: 5px solid;
        ''')

        self.flowTxt = QLabel()
        self.flowTxt.setWordWrap(True)
        self.flowTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowTxt.setFixedWidth(270)
        self.flowTxt.setStyleSheet('''
            font-size: 32px;
            background-color: transparent;
            font-family: Roboto, sans-serif; 
            font-weight: bold;                                              
        ''')
        self.setName(name)

        self.arrow = QLabel()
        self.arrow.setStyleSheet('background-color: transparent;')
        self.arrowImg = QPixmap(150, 150)
        self.arrowImg.fill(Qt.GlobalColor.transparent)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.arrow, 0, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.flowImg, 0, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.flowTxt, 1, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(20)

        self.setStatus(FlowStatus.DONE)
        
    def setSelected(self, selected):
        self.selected = selected

    def setName(self, name):
        self.curName = name
        self.flowTxt.setText(textwrap.fill(self.curName))
    
    def setStatus(self, curStatus):
        arrowColor = ''
        iconColor = ''

        match curStatus:
            # case FlowStatus.NOT_STARTED:
            #     self.flowImg.setStyleSheet(f'{self.flowImg.styleSheet()} border-color: #aeabab; background-color: white;')
            #     self.flowTxt.setStyleSheet(f'{self.flowTxt.styleSheet()} color: #aeabab;')
            #     arrowColor = '#aeabab'
            #     iconColor = '#8497B0'
            
            case FlowStatus.IN_PROGRESS:
                self.flowImg.setStyleSheet(f'{self.flowImg.styleSheet()} border-color: #2F5597; background-color: #2F5597;')
                self.flowTxt.setStyleSheet(f'{self.flowTxt.styleSheet()} color: #2F5597;')
                arrowColor = '#2F5597'
                iconColor = 'white'
            
            case FlowStatus.DONE:
                self.flowImg.setStyleSheet(f'{self.flowImg.styleSheet()} border-color: #2F5597; background-color: white;')
                self.flowTxt.setStyleSheet(f'{self.flowTxt.styleSheet()} color: #2F5597;')
                arrowColor = '#2F5597'
                iconColor = '#2F5597'
            
        if self.hasStep:
            self.defaultArrowIcon = qtawesome.icon('mdi.chevron-triple-right', color=arrowColor)
            self.arrowImg = QPixmap(self.defaultArrowIcon.pixmap(150, 150))
    
        self.arrow.setPixmap(self.arrowImg)

        self.icon = qtawesome.icon(self.curIcon, color=iconColor)
        self.flowImg.setPixmap(self.icon.pixmap(150, 150))

    
    def generateImage(self):
        wasSelected = False

        if self.selected == True:
            wasSelected = True
            self.setSelected(False)

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
    
        self.flowImg.setPixmap(self.icon.pixmap(int(150*scale), int(150*scale)))
        self.flowImg.setFixedSize(int(200*scale), int(200*scale))
        self.flowImg.setStyleSheet(f'''
            {self.flowImg.styleSheet()}
            border-radius: {int(30*scale)}px;
            border-width: {int(5*scale)}px;
        ''')

        self.flowTxt.setFixedWidth(int(270*scale))
        self.flowTxt.setStyleSheet(f'''
            {self.flowTxt.styleSheet()}
            font-size: {int(32*scale)}px;                                             
        ''')

        self.layout.setVerticalSpacing(int(20*scale))

        if self.hasStep:
            self.arrowImg = self.defaultArrowIcon.pixmap(int(150*scale), int(150*scale))
            self.arrow.setPixmap(self.arrowImg)
        else:
            self.arrowImg = QPixmap(150, 150)
            self.arrowImg.fill(Qt.GlobalColor.transparent)

        self.resize(((self.defaultSize * scale)) + QSize(self.layout.spacing(), 0))
    
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

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def leaveEvent(self, event):
        self.unsetCursor()
