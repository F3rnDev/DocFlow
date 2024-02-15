from enum import Enum

class Screen(Enum):
    FlowCreator = 0
    IconSelector = 1

class ScreenManager:
    def getScreen(self, screen):
        match Screen[screen]:
            case Screen.FlowCreator:
                from src.screens.flowCreator import FlowCreator
                return FlowCreator()
            case Screen.IconSelector:
                from src.screens.iconSelector import IconSelector
                return IconSelector()