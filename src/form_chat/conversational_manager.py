from form_chat.forms import *
import re
from openai import OpenAI
from loguru import logger
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_KEY"],
)



class ConversationalFormManager:
    def __init__(self, form: FormFormat, openai_client = client, model_name="gpt-3.5-turbo"):
        self.form = form
        self.openai_client = openai_client
        self.model_name = model_name
        self.openai_config = {"temperature": 0.9}

    def get_next_question(self) -> dict:
        missing  = self.form.missing_values
        
        if missing:
            next_field = next(iter(missing))
            question = self.form.fields[next_field].question_in_chat
            return {"status" : f"{len(missing)} fields left","field": next_field, "question": question}
        else:
            return {"status": "completed", "message": "All fields are filled."}

    def identify_field(self, message: str, last_presented_field: str) -> str | None:
        last_question = self.form.fields[last_presented_field].question_in_chat
        
        field_question_pairs = "\n".join([f"{field} - {self.form.fields[field].question_in_chat}" for field in self.form.fields.keys()])

        prompt = f"""
        You are helping to identify the intent of a user message for a chatbot that is filling out forms.
        The user was asked the question for field '{last_presented_field}': "{last_question}".
        Valid form fields and their respective questions are:
        {field_question_pairs}.
        The user's message is: "{message}".
        Which form field is the user most likely referring to?
        
        Return only the field name!
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are helping to identify the intent of a user message for a chatbot that is filling out forms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                **self.openai_config
            )
            
            most_likely_field = response.choices[0].message.content.strip()

            logger.info(f"Received response from OpenAI: {most_likely_field} for message {message}")

            if most_likely_field in self.form.fields:
                logger.debug(f"Field '{most_likely_field}' is valid.")
                return most_likely_field
            else:
                logger.error(f"Invalid field identified by GPT: {most_likely_field}")
                return None
        except Exception as e:
            logger.error(f"Error while identifying the field for message '{message}': {e}", exc_info=True)
            return None

    def slot_filling(self, message: str, field: str) -> str | None:
        question = self.form.fields[field].question_in_chat
        
        prompt = f"""
        You are doing slot extraction based on the chatbot's question: "{question}" for the field "{field}".
        The user answered: "{message}".
        Extract and return only the relevant part of the user message that fills the slot for the field '{field}'.
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are extracting relevant information from user messages."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                **self.openai_config
            )
            
            extracted = response.choices[0].message.content.strip()

            logger.info(f"Extracted: '{extracted}' from message '{message}' and field {field}")

            return extracted
        except Exception as e:
            logger.error(f"Error during slot filling for field '{field}' with message '{message}': {e}", exc_info=True)
            return None

    def process_answer(self, field: str, value: str) -> dict:
        if field not in self.form.fields:
            return {"status": "error", "message": f"Field '{field}' is not a valid form field."}

        error_message = self.form.fill_value(field, value)

        if error_message:
            return {"status": "wrong_value", "message": error_message}
        else:
            return {"status": "success", "message": f"'{field}' was successfully filled."}

    def compute_response(self, message: str, last_presented_field: str) -> dict:
        """
        Process the user's message by identifying the intent, extracting the relevant information, 
        and filling the slot in the form. It returns a response dict indicating the next action.
        """
        try:
            # Identify the field the user is referring to (intent recognition)
            identified_field = self.identify_field(message, last_presented_field)
            if not identified_field:
                return {"status": "error", "message": "Could not identify the field."}

            # Extract the slot value from the message
            extracted_value = self.slot_filling(message, identified_field)
            if not extracted_value:
                return {"status": "w", "message": "Could not extract a valid value for the field."}

            # Process the extracted value
            response = self.process_answer(identified_field, extracted_value)

            return response
        except Exception as e:
            logger.error(f"Error in compute_response for message '{message}': {e}", exc_info=True)
            return {"status": "error", "message": "Something went wrong while processing the message."}
        
        
