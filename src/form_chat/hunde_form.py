from .forms import *

# Define the fields for the dog registration form in German
dog_fields = {
    "name": FormField(validate_name, "Wie ist Ihr Name?"),
    "birthday": FormField(validate_birthday, "Was ist Ihr Geburtsdatum? (TT.MM.JJJJ)"),
    "address": FormField(validate_address, "Wie lautet Ihre Adresse? (Straßenname Hausnummer)"),
    "postal_code": FormField(validate_postal_code, "Wie lautet Ihre Postleitzahl?"),
    "race": FormField(validate_race, "Wie lautet die Rasse des Hundes?"),
    "microchipnumber": FormField(validate_microchipnumber, "Wie lautet die Mikrochipnummer des Hundes?"),
    "dog_arrival": FormField(validate_Date, "Seit wann halten Sie den Hund? (Angabe in TT.MM.YYYY)")
}

DOG_FORM = FormFormat(name="Hundeanmeldeformular", description="Formular zur Registrierung Ihres Hundes", fields=dog_fields)