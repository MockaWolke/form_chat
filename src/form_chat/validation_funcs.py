"""
This module includes validation functions for different form fields.
Each function returns the validated value or raises a ValueError with a
clear message for the frontend if the input is invalid.
"""

from datetime import datetime
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

# Race Validierung (Nur Buchstaben)
def validate_race(race: str) -> str:
    if not race.isalpha():
        raise ValueError("Please enter a valid dog breed.")
    return race

# Mikrochip Validierung (Nummer aus 15 stellen)
def validate_microchipnumber(microchipnumber: str) -> str:
    if not (microchipnumber.isdigit() and len(microchipnumber) == 15):
        raise ValueError(f"Please enter the microchip number of your dog (15 digits) {len(microchipnumber)}")
    return microchipnumber

# Hunde Haltungsdatum
def validate_Date(date: str) -> str:
    try:
        date = datetime.strptime(date.strip(), "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Could not parse Date. Please use DD.MM.YYYY format.")
    return date