from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from form_chat.forms import *
from form_chat.hunde_form import DOG_FORM
from form_chat.conversational_manager import ConversationalFormManager
from form_chat.pdf import create_pdf_table
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os


PDF_FOLDER = "pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

manager = ConversationalFormManager(form=DOG_FORM)

app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow CORS from any origin (for testing purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows any origin; restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat history to store interaction
chat_history = []

# Serve the index.html file at the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open(os.path.join("static", "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/download_form")
def send_download_form():
    filename = os.path.join(
            PDF_FOLDER,
            f"{DOG_FORM.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        )
    
    create_pdf_table(DOG_FORM, filename=filename)
    return FileResponse(filename, media_type='application/pdf', filename=os.path.basename(filename))

@app.get("/next_question")
async def get_next_question():
    next_question = manager.get_next_question()
    
    if next_question["status"] == "completed":
        return JSONResponse(content={
            "status": "completed",
            "message": "Alle Felder wurden erfolgreich ausgefüllt!",
        })
    
    chat_history.append({
        "role": "system",
        "message": next_question["question"]
    })
    
    return JSONResponse(content={
        "status": "ongoing",
        "question": next_question["question"],
        "field": next_question["field"],
        "chat_history": chat_history
    })

@app.post("/submit_answer")
async def submit_answer(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    last_presented_field = data.get("field", "")

    response = manager.compute_response(user_input, last_presented_field)

    if response["status"] == "error":
        chat_history.append({
            "role": "error",
            "message": response["message"]
        })
        return JSONResponse(content={"status": "error", "message": response["message"], "chat_history": chat_history})

    chat_history.append({
        "role": "user",
        "message": user_input
    })

    # Append the system message with both field and value
    if response["status"] == "success":
        chat_history.append({
            "role": "system",
            "field": response["field"],
            "value": response["value"]
        })

        return JSONResponse(content={
            "status": "success",
            "field": response["field"],
            "value": response["value"],
            "message" : None,
            "chat_history": chat_history
        })
        
    return JSONResponse(content={
            "status": response["status"],
            "field": None,
            "value": None,
            "message" : response["message"],
            "chat_history": chat_history
    })