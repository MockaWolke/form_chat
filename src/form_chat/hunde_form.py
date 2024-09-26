from .forms import *

# Define the fields for the dog registration form in German
dog_fields = {
    "name": FormField(validate_name, "Wie ist Ihr Name?"),
    "birthday": FormField(validate_birthday, "Was ist Ihr Geburtsdatum? (TT.MM.JJJJ)"),
    "address": FormField(validate_address, "Wie lautet Ihre Adresse? (Straßenname Hausnummer)"),
    "postal_code": FormField(validate_postal_code, "Wie lautet Ihre Postleitzahl?")
}

DOG_FORM = FormFormat(name="Hundeanmeldeformular", description="Formular zur Registrierung Ihres Hundes", fields=dog_fields)