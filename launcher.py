from PyQt6.QtWidgets import QApplication
from src.main.screenManager import ScreenManager as manager
from components.window import Window

appName = "DocFlow"
appVersion = "0.0.1"
defaultTitle = f"{appName} {appVersion}"
windowSize = [1920 , 1080]

def startApplication():
    app = QApplication([])

    main = Window(manager().getScreen("FlowCreator"), defaultTitle, windowSize[0], windowSize[1])
    main.showMaximized()
    main.show()

    app.exec()

startApplication()



