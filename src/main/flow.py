class Flow: 
    def __init__(self):
        self.steps = []

    def addStep(self):
        self.steps.append(Step("Etapa", 'fa5s.cog'))
    
    def deleteStep(self, index):
        if index < self.steps.__len__():
            self.steps.pop(index)
        else:
            print('Index out of range')

    def exportFlow(self, name):
        exportData = {"name": name, "flow": []}

        for step in self.steps:
            exportData["flow"].append([step.name, step.icon])
        
        return exportData

    def importFlow(self, data):
        self.steps = []

        for step in data["flow"]:
            self.steps.append(Step(step[0], step[1]))

class Step:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
    
    def setName(self, name):
        self.name = name
    
    def setIcon(self, icon):
        self.icon = icon
        