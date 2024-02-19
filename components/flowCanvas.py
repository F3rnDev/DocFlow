from PyQt6.QtWidgets import QWidget, QApplication, QHBoxLayout, QStyleOption, QStyle
from PyQt6.QtGui import QMouseEvent, QPainter
from PyQt6.QtCore import QRect, QPoint, Qt
from components.flowStep import FlowStep, FlowStatus
from PIL import Image
import os

class FlowCanvas(QWidget):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, 10000, 10000))

        self.selectedStep = 0

        self.setStyleSheet('background-color: #ffffff;')

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(30)

        self.drag = QPoint()

        self.resetCanvasPosition()
    
    def resetCanvasPosition(self):
        screenGeometry = QApplication.primaryScreen().geometry()
        flowX = (screenGeometry.width() - self.width()) // 2
        flowY = (screenGeometry.height() - self.height()) // 2
        self.move(flowX, flowY)
    
    def onStepClick(self, id):
        self.selectedStep = id
        self.updateFlow(self.parent().project.getFlow())

    def exportImages(self, path):
        flowFolder = os.path.join(path, 'flow_images')
        os.makedirs(flowFolder, exist_ok=True)

        for i in range(self.layout.count()):
            step = self.layout.itemAt(i).widget()
            if isinstance(step, FlowStep):
                self.saveImg(step, i, flowFolder)
    
    def saveImg(self, widget, i, path):
        for status in FlowStatus:
            widget.setStatus(status)
            img = Image.fromqpixmap(widget.generateImage())
            img.save(os.path.join(path, f'flowStep{i}_{status.name}.png'))

            print(img.size)
        
    
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
    

    def updateFlow(self, flow):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        for stepId, step in enumerate(flow, start=0):
            self.addFlowStep(stepId, step, flow)      
            self.layout.itemAt(stepId).widget().clicked.connect(self.onStepClick)
        
        if flow.__len__() > 0 and self.selectedStep < flow.__len__():
            self.layout.itemAt(self.selectedStep).widget().setSelected(True)
            self.parent().loadStepInfo(self.selectedStep)
        else:
            self.parent().loadStepInfo(None)
    
    def addFlowStep(self, stepId, step, flow):
        if stepId == flow.__len__() - 1:
            self.layout.addWidget(FlowStep(step.name, step.icon, stepId))
        else:
            self.layout.addWidget(FlowStep(step.name, step.icon, stepId, True))

    #moving the flow canvas
    def mousePressEvent(self, event: QMouseEvent):
        self.drag = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if not self.drag.isNull():
            position = event.globalPosition().toPoint() - self.drag

            limitX = [-2000, -6000]
            limitY = [-3950, -5000]

            move_x = max(limitX[1], min(position.x(), limitX[0]))
            move_y = max(limitY[1], min(position.y(), limitY[0]))

            new_position = QPoint(move_x, move_y)

            self.move(new_position)
    
    def mouseReleaseEvent(self, event):
        self.drag = QPoint()