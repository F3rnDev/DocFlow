from enum import Enum
from src.screens.flowCreator import FlowCreator

class Screen(Enum):
    FlowCreator = 0

class ScreenManager:
    def getScreen(self, screen):
        match Screen[screen]:
            case Screen.FlowCreator:
                return FlowCreator()