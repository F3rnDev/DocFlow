from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog, QLineEdit
from components.flowCanvas import FlowCanvas
from components.flowStep import FlowStep
from src.main.flow import Flow

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
        self.stepName.textChanged.connect(self.updateStepInfo)
    
    def updateFlow(self, loadedFlow):
        while self.flow.layout.count():
            item = self.flow.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        for stepId, step in enumerate(loadedFlow.flow, start=0):
            if stepId == loadedFlow.flow.__len__() - 1:
                self.flow.layout.addWidget(FlowStep(step.name, step.icon, stepId))
            else:
                self.flow.layout.addWidget(FlowStep(step.name, step.icon, stepId, True))
            
            self.flow.layout.itemAt(stepId).widget().clicked.connect(self.flow.onStepClick)
        
        if self.loadedFlow.flow.__len__() > 0:
            self.flow.layout.itemAt(self.flow.selectedStep).widget().setSelected(True)
            self.loadStepInfo(self.flow.selectedStep)
        else:
            self.loadStepInfo(None)
    
    def loadStepInfo(self, stepId: int):
        if stepId == None:
            self.stepName.setDisabled(True)
            self.stepName.setText('')
        else:
            self.stepName.setDisabled(False)
            self.stepName.setText(self.loadedFlow.flow[stepId].name)
    
    def updateStepInfo(self):
        if self.loadedFlow.flow.__len__() > 0:
            self.loadedFlow.flow[self.flow.selectedStep].setName(self.stepName.text())
            self.flow.layout.itemAt(self.flow.selectedStep).widget().setName(self.stepName.text())
    
    def addFlowStep(self):
        self.loadedFlow.addStep()
        self.updateFlow(self.loadedFlow)
    
    def removeFlowStep(self):
        self.loadedFlow.deleteStep(self.flow.selectedStep)
        self.updateFlow(self.loadedFlow)
    
    def openExportWindow(self):
        docFile = None

        if self.loadedFlow.flow.__len__() > 0:
            docFile = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para exportar as imagens')
        
        if docFile:
            self.flow.exportImages(docFile)

