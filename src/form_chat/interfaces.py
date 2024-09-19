from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import List, Any

class Speaker(Enum):
    USER = "user"
    BOT = "bot"


@dataclass
class MessageHistoryItem:
    speaker: Speaker
    message: str


class CHAT_LLM_Interface(ABC):

    @abstractmethod
    def compute_response(self, message: str, instruction: str, history: List[MessageHistoryItem] = list()) -> str:
        pass

class FormFormat(ABC):
    
    @abstractmethod
    def fill_value(self, name : str, val : Any) -> None | str:
        pass
    
    @abstractmethod
    @property
    def missing_values(self) -> list[str]:
        pass
    
    
    @abstractmethod
    @property
    def filled_values(self) -> list[str]:
        pass
    
    @abstractmethod
    @property
    def description(self) -> str:
        pass
    
    
class ConversationalManagerInterface(ABC):
    pass
    

class FormDataBaseInterface(ABC):
    
    @abstractmethod
    def refill_database(self):
        pass
    
    @abstractmethod
    def find_form(self, str) -> FormFormat:
        pass