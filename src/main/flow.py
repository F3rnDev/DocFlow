from PyQt6.QtGui import QPixmap
from src.main.resource import Resource

class Flow:
    def __init__(self):
        self.flow = []
    
    def addStep(self):
        defaultIcon = Resource.resource_path('assets/defaultIcon.png')
        self.flow.append(Step("default", QPixmap(defaultIcon)))
    
    def deleteStep(self, index):
        self.flow.pop(index)

class Step:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
    
    def setName(self, name):
        self.name = name
    
    def setIcon(self, icon):
        self.icon = icon
        