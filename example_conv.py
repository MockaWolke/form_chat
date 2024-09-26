from form_chat.forms import *
from form_chat.conversational_manager import ConversationalFormManager
import sys    

# Define the fields for the dog registration form in German
dog_fields = {
    "name": FormField(validate_name, "Wie ist Ihr Name?"),
    "birthday": FormField(validate_birthday, "Was ist Ihr Geburtsdatum? (TT.MM.JJJJ)"),
    "address": FormField(validate_address, "Wie lautet Ihre Adresse? (Straßenname Hausnummer)"),
    "postal_code": FormField(validate_postal_code, "Wie lautet Ihre Postleitzahl?")
}

DOG_FORM = FormFormat(name="Hundeanmeldeformular", description="Formular zur Registrierung Ihres Hundes", fields=dog_fields)

manager = ConversationalFormManager(form=DOG_FORM)

def main():
    print("Willkommen beim Hundeanmelde-CLI!")
    print("Bitte geben Sie die erforderlichen Daten zur Registrierung Ihres Hundes ein.\n")

    # Start the loop to simulate chat
    last_presented_field = None

    while True:
        # Get the next question to ask the user
        next_question = manager.get_next_question()
        
        if next_question["status"] == "completed":
            print("Alle Felder wurden erfolgreich ausgefüllt!")
            print("\n")
            print(DOG_FORM)
            
            break

        field = next_question['field']
        question = next_question['question']
        last_presented_field = field

        # Ask the user for input
        user_input = input(f"{question}\n> ")

        # Compute the response based on user input
        response = manager.compute_response(user_input, last_presented_field)

        # Handle errors and success messages
        if response["status"] == "error":
            print(f"Fehler: {response['message']}")
        else:
            print(response["message"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBeenden des Hundeanmelde-CLI. Auf Wiedersehen!")
        sys.exit(0)
