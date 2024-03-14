from PyQt6.QtGui import QCloseEvent, QResizeEvent
from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog, QLineEdit, QLabel, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from components.toolBar import ToolBarOptions
from components.flowCanvas import FlowCanvas
from components.sideBar import SideBar
from src.main.project import Project
from components.window import Window
from src.main.screenManager import ScreenManager as manager

class FlowCreator(QWidget):
    project = Project()

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setGeometry(0, 0, 1920, 1080)

        self.flow = FlowCanvas(self)

        #---------------------delete later---------------------
        removeFlowBtn = QPushButton('Remover Etapa', self)
        removeFlowBtn.setGeometry(300, 20, 200, 50)
        removeFlowBtn.clicked.connect(self.removeFlowStep)

        resetCanvasBtn = QPushButton('Resetar Posição do Fluxo', self)
        resetCanvasBtn.setGeometry(700, 20, 200, 50)
        resetCanvasBtn.clicked.connect(self.flow.resetCanvasPosition)

        self.stepName = QLineEdit(self)
        self.stepName.setDisabled(True)
        self.stepName.setGeometry(1200, 20, 200, 50)
        self.stepName.setPlaceholderText('Nome da Etapa')
        self.stepName.textEdited.connect(self.updateStepInfo)

        self.iconBttn = QPushButton('Icone', self)
        self.iconBttn.setDisabled(True)
        self.iconBttn.setGeometry(1400, 20, 200, 50)
        self.iconBttn.clicked.connect(self.openIconPicker)

        self.languagePicker = QComboBox(self)
        self.languagePicker.setGeometry(900, 20, 200, 50)
        self.languagePicker.currentIndexChanged.connect(self.flow.changeLanguage)

        for lang in self.project.languages:
            self.languagePicker.addItem(lang.cur.name)
        # addFlowBtn = QPushButton('Adicionar Etapa', self)
        # addFlowBtn.setGeometry(100, 20, 200, 50)
        # addFlowBtn.clicked.connect(self.addFlowStep)

        # newProjectBtn = QPushButton('Novo Projeto', self)
        # newProjectBtn.setGeometry(100, 80, 200, 50)
        # newProjectBtn.clicked.connect(self.newProject)
        
        # saveFlowBtn = QPushButton('Salvar Fluxo', self)
        # saveFlowBtn.setGeometry(300, 80, 200, 50)
        # saveFlowBtn.clicked.connect(self.saveFlow)

        # openFlowBtn = QPushButton('Abrir Fluxo', self)
        # openFlowBtn.setGeometry(700, 80, 200, 50)
        # openFlowBtn.clicked.connect(self.openFlow)

        # saveAsFlowBtn = QPushButton('Salvar Como', self)
        # saveAsFlowBtn.setGeometry(500, 80, 200, 50)
        # saveAsFlowBtn.clicked.connect(self.saveAsFlow)

        # exportBtn = QPushButton('Exportar Imagens', self)
        # exportBtn.setGeometry(500, 20, 200, 50)
        # exportBtn.clicked.connect(self.openExportWindow)
        
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

        # self.stepInfoUI = StepFlowInfo(self)
        # toolbarLayout.addWidget(self.stepInfoUI)
    
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.toolbar.resize(self.width(), 180)
        self.flow.resetCanvasPosition()

        self.sideBar.responsiveResize(self.width(), self.height(), self.toolbar.height())
    
    def loadStepInfo(self, stepId: int):
        if stepId == None:
            self.stepName.setDisabled(True)
            self.iconBttn.setDisabled(True)
            self.stepName.setText('')
        else:
            self.stepName.setDisabled(False)
            self.iconBttn.setDisabled(False)
            self.stepName.setText(self.project.getFlowSteps(self.flow.curLang)[stepId].name)
    
    def updateStepInfo(self):
        if self.project.getFlowSteps(self.flow.curLang).__len__() > 0 and self.flow.selectedStep < self.project.getFlowSteps(self.flow.curLang).__len__():
            self.project.getFlowSteps(self.flow.curLang)[self.flow.selectedStep].setName(self.stepName.text())
            self.flow.layout.itemAt(self.flow.selectedStep).widget().setName(self.stepName.text())
    
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
    
    def openIconPicker(self):
        self.iconWindow = Window(manager().getScreen("IconSelector"), "Selecione um ícone", 700, 700, True)
        self.iconWindow.show()
        self.iconWindow.content.selectItem.connect(self.updateStepIcon)
    
    def updateStepIcon(self, icon: str):
        self.project.setIcons(self.flow.selectedStep, icon)
        self.project.getFlowSteps(self.flow.curLang)[self.flow.selectedStep].setIcon(icon)
        self.flow.updateFlow(self.project.getFlowSteps(self.flow.curLang))


    
    def openExportWindow(self):
        docFile = None

        if self.project.getFlowSteps(self.flow.curLang).__len__() > 0:
            docFile = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para exportar as imagens')
        
        if docFile:
            self.flow.exportImages(docFile)