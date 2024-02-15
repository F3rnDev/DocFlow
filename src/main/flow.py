from PyQt6.QtGui import QPixmap
import qtawesome

class Flow:
    def __init__(self):
        self.flow = []
    
    def addStep(self):
        self.flow.append(Step("default", 'fa5s.cog'))
    
    def deleteStep(self, index):
        if index < self.flow.__len__():
            self.flow.pop(index)
        else:
            print('Index out of range')

class Step:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
    
    def setName(self, name):
        self.name = name
    
    def setIcon(self, icon):
        self.icon = icon
        