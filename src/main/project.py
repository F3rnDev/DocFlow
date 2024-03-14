from PyQt6.QtWidgets import QFileDialog
from src.main.language import Language, allLanguages
import json
import os

class Project:
    def __init__(self):
        self.new()
    
    def new(self):
        self.file = None
        self.name = 'Novo Projeto'

        self.languages = []

        for language in allLanguages:
            self.languages.append(Language(language))
    
    def setName(self, name):
        self.name = name
        print(self.name)
    
    def addSteps(self):
        for language in self.languages:
            language.flow.addStep()
    
    def deleteSteps(self, index):
        for language in self.languages:
            language.flow.deleteStep(index)
    
    def setIcons(self, index, icon):
        for language in self.languages:
            language.flow.steps[index].setIcon(icon)
    
    def getFlowSteps(self, selectedLanguage):
        return self.languages[selectedLanguage].flow.steps

    def getFlow(self, selectedLanguage):
        return self.languages[selectedLanguage].flow
    
    def open(self):
        docFile = QFileDialog.getOpenFileName(None, 'Abrir Fluxo', '', 'Docflow File (*.docflow);;Todos os Arquivos (*)')
        
        if docFile and docFile.__len__() > 0 and docFile[0] != '':
            with open (docFile[0], 'r') as file:
                data = json.load(file)
                self.file = docFile[0]
                self.name = data['name']
                self.importSteps(data)
    
    def importSteps(self, data):
        for language in self.languages:
            
            if language.cur.value in data:
                language.flow.importFlow(data[language.cur.value])
            else:
                language.flow.importFlow([])
    
    def saveControl(self):
        if self.file == None:
            self.saveAs()
        else:
            self.save(self.name, self.file)
    
    def save(self, saveName, filePath):
        data = {"name": self.name}

        for language in self.languages:
            data[language.cur.value] = language.flow.exportFlow()

        with open (filePath, 'w') as file:
            json.dump(data, file)
            self.file = filePath
    
    def saveAs(self):
        docFile = QFileDialog.getSaveFileName(None, 'Salvar Fluxo', self.name, 'Docflow File (*.docflow);;Todos os Arquivos (*)')
        
        if docFile and docFile.__len__() > 0 and docFile[0] != '':
            self.save(os.path.basename(docFile[0]).split('.')[0], docFile[0])