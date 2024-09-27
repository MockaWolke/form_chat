from .interfaces import FormFormatInterface, FormField
from typing import Any


class FormFormat(FormFormatInterface):
    
    def __init__(self, name : str, description : str, fields : dict[str, FormField]) -> None:
        super().__init__()
    
        self.name : str = name
        self.desc = description
        self.fields = fields
        self.filled = set()
    
    def fill_value(self, name : str, val : Any) -> None | str:
        
        if name not in self.fields:
            raise ValueError("name not in fields")
        
        try:
            
            val = self.fields[name].validation_func(val)
            self.fields[name].value = val
        except ValueError as e:
            return str(e)
    
        self.filled.add(name)
    
        return None
    
    @property
    def missing_values(self) -> list[str]:
        return [i for i in self.fields if i not in self.filled]
    
    
    @property
    def filled_values(self) -> set[str]:
        return self.filled
    
    @property
    def description(self) -> str:
        return self.desc
    
    def __str__(self) -> str:
        # Nicely format the filled-out values for printing
        filled_out = []
        for field in self.filled:
            filled_out.append(f"{field}: {self.fields[field].val}")
        if not filled_out:
            return "No fields have been filled yet."
        return f"Form: {self.name}\n" + "\n".join(filled_out)