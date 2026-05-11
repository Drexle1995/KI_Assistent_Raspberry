import os
import threading
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import anthropic
from tts import speak
from stt import listen

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODI = {
    # Assistent
    "assistent": "Du bist ein hilfreicher KI-Assistent. Antworte immer auf Deutsch.",

    # → Deutsch
    "fr_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Französischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "en_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Englischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "es_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Spanischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "it_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Italienischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "pt_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Portugiesischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "nl_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Niederländischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "pl_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Polnischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "sv_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Schwedischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "ro_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Rumänischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "hr_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Kroatischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "sr_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Serbischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "cs_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Tschechischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "sk_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Slowakischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "el_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Griechischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "hu_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Ungarischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "da_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Dänischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "fi_de": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Finnischen ins Deutsche. Gib NUR die Übersetzung aus, ohne Erklärungen.",

    # Deutsch →
    "de_fr": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Französische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_en": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Englische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_es": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Spanische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_it": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Italienische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_pt": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Portugiesische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_nl": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Niederländische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_pl": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Polnische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_sv": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Schwedische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_ro": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Rumänische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_hr": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Kroatische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_cs": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Tschechische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_el": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Griechische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
    "de_hu": "Du bist ein Übersetzer. Übersetze alles was der Nutzer schreibt vom Deutschen ins Ungarische. Gib NUR die Übersetzung aus, ohne Erklärungen.",
}

# Gesprächsverlauf (wird pro Session im Speicher gehalten)
conversation_history = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    modus = data.get("modus", "assistent")

    if not user_input:
        return jsonify({"error": "Keine Eingabe"}), 400

    # Unbekannten Modus abfangen
    if modus not in MODI:
        modus = "assistent"

    # Nachricht zum Verlauf hinzufügen
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=MODI[modus],
            messages=conversation_history
        )

        reply = response.content[0].text

        # Antwort zum Verlauf hinzufügen
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        # Sprachausgabe in eigenem Thread (blockiert nicht den Browser)
        threading.Thread(target=speak, args=(reply,), daemon=True).start()

        return jsonify({"reply": reply})

    except Exception as e:
        # Bei Fehler die letzte User-Nachricht wieder entfernen
        conversation_history.pop()
        print(f"Fehler bei Claude-Anfrage: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/listen", methods=["POST"])
def listen_route():
    try:
        data = request.json or {}
        modus = data.get("modus", "assistent")
        text = listen(modus)
        if text:
            return jsonify({"text": text})
        return jsonify({"error": "Nichts verstanden"}), 400
    except Exception as e:
        print(f"Fehler bei Spracheingabe: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/stop_listen", methods=["POST"])
def stop_listen_route():
    from stt import stop_listening
    stop_listening()
    return jsonify({"status": "ok"})


@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
