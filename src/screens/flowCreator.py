from PyQt6.QtWidgets import QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
from components.flowStep import FlowStep
from PyQt6.QtGui import QPixmap, QColor, QPainter, QResizeEvent
from PIL import Image
from PyQt6.QtCore import QRect
from src.main.flow import Flow

class FlowCreator(QWidget):
    loadedFlow = Flow()

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.flow = QWidget(self)
        self.flow.setGeometry(QRect(0, 0, 1920, 1080))
        self.flow.setStyleSheet('background-color: #ffffff;')

        addFlowBtn = QPushButton('Adicionar Etapa', self)
        addFlowBtn.setGeometry(100, 20, 200, 50)
        addFlowBtn.clicked.connect(self.addFlowStep)

        removeFlowBtn = QPushButton('Remover Etapa', self)
        removeFlowBtn.setGeometry(300, 20, 200, 50)
        removeFlowBtn.clicked.connect(self.removeFlowStep)

        exportBtn = QPushButton('Exportar Imagens', self)
        exportBtn.setGeometry(500, 20, 200, 50)
        exportBtn.clicked.connect(self.exportImages)
        
        self.flowLayout = QHBoxLayout(self.flow)
        self.flowLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowLayout.setSpacing(30)
        
    
    def updateFlow(self):
        while self.flowLayout.count():
            item = self.flowLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for stepId, step in enumerate(self.loadedFlow.flow, start=0):
            if stepId == self.loadedFlow.flow.__len__() - 1:
                self.flowLayout.addWidget(FlowStep(step.name, step.icon))
            else:
                self.flowLayout.addWidget(FlowStep(step.name, step.icon, True))
    
    def addFlowStep(self):
        self.loadedFlow.addStep()
        self.updateFlow()
    
    def removeFlowStep(self):
        self.loadedFlow.deleteStep()
        self.updateFlow()
    
    def exportImages(self):
        for i in range(self.flowLayout.count()):
            step = self.flowLayout.itemAt(i).widget()

            if isinstance(step, FlowStep):
                img = Image.fromqpixmap(step.generateImage())
                img.save(f'flowStep{i}.png')

                print(img.size)
