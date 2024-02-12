from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog
from components.flowCanvas import FlowCanvas
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
    
    def addFlowStep(self):
        self.loadedFlow.addStep()
        self.flow.updateFlow(self.loadedFlow)
    
    def removeFlowStep(self):
        self.loadedFlow.deleteStep()
        self.flow.updateFlow(self.loadedFlow)
    
    def openExportWindow(self):
        docFile = None

        if self.loadedFlow.flow.__len__() > 0:
            docFile = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para exportar as imagens')
        
        if docFile:
            self.flow.exportImages(docFile)

