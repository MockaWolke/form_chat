from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass
@dataclass
class FormField:
    validation_func : callable
    question_in_chat : str
    value : Optional[Any] = None


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