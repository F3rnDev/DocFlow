from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qtawesome
from src.main.screenManager import ScreenManager as manager
from components.window import Window

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
        self.collapseArrow.clicked.connect(lambda: self.toggleCollapse())
        self.layout.addWidget(self.collapseArrow, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.stepInfoUI = StepInfoUI(self)
        self.layout.addWidget(self.stepInfoUI)
    
    def toggleCollapse(self, curState = None):
        if curState == None:
            self.collapsed = not self.collapsed
        else:
            self.collapsed = curState
        
        windowRef = self.parent().parent()

        if windowRef != None:
            windowWidth = windowRef.width()

            collapsedPos = windowWidth - self.collapseArrow.width()
            expandedPos = windowWidth - self.widgetWidth

            if self.collapsed and self.x() == expandedPos:
                self.animateCollapse(collapsedPos, self.y())
                self.collapseArrow.setText('<')
            elif not self.collapsed and self.x() == collapsedPos:
                self.animateCollapse(expandedPos, self.y())
                self.collapseArrow.setText('>') 
    
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
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.stepName = stepOption(self, 'Nome da etapa:', 'Etapa')
        self.stepName.textChanged.connect(self.setText)
        self.layout.addWidget(self.stepName)

        self.stepIcon = stepOption(self, 'Ícone da etapa:', 'Ícone', True)
        self.stepIcon.textChanged.connect(self.checkIcon)
        self.stepIcon.searchSelected.connect(self.searchIcon)
        self.layout.addWidget(self.stepIcon)

        self.setLayout(self.layout)
    
    def setText(self, text:str):
        self.parent().parent().updateStepInfo(text)
    
    def searchIcon(self):
        print("open da window")
        self.iconWindow = Window(manager().getScreen("IconSelector"), "Selecione um ícone", 700, 700, True)
        self.iconWindow.show()
        self.iconWindow.content.selectItem.connect(self.parent().parent().updateStepIcon)    
    
    def checkIcon(self, iconEntered:str):
        print("check icon")
        qtawesome._instance()
        fontMaps = qtawesome._resource['iconic'].charmap

        self.iconNames = []
        for fontCollection, fontData in fontMaps.items():
            for iconName in fontData:
                self.iconNames.append('%s.%s' % (fontCollection, iconName))
        if iconEntered in self.iconNames:
            self.parent().parent().updateStepIcon(iconEntered)
    
    def setStepIcon(self, iconName):
        self.stepIcon.textChanged.disconnect()
        self.stepIcon.lineEdit.setText(iconName)
        self.stepIcon.textChanged.connect(self.checkIcon)
    
    def setStepName(self, name):
        self.stepName.lineEdit.setText(name)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

class stepOption(QWidget):
    searchSelected = pyqtSignal()
    textChanged = pyqtSignal(str)

    def __init__(self, parent, fieldName, placeholder, search = False):
        super().__init__(parent)
        self.setParent(parent)
        self.setup(fieldName, placeholder, search)
    
    def setup(self, fieldName, placeholder, search = False):
        self.layout = QVBoxLayout(self)

        self.label = QLabel(fieldName, self)
        self.label.setStyleSheet('''
                                border: none;
                                font-size: 20px;
                                font-weight: bold;
        ''')
        self.layout.addWidget(self.label)

        self.barEdit = QWidget(self)
        self.barEditLayout = QHBoxLayout(self.barEdit)
        self.barEditLayout.setSpacing(0)
        self.barEditLayout.setContentsMargins(0, 0, 0, 0)
        self.barEditLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText(placeholder)
        self.lineEdit.setFixedSize(300, 50)
        self.lineEdit.textChanged.connect(lambda: self.textChanged.emit(self.lineEdit.text()))
        self.lineEdit.setStyleSheet('''
                                font-size: 20px;
        ''')
        self.barEditLayout.addWidget(self.lineEdit)

        if search:
            self.searchButton = QPushButton('', self)
            self.searchButton.setFixedSize(50, 50)
            self.barEditLayout.addWidget(self.searchButton)
            self.searchButton.setIcon(qtawesome.icon('fa.search', color = '#000000'))
            self.searchButton.setIconSize(QSize(20, 20))
            self.searchButton.clicked.connect(self.searchSelected.emit)

            self.lineEdit.setFixedWidth(250)
        
        self.layout.addWidget(self.barEdit)