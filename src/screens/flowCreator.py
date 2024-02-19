from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog, QLineEdit, QLabel
from PyQt6.QtCore import QCoreApplication
from components.flowCanvas import FlowCanvas
from src.main.project import Project
from components.window import Window
from src.main.screenManager import ScreenManager as manager

class FlowCreator(QWidget):
    project = Project()

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.flow = FlowCanvas(self)

        self.displayName = QLabel(self.project.name, self)
        self.displayName.setGeometry(100, 150, 200, 50)

        addFlowBtn = QPushButton('Adicionar Etapa', self)
        addFlowBtn.setGeometry(100, 20, 200, 50)
        addFlowBtn.clicked.connect(self.addFlowStep)

        newProjectBtn = QPushButton('Novo Projeto', self)
        newProjectBtn.setGeometry(100, 80, 200, 50)
        newProjectBtn.clicked.connect(self.newProject)
        
        saveFlowBtn = QPushButton('Salvar Fluxo', self)
        saveFlowBtn.setGeometry(300, 80, 200, 50)
        saveFlowBtn.clicked.connect(self.saveFlow)

        openFlowBtn = QPushButton('Abrir Fluxo', self)
        openFlowBtn.setGeometry(700, 80, 200, 50)
        openFlowBtn.clicked.connect(self.openFlow)

        saveAsFlowBtn = QPushButton('Salvar Como', self)
        saveAsFlowBtn.setGeometry(500, 80, 200, 50)
        saveAsFlowBtn.clicked.connect(self.saveAsFlow)

        removeFlowBtn = QPushButton('Remover Etapa', self)
        removeFlowBtn.setGeometry(300, 20, 200, 50)
        removeFlowBtn.clicked.connect(self.removeFlowStep)

        exportBtn = QPushButton('Exportar Imagens', self)
        exportBtn.setGeometry(500, 20, 200, 50)
        exportBtn.clicked.connect(self.openExportWindow)

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
    
    def loadStepInfo(self, stepId: int):
        if stepId == None:
            self.stepName.setDisabled(True)
            self.iconBttn.setDisabled(True)
            self.stepName.setText('')
        else:
            self.stepName.setDisabled(False)
            self.iconBttn.setDisabled(False)
            self.stepName.setText(self.project.getFlow()[stepId].name)
    
    def updateStepInfo(self):
        if self.project.getFlow().__len__() > 0 and self.flow.selectedStep < self.project.getFlow().__len__():
            self.project.getFlow()[self.flow.selectedStep].setName(self.stepName.text())
            self.flow.layout.itemAt(self.flow.selectedStep).widget().setName(self.stepName.text())
    
    def addFlowStep(self):
        self.project.flow.addStep()
        self.flow.updateFlow(self.project.getFlow())
    
    def removeFlowStep(self):
        self.project.flow.deleteStep(self.flow.selectedStep)
        self.flow.updateFlow(self.project.getFlow())
    
    def openFlow(self):
        self.project.open()
        self.flow.updateFlow(self.project.getFlow())
        self.displayName.setText(self.project.name)
    
    def saveFlow(self):
        self.project.saveControl()
        self.displayName.setText(self.project.name)
    
    def saveAsFlow(self):
        self.project.saveAs()
        self.displayName.setText(self.project.name)
    
    def newProject(self):
        self.project.new()
        self.flow.updateFlow(self.project.getFlow())
        self.displayName.setText(self.project.name)
    
    def openIconPicker(self):
        self.iconWindow = Window(manager().getScreen("IconSelector"), "Selecione um ícone", 700, 700, True)
        self.iconWindow.show()
        self.iconWindow.content.selectItem.connect(self.updateStepIcon)
    
    def updateStepIcon(self, icon: str):
        self.project.getFlow()[self.flow.selectedStep].setIcon(icon)
        self.flow.updateFlow(self.project.getFlow())
    
    def openExportWindow(self):
        docFile = None

        if self.project.getFlow().__len__() > 0:
            docFile = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para exportar as imagens')
        
        if docFile:
            self.flow.exportImages(docFile)