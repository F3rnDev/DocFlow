from PyQt6.QtWidgets import QWidget, QApplication, QHBoxLayout
from PyQt6.QtGui import QMouseEvent, QPalette, QColor
from PyQt6.QtCore import QRect, QPoint, Qt
from components.flowStep import FlowStep
from PIL import Image
import os

class FlowCanvas(QWidget):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, 10000, 10000))

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

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
    
    def updateFlow(self, loadedFlow):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for stepId, step in enumerate(loadedFlow.flow, start=0):
            if stepId == loadedFlow.flow.__len__() - 1:
                self.layout.addWidget(FlowStep(step.name, step.icon))
            else:
                self.layout.addWidget(FlowStep(step.name, step.icon, True))

    def exportImages(self, path):
        flowFolder = os.path.join(path, 'flow_images')
        os.makedirs(flowFolder, exist_ok=True)

        for i in range(self.layout.count()):
            step = self.layout.itemAt(i).widget()

            if isinstance(step, FlowStep):
                img = Image.fromqpixmap(step.generateImage())
                img.save(os.path.join(flowFolder, f'flowStep{i}.png'))

                print(img.size)
    
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