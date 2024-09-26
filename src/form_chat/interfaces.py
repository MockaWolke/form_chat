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

class FormFormatInterface(ABC):
    
    @abstractmethod
    def fill_value(self, name : str, val : Any) -> None | str:
        pass
    
    @property
    @abstractmethod
    def missing_values(self) -> set[str]:
        pass
    
    
    @property
    @abstractmethod
    def filled_values(self) -> set[str]:
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        pass
    
    
class ConversationalManagerInterface(ABC):
    pass
    

class FormDataBaseInterface(ABC):
    
    @abstractmethod
    def refill_database(self):
        pass
    
    @abstractmethod
    def find_form(self, str) -> FormFormatInterface:
        pass
    
    @property
    @abstractmethod
    def all_forms(self, str) -> list[FormFormatInterface]:
        pass