from PyQt6.QtGui import QCloseEvent, QResizeEvent, QIcon
from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog, QLineEdit, QLabel, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QSize, QPoint, QPropertyAnimation, QEasingCurve
from components.toolBar import ToolBarOptions
from components.flowCanvas import FlowCanvas
from components.sideBar import SideBar
from src.main.project import Project
from src.main.resource import Resource
import qtawesome

class FlowCreator(QWidget):
    project = Project()

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setGeometry(0, 0, 1920, 1080)

        #The background canvas
        self.flow = FlowCanvas(self)

        #The entire upper toolbar
        self.toolbar = QWidget(self)
        self.toolbar.setGeometry(0, 0, 1920, 180)

        toolbarLayout = QVBoxLayout(self.toolbar)
        self.toolbar.setLayout(toolbarLayout)
        toolbarLayout.setContentsMargins(0, 0, 0, 0)
        toolbarLayout.setSpacing(0)

        #The project name section of the toolbar
        self.proj = QWidget(self)
        self.proj.setGeometry(0, 0, 1920, 50)
        self.proj.setStyleSheet(''' background-color: #ffffff; border: none;''')
        toolbarLayout.addWidget(self.proj)

        projLayout = QHBoxLayout(self.proj)
        self.proj.setLayout(projLayout)
        projLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        projLayout.setContentsMargins(20, 10, 0, 0)

        #The project name input
        self.displayName = QLineEdit(self.project.name, self)
        self.displayName.setPlaceholderText('Nome do Projeto')
        self.displayName.setStyleSheet('''
            background-color: transparent;
            border: none;
            border-bottom: 2px solid #d0d0d0;
            font-size: 20px;
        ''')
        self.displayName.setFixedWidth(280)
        self.displayName.textEdited.connect(lambda: self.project.setName(self.displayName.text()))
        projLayout.addWidget(self.displayName)
        projLayout.addStretch(1)

        #The project toolbar options
        self.toolBarOpt = ToolBarOptions(self)
        toolbarLayout.addWidget(self.toolBarOpt)

        #The language picker
        self.languagePicker = QComboBox(self)
        self.languagePicker.setGeometry(20, 200, 110, 50)
        self.languagePicker.setIconSize(QSize(50, 50))

        downArrowPath = Resource.resource_path('assets/down-arrow.svg')
        downArrowPath = downArrowPath.replace('\\', '/')
        fullStykeSheet = """
            QComboBox {
                background-color: transparent;
                selection-background-color: transparent;
                selection-color: #000000;
                font-size: 15px;
                font-weight: bold;
                border-radius: 15px
            }
            QComboBox::hover {
                background-color: #d0d0d0;
                border: none;
            }
            QComboBox::drop-down{
                border: none;
                background-color: transparent;
                width: 15px;
                height: 50px;
                margin-left: 5px;
            }
            
            QComboBox::down-arrow{
                image: url('%1');
            }
        """
        self.languagePicker.setStyleSheet(fullStykeSheet.replace('%1', downArrowPath))
        for lang in self.project.languages:
            self.languagePicker.addItem(QIcon(Resource.resource_path(f"assets/flags/{lang.cur.value}.svg")), lang.cur.value.upper())
        
        #The stepInfo sideBar
        self.sideBar = SideBar(self)

        #Connect Language Picker, crashes if created before SideBar
        self.languagePicker.currentIndexChanged.connect(self.flow.changeLanguage)
            
        #Reset Canvas Position
        self.resetCanvasBtn = QPushButton('', self)
        self.resetCanvasBtn.setGeometry(0, 0, 80, 50)
        self.resetCanvasBtn.setIcon(qtawesome.icon('mdi6.fit-to-screen', color='black'))
        self.resetCanvasBtn.setIconSize(QSize(50, 50))
        self.resetCanvasBtn.clicked.connect(self.flow.resetCanvasPosition)

        #Connect the stepInfo sideBar to the resetCanvasBtn
        self.sideBar.collapseSignal.connect(self.moveResetBtn)
    
    def moveResetBtn(self, collapse: bool):
        if not collapse:
            self.animateResetBtn(self.resetCanvasBtn, self.width() - self.sideBar.widgetWidth - self.resetCanvasBtn.width(), 200)
        else:
            self.animateResetBtn(self.resetCanvasBtn, self.width() - self.sideBar.collapseArrow.width() - self.resetCanvasBtn.width(), 200)
    
    def animateResetBtn(self, obj, posx, posy):
        obj.animation = QPropertyAnimation(obj, b'pos')
        obj.animation.setDuration(300)
        obj.animation.setStartValue(QPoint(obj.x(), obj.y()))
        obj.animation.setEndValue(QPoint(posx, posy))
        obj.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        obj.animation.start()
    
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.toolbar.resize(self.width(), 180)
        self.flow.resetCanvasPosition()

        self.sideBar.responsiveResize(self.width(), self.height(), self.toolbar.height())
        self.resetCanvasBtn.setGeometry(self.sideBar.x() - 80, 200, 80, 50)
    
    def loadStepInfo(self, stepId: int):
        if stepId == None:
            self.sideBar.setDisabled(True)
            self.sideBar.toggleCollapse(True)
        else:
            self.sideBar.setDisabled(False)
            self.sideBar.stepInfoUI.setStepName(self.project.getFlowSteps(self.flow.curLang)[stepId].name)
            self.sideBar.stepInfoUI.setStepIcon(self.project.getFlowSteps(self.flow.curLang)[stepId].icon)
            self.sideBar.toggleCollapse(False)
    
    def addFlowStep(self):
        self.project.addSteps()
        self.flow.updateFlow(self.project.getFlowSteps(self.flow.curLang))
    
    def removeFlowStep(self):
        self.project.deleteSteps(self.flow.selectedStep)
        self.flow.updateFlow(self.project.getFlowSteps(self.flow.curLang))
    
    def openFlow(self):
        self.project.open()
        self.flow.updateFlow(self.project.getFlowSteps(self.flow.curLang))
        self.displayName.setText(self.project.name)
    
    def saveFlow(self):
        self.project.saveControl()
        self.displayName.setText(self.project.name)
    
    def saveAsFlow(self):
        self.project.saveAs()
        self.displayName.setText(self.project.name)
    
    def newProject(self):
        self.project.new()
        self.flow.updateFlow(self.project.getFlowSteps(self.flow.curLang))
        self.displayName.setText(self.project.name)
    
    def updateStepIcon(self, icon: str):
        self.project.setIcons(self.flow.selectedStep, icon)
        self.project.getFlowSteps(self.flow.curLang)[self.flow.selectedStep].setIcon(icon)
        self.flow.updateFlow(self.project.getFlowSteps(self.flow.curLang))
    
    def updateStepInfo(self, text: str):
        if self.project.getFlowSteps(self.flow.curLang).__len__() > 0 and self.flow.selectedStep < self.project.getFlowSteps(self.flow.curLang).__len__():
            self.project.getFlowSteps(self.flow.curLang)[self.flow.selectedStep].setName(text)
            self.flow.layout.itemAt(self.flow.selectedStep).widget().setName(text)
        
    def openExportWindow(self):
        docFile = None

        if self.project.getFlowSteps(self.flow.curLang).__len__() > 0:
            docFile = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para exportar as imagens')
        
        if docFile:
            self.flow.exportImages(docFile)