from .interfaces import FormFormatInterface, FormField
from datetime import datetime, date
from typing import Any
from dataclasses import dataclass
import re


def validate_name(string: str) -> str:
    string = string.strip().title()
    if len(string) < 3:
        raise ValueError("The name is too short!")
    return string

# Geburtstag Validierung
def validate_birthday(birth_day: str, min_year: int = 2004) -> datetime:
    try:
        birth_day = datetime.strptime(birth_day.strip(), "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Could not parse Date. Please use DD.MM.YYYY format.")
    
    if birth_day.year > min_year:
        raise ValueError("You are not old enough!")
    
    return birth_day

# Adresse Validierung (Straßenname mit Hausnummer)
def validate_address(address: str) -> str:
    if not re.match(r"[A-Za-zÄÖÜäöüß\s]+\s\d+[a-zA-ZÄÖÜäöüß]?", address.strip()):
        raise ValueError("Invalid address format. Use 'Streetname Housenumber' format.")
    return address.strip()

# Postleitzahl Validierung
def validate_postal_code(postal_code: str) -> str:
    if len(postal_code) != 5 or not postal_code.isdigit():
        raise ValueError("Postcode must be exactly 5 digits.")
    return postal_code


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