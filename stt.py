import speech_recognition as sr
import threading

# Sprache je nach Modus — Quellsprache wird erkannt
SPRACHEN = {
    "assistent": "de-DE",
    # → Deutsch (Quellsprache wird erkannt)
    "fr_de": "fr-FR",
    "en_de": "en-US",
    "es_de": "es-ES",
    "it_de": "it-IT",
    "pt_de": "pt-PT",
    "nl_de": "nl-NL",
    "pl_de": "pl-PL",
    "sv_de": "sv-SE",
    "ro_de": "ro-RO",
    "hr_de": "hr-HR",
    "sr_de": "sr-RS",
    "cs_de": "cs-CZ",
    "sk_de": "sk-SK",
    "el_de": "el-GR",
    "hu_de": "hu-HU",
    "da_de": "da-DK",
    "fi_de": "fi-FI",
    # Deutsch → (immer Deutsch erkennen)
    "de_fr": "de-DE",
    "de_en": "de-DE",
    "de_es": "de-DE",
    "de_it": "de-DE",
    "de_pt": "de-DE",
    "de_nl": "de-DE",
    "de_pl": "de-DE",
    "de_sv": "de-DE",
    "de_ro": "de-DE",
    "de_hr": "de-DE",
    "de_cs": "de-DE",
    "de_el": "de-DE",
    "de_hu": "de-DE",
}

# Globales Stop-Flag
stop_flag = threading.Event()

def stop_listening():
    stop_flag.set()

def listen(modus="assistent"):
    sprache = SPRACHEN.get(modus, "de-DE")
    recognizer = sr.Recognizer()
    stop_flag.clear()  # Flag zurücksetzen

    with sr.Microphone() as source:
        print(f"🎤 Höre zu... (Sprache: {sprache})")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 1.5
        recognizer.non_speaking_duration = 0.5

        try:
            # Aufnahme in kleinen Blöcken damit stop_flag geprüft werden kann
            frames = []
            while not stop_flag.is_set():
                try:
                    chunk = recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    frames.append(chunk)
                    # Wenn Stille erkannt wurde (phrase beendet), aufhören
                    break
                except sr.WaitTimeoutError:
                    # Noch keine Sprache — weiter warten bis stop_flag gesetzt
                    continue

            if stop_flag.is_set() and not frames:
                print("Aufnahme manuell gestoppt")
                return None

            if not frames:
                return None

            audio = frames[0]
            text = recognizer.recognize_google(audio, language=sprache)
            print(f"Erkannt: {text}")
            return text

        except sr.UnknownValueError:
            print("Sprache nicht erkannt")
            return None
        except sr.RequestError as e:
            print(f"Google Speech API Fehler: {e}")
            return None
