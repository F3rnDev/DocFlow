from PyQt6.QtGui import QCloseEvent, QResizeEvent
from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog, QLineEdit, QLabel, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from components.toolBar import ToolBarOptions
from components.flowCanvas import FlowCanvas
from components.sideBar import SideBar
from src.main.project import Project
import qtawesome

class FlowCreator(QWidget):
    project = Project()

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setGeometry(0, 0, 1920, 1080)

        self.flow = FlowCanvas(self)
        #---------------------delete later---------------------
        resetCanvasBtn = QPushButton('Resetar Posição do Fluxo', self)
        resetCanvasBtn.setGeometry(700, 20, 200, 50)
        resetCanvasBtn.clicked.connect(self.flow.resetCanvasPosition)
        #---------------------END delete later---------------------
        self.toolbar = QWidget(self)
        self.toolbar.setGeometry(0, 0, 1920, 180)

        toolbarLayout = QVBoxLayout(self.toolbar)
        self.toolbar.setLayout(toolbarLayout)
        toolbarLayout.setContentsMargins(0, 0, 0, 0)
        toolbarLayout.setSpacing(0)

        self.proj = QWidget(self)
        self.proj.setGeometry(0, 0, 1920, 50)
        self.proj.setStyleSheet(''' background-color: #ffffff; border: none;''')
        toolbarLayout.addWidget(self.proj)

        projLayout = QHBoxLayout(self.proj)
        self.proj.setLayout(projLayout)
        projLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        projLayout.setContentsMargins(20, 10, 0, 0)

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

        self.toolBarOpt = ToolBarOptions(self)
        toolbarLayout.addWidget(self.toolBarOpt)

        self.sideBar = SideBar(self)

        #---------------------delete later---------------------
        self.languagePicker = QComboBox(self)
        self.languagePicker.setGeometry(900, 20, 200, 50)
        self.languagePicker.currentIndexChanged.connect(self.flow.changeLanguage)
        self.languagePicker.hide()
        for lang in self.project.languages:
            self.languagePicker.addItem(lang.cur.name)
        #---------------------END delete later---------------------
    
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.toolbar.resize(self.width(), 180)
        self.flow.resetCanvasPosition()

        self.sideBar.responsiveResize(self.width(), self.height(), self.toolbar.height())
    
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