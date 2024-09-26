let lastField = "";

function toTitleCase(str) {
    return str
        .replace(/_/g, ' ') // Ersetzt alle Unterstriche durch Leerzeichen
        .toLowerCase() // Optional: Alles erst mal in Kleinbuchstaben umwandeln
        .split(' ') // In ein Array von Wörtern aufteilen
        .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Jedes Wort großschreiben
        .join(' '); // Wieder zu einem String zusammenfügen
}

function displayMessage(role, message, field = "", value = "", isError = false) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message");

    if (isError) {
        messageDiv.classList.add("error-message"); // Füge eine spezielle Klasse für Fehler hinzu
        messageDiv.textContent = message; // Zeige die Fehlermeldung an
    } else if (role === "system") {
        messageDiv.classList.add("system-message");
        if (field && value) {
            messageDiv.innerHTML = `<span style="color: green;">${toTitleCase(field)}: ${value}</span>`;
        } else {
            messageDiv.textContent = message;
        }
    } else if (role === "user") {
        messageDiv.classList.add("user-message");
        messageDiv.textContent = message;
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
}

async function fetchNextQuestion() {
    const response = await fetch("http://127.0.0.1:8000/next_question");
    const data = await response.json();

    if (data.status === "completed") {
        displayMessage("system", data.message);
        document.getElementById("form-container").style.display = "none";
    } else {
        lastField = data.field;
        displayMessage("system", data.question);
    }
}

async function submitAnswer() {
    const userInput = document.getElementById("user-input").value;
    document.getElementById("user-input").value = "";

    if (!userInput.trim()) return;

    displayMessage("user", userInput);

    const response = await fetch("http://127.0.0.1:8000/submit_answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message: userInput,
            field: lastField,
        }),
    });

    const data = await response.json();
    
    if (data.status === "wrong_value") {
        // Bei Fehlern zeigen wir die Nachricht in roter Schrift an
        displayMessage("system", "Fehler: " + data.message, "", "", true); // "isError" wird auf true gesetzt
    } else if (data.status === "success") {
        displayMessage("system", "", data.field, data.value);
    }

    // Leert das Eingabefeld sofort nach der Eingabe
    document.getElementById("user-input").value = "";
    fetchNextQuestion();
}

// Fügt einen Event Listener für die Enter-Taste hinzu
document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Verhindert das Standardverhalten des Enter-Tasten-Drucks
        submitAnswer();  // Ruft die Submit-Funktion auf
    }
});

// Fetch the first question when the page loads
window.onload = function() {
    fetchNextQuestion();
};
