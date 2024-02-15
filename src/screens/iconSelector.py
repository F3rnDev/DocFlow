from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QPushButton, QLineEdit
from PyQt6.QtCore import pyqtSignal
import qtawesome

class IconSelector(QWidget):
    selectItem = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(0, 50, 700, 650)

        qtawesome._instance()
        fontMaps = qtawesome._resource['iconic'].charmap

        self.iconNames = []
        for fontCollection, fontData in fontMaps.items():
            for iconName in fontData:
                self.iconNames.append('%s.%s' % (fontCollection, iconName))
            
        for iconName in self.iconNames:
            item = QListWidgetItem(iconName)
            item.setIcon(qtawesome.icon(iconName, color='black'))
            self.list_widget.addItem(item)

        confirmBtn = QPushButton('Confirmar', self)
        confirmBtn.setGeometry(310, 0, 100, 40)
        confirmBtn.clicked.connect(self.confirmIcon)

        cancelBtn = QPushButton('Cancelar', self)
        cancelBtn.setGeometry(410, 0, 100, 40)
        cancelBtn.clicked.connect(self.closeWindow)

        searchBar = QLineEdit(self)
        searchBar.setGeometry(10, 0, 300, 40)
        searchBar.setPlaceholderText('Pesquisar ícone')
        searchBar.textChanged.connect(self.searchIcon)

    def confirmIcon(self):
        self.selectItem.emit(self.list_widget.currentItem().text())
        self.closeWindow()
    
    def closeWindow(self):
        self.parent().closeWindow()
    
    def searchIcon(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)