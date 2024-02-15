from PyQt6.QtGui import QPixmap
import qtawesome

class Flow:
    def __init__(self):
        self.flow = []
    
    def addStep(self):
        defaultIcon = qtawesome.icon('fa5s.cog', color='#174077')
        self.flow.append(Step("default", defaultIcon))
    
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
        newIcon = qtawesome.icon(icon, color='#174077')
        self.icon = newIcon
        