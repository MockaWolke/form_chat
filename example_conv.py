from form_chat.forms import *
from form_chat.conversational_manager import ConversationalFormManager
import sys    

dog_fields = {
    "name": FormField(validate_name, "What is your name?"),
    "birthday": FormField(validate_birthday, "What is your birthday? (DD.MM.YYYY)"),
    "address": FormField(validate_address, "What is your address? (Streetname Housenumber)"),
    "postal_code": FormField(validate_postal_code, "What is your postal code?")
}

DOG_FORM = FormFormat(name="Dog Registration Form", description="Form to register your dog", fields=dog_fields)



manager = ConversationalFormManager(form=DOG_FORM)


def main():
    print("Welcome to the Dog Registration CLI!")
    print("Please provide the necessary details to register your dog.\n")

    # Start the loop to simulate chat
    last_presented_field = None

    while True:
        # Get the next question to ask the user
        next_question = manager.get_next_question()
        
        if next_question["status"] == "completed":
            print("All fields are successfully filled!")
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
            print(f"Error: {response['message']}")
        else:
            print(response["message"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the Dog Registration CLI. Goodbye!")
        sys.exit(0)