from src.main.flow import Flow
from PyQt6.QtWidgets import QFileDialog
import json
import os

class Project:
    def __init__(self):
        self.new()
    
    def new(self):
        self.flow = Flow()
        self.file = None
        self.name = 'Novo Projeto'
    
    def getFlow(self):
        return self.flow.steps
    
    def open(self):
        docFile = QFileDialog.getOpenFileName(None, 'Abrir Fluxo', '', 'Docflow File (*.docflow);;Todos os Arquivos (*)')
        
        if docFile and docFile.__len__() > 0 and docFile[0] != '':
            with open (docFile[0], 'r') as file:
                data = json.load(file)
                self.flow.importFlow(data)
                self.file = docFile[0]
                self.name = data['name']
    
    def saveControl(self):
        if self.file == None:
            self.saveAs()
        else:
            self.save(self.name, self.file)
    
    def save(self, saveName, filePath):
        data = self.flow.exportFlow(saveName)

        with open (filePath, 'w') as file:
            json.dump(data, file)
            self.name = saveName
            self.file = filePath
    
    def saveAs(self):
        docFile = QFileDialog.getSaveFileName(None, 'Salvar Fluxo', self.name, 'Docflow File (*.docflow);;Todos os Arquivos (*)')
        
        if docFile and docFile.__len__() > 0 and docFile[0] != '':
            self.save(os.path.basename(docFile[0]).split('.')[0], docFile[0])