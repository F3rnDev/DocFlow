import os
from PyQt6.QtGui import QMouseEvent, QResizeEvent
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QApplication, QFileDialog
from PyQt6.QtCore import Qt, QRect, QPoint
from components.flowStep import FlowStep
from components.flowCanvas import FlowCanvas
from PIL import Image
from src.main.flow import Flow

class FlowCreator(QWidget):
    loadedFlow = Flow()

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.flow = QWidget(self)
        self.flow.setGeometry(QRect(0, 0, 10000, 10000))
        self.flow.setStyleSheet('background-color: #ffffff;')

        screenGeometry = QApplication.primaryScreen().geometry()
        flowX = (screenGeometry.width() - self.flow.width()) // 2
        flowY = (screenGeometry.height() - self.flow.height()) // 2
        self.flow.move(flowX, flowY)

        self.flowLayout = QHBoxLayout(self.flow)
        self.flowLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flowLayout.setSpacing(30)

        self.drag = QPoint()

        addFlowBtn = QPushButton('Adicionar Etapa', self)
        addFlowBtn.setGeometry(100, 20, 200, 50)
        addFlowBtn.clicked.connect(self.addFlowStep)

        removeFlowBtn = QPushButton('Remover Etapa', self)
        removeFlowBtn.setGeometry(300, 20, 200, 50)
        removeFlowBtn.clicked.connect(self.removeFlowStep)

        exportBtn = QPushButton('Exportar Imagens', self)
        exportBtn.setGeometry(500, 20, 200, 50)
        exportBtn.clicked.connect(self.openExportWindow)
    
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
    
    def openExportWindow(self):
        docFile = None

        if self.flowLayout.count() > 0:
            docFile = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para exportar as imagens')
        
        if docFile:
            self.exportImages(docFile)
    
    def exportImages(self, path):
        flowFolder = os.path.join(path, 'flow_images')
        os.makedirs(flowFolder, exist_ok=True)

        for i in range(self.flowLayout.count()):
            step = self.flowLayout.itemAt(i).widget()

            if isinstance(step, FlowStep):
                img = Image.fromqpixmap(step.generateImage())
                img.save(os.path.join(flowFolder, f'flowStep{i}.png'))

                print(img.size)
    
    #moving the flow canvas
    def mousePressEvent(self, event: QMouseEvent):
        child_widget = self.childAt(event.pos())
        if child_widget and child_widget == self.flow and event.button() == Qt.MouseButton.LeftButton:
            self.drag = event.pos() - self.flow.pos()

    def mouseMoveEvent(self, event):
        if self.drag and not self.drag.isNull():
            new_position = event.pos() - self.drag

            limitX = [-2000, -6000]
            limitY = [-3950, -5000]

            move_x = max(limitX[1], min(new_position.x(), limitX[0]))
            move_y = max(limitY[1], min(new_position.y(), limitY[0]))

            self.flow.move(move_x, move_y)
    
    def mouseReleaseEvent(self, event):
        self.drag = QPoint()

