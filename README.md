# Prototyp for Chat Bot for Filling Out Government Forms

This project is a prototype for a chatbot that assists with filling out government forms. It currently relies on the OpenAI API for slot filling and intent detection, making it adaptable for various forms.

## Features
- **OpenAI API Integration**: Utilizes the OpenAI API to handle slot filling and intent detection for dynamic conversations.
- **Easily Extendible**: The system can be easily extended to support different forms. For an example, check out `src/form_chat/hunde_form.py`.
  
## Structure

```
├── src/form_chat
│   The main package handling all chatbot logic, form validation, and interaction flow.
│   ├── conversational_manager.py 
│   ├── forms.py 
│   ├── validation_funcs.py
│   ├── hunde_form.py  # Example of a government form implementation for dog registration.
│   ├── interfaces.py
│   └── pdf.py
├── backend.py 
│   Simple FastAPI wrapper around the package, providing API routes for the frontend to interact with.
├── static/
│   ├── index.html
│   └── js/
│       └── main.js
    Frontend code (HTML, CSS, JavaScript) for the chat interface.
├── pdfs
    Folder for storing generated PDFs.
└── test_form.py
    Test script for form interactions.

```

## Installation

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Copy the .env.template file and rename it to .env. Include your OpenAI API key in the .env file:

```OPENAI_API_KEY=your-api-key-here```


## Running the Project
Start the server with the following command:
```uvicorn backend:app```
