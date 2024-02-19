from enum import Enum
from src.main.flow import Flow

class allLanguages(Enum):
    PORTUGUESE = "por"
    ENGLISH = "eng"
    SPANISH = "spa"

class Language:
    def __init__(self, defaultLanguage):
        self.cur = defaultLanguage
        self.flow = Flow()