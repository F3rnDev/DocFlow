from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog, QLineEdit
from PyQt6.QtCore import QCoreApplication
from components.flowCanvas import FlowCanvas
from src.main.flow import Flow
from components.window import Window
from src.main.screenManager import ScreenManager as manager

class FlowCreator(QWidget):
    loadedFlow = Flow()

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.flow = FlowCanvas(self)

        addFlowBtn = QPushButton('Adicionar Etapa', self)
        addFlowBtn.setGeometry(100, 20, 200, 50)
        addFlowBtn.clicked.connect(self.addFlowStep)

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
            self.stepName.setText(self.loadedFlow.flow[stepId].name)
    
    def updateStepInfo(self):
        if self.loadedFlow.flow.__len__() > 0 and self.flow.selectedStep < self.loadedFlow.flow.__len__():
            self.loadedFlow.flow[self.flow.selectedStep].setName(self.stepName.text())
            self.flow.layout.itemAt(self.flow.selectedStep).widget().setName(self.stepName.text())
    
    def addFlowStep(self):
        self.loadedFlow.addStep()
        self.flow.updateFlow(self.loadedFlow)
    
    def removeFlowStep(self):
        self.loadedFlow.deleteStep(self.flow.selectedStep)
        self.flow.updateFlow(self.loadedFlow)
    
    def openIconPicker(self):
        self.iconWindow = Window(manager().getScreen("IconSelector"), "Selecione um ícone", 700, 700, True)
        self.iconWindow.show()
        self.iconWindow.content.selectItem.connect(self.updateStepIcon)
    
    def updateStepIcon(self, icon: str):
        self.loadedFlow.flow[self.flow.selectedStep].setIcon(icon)
        self.flow.updateFlow(self.loadedFlow)
    
    def openExportWindow(self):
        docFile = None

        if self.loadedFlow.flow.__len__() > 0:
            docFile = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para exportar as imagens')
        
        if docFile:
            self.flow.exportImages(docFile)
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        QCoreApplication.quit()
        QCoreApplication.exit()

