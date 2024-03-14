from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qtawesome
from PyQt6.QtCore import *

class ToolBarOptions(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup(parent)
    
    def setup(self, parent):
        self.resize(1920, 80)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setStyleSheet('''
            background-color: #ffffff;
            border: 2px solid #d0d0d0;
            ''')

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.addSaveOptions(parent)
        self.layout.addStretch(1)
        self.addCreationOptions(parent)
        self.layout.addStretch(1)

        exportBtn = toolBarBttn(self, 'fa5s.file-export', 'Exportar Imagens')
        exportBtn.clicked.connect(parent.openExportWindow)
        self.layout.addWidget(exportBtn)
        self.setLayout(self.layout)
    
    def addCreationOptions(self, parent):
        addFlowBtn = toolBarBttn(self, 'fa5s.plus', 'Adicionar Etapa')
        addFlowBtn.clicked.connect(parent.addFlowStep)
        self.layout.addWidget(addFlowBtn)
    
    def addSaveOptions(self, parent):
        fileOptions = [['Novo Projeto', 'fa5s.file', parent.newProject, True], 
            ['Salvar', 'fa5s.save', parent.saveFlow, False], 
            ['Salvar Como', 'mdi6.content-save-plus', parent.saveAsFlow], 
            ['Abrir Fluxo', 'fa5s.folder-open', parent.openFlow]]

        optionButton = toolBarBttn(self, None, 'Arquivo', fileOptions)

        self.layout.addWidget(optionButton)

        # newProjectBtn = toolBarBttn(self, 'fa5s.file', 'Novo Projeto')
        # newProjectBtn.clicked.connect(parent.newProject)

        # saveBtn = toolBarBttn(self, 'fa5s.save', 'Salvar')
        # saveBtn.clicked.connect(parent.saveFlow)

        # saveAsBtn = toolBarBttn(self, 'mdi6.content-save-plus', 'Salvar Como')
        # saveAsBtn.clicked.connect(parent.saveAsFlow)

        # openBtn = toolBarBttn(self, 'fa5s.folder-open', 'Abrir Fluxo')
        # openBtn.clicked.connect(parent.openFlow)

        # self.layout.addWidget(newProjectBtn)
        # self.layout.addWidget(saveBtn)
        # self.layout.addWidget(saveAsBtn)
        # self.layout.addWidget(openBtn)
    
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

class toolBarCategory(QWidget):
    def __init__(self, parent, title):
        super().__init__(parent)

        self.setStyleSheet('''
            background-color: #d0d0d0;
            border: none;
        ''')

        self.layout = QVBoxLayout(self)

        self.title = QLabel(title, self)
        self.title.setStyleSheet('''
            font-size: 13px;
            color: #000000;
        ''')

        self.layout.addWidget(self.title)
        self.setLayout(self.layout)
    
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)

class toolBarBttn(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent, icon, tooltip, options = None):
        super().__init__(parent)

        self.setStyleSheet('''
            QWidget {
                background-color: transparent;
                border: 0px;
                border-radius: 5px;
                text-align: center;
            }
                                 
            QWidget::hover {
                background-color: #e0e0e0;
            }
        ''')

        self.setToolTip(tooltip)

        self.layout = QGridLayout(self)

        self.label = QLabel(self)
        self.label.setStyleSheet('background-color: transparent;')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label, 0, 0)

        self.text = QLabel(tooltip, self)
        self.text.setStyleSheet('background-color: transparent;')
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if icon != None:
            self.displayIcon = qtawesome.icon(icon, color='black').pixmap(QSize(48, 48))
            self.label.setPixmap(self.displayIcon)
            self.layout.addWidget(self.text, 1, 0)
        else:
            self.label.hide()
            self.text.setStyleSheet('font-size: 20px;')
            self.layout.addWidget(self.text, 0, 0)
        
        if options != None:
            self.clicked.connect(self.showMenu)
            self.options = options
            self.addMenuOption()

    def addMenuOption(self):
        self.menu = QMenu(self)
        self.menu.setFixedWidth(200)
        self.menu.setStyleSheet('''
            QMenu {
                border: 2px solid #d0d0d0;
            }
            QMenu::item {
                background-color: #f0f0f0;
                font-size: 20px;
            }

            QMenu::item:selected {
                background-color: #e0e0e0;
                color: black;
            }
        ''')

        for option in self.options:
            action = self.menu.addAction(option[0])

            icon = QIcon(qtawesome.icon(option[1], color='black').pixmap(QSize(40, 40)))
            action.setIcon(icon)
            
            action.triggered.connect(option[2])

    
    def showMenu(self):
       self.menu.exec(self.mapToGlobal(self.rect().bottomLeft()))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)
    
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
