from PyQt6.QtGui import QPixmap

class Flow:
    def __init__(self):
        self.flow = []
    
    def addStep(self):
        self.flow.append(Step("default", QPixmap('assets/defaultIcon.png')))
    
    def deleteStep(self):
        if self.flow.__len__() > 0:
            self.flow.pop(self.flow.__len__() - 1)

class Step:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
    
    def setName(self, name):
        self.name = name
    
    def setIcon(self, icon):
        self.icon = icon
        