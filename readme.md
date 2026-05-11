# 🤖 KI-Assistent — Raspberry Pi 5

Ein KI-gestützter Assistent mit Spracheingabe, Sprachausgabe und Übersetzungsfunktion für 17 europäische Sprachen. Entwickelt als Schulprojekt auf Basis der Claude API von Anthropic.

---

## 📋 Voraussetzungen

- Raspberry Pi 5 (empfohlen: 4 GB oder 8 GB RAM)
- Raspberry Pi OS (Bookworm, 64-bit)
- Python 3.11+
- USB-Mikrofon
- Lautsprecher oder Kopfhörer
- Internetzugang
- API-Key von [console.anthropic.com](https://console.anthropic.com)

---

## 📁 Projektstruktur

```
ki-assistent/
├── app.py              ← Flask-Server (Hauptprogramm)
├── tts.py              ← Text-to-Speech Modul
├── stt.py              ← Speech-to-Text Modul
├── .env                ← API-Key (geheim, nicht teilen!)
├── README.md           ← Diese Datei
└── templates/
    └── index.html      ← Web-Interface
```

---

## ⚙️ Installation

**1. Systempakete installieren:**
```bash
sudo apt update
sudo apt install espeak portaudio19-dev flac -y
```

**2. Python-Pakete installieren:**
```bash
pip install anthropic flask pyttsx3 SpeechRecognition pyaudio python-dotenv
```

**3. API-Key konfigurieren:**

Datei `.env` im Projektordner erstellen:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ▶️ Starten

```bash
cd ki-assistent
python app.py
```

Dann im Browser öffnen:
- Auf dem Pi: `http://localhost:5000`
- Von anderen Geräten im WLAN: `http://[IP-Adresse des Pi]:5000`

IP-Adresse des Pi herausfinden:
```bash
hostname -I
```

---

## 🖥️ Funktionen

| Funktion | Beschreibung |
|---|---|
| 🤖 KI-Assistent | Beantwortet Fragen auf Deutsch |
| 🔊 Sprachausgabe | Liest Antworten automatisch vor |
| 🎤 Spracheingabe | Erkennt gesprochene Eingaben per Mikrofon |
| 🌍 Übersetzer | Übersetzt zwischen Deutsch und 17 europäischen Sprachen |
| 💬 Gesprächsgedächtnis | Erinnert sich an den bisherigen Gesprächsverlauf |
| 🗑️ Chat leeren | Startet ein neues Gespräch |

---

## 🌍 Unterstützte Sprachen

| Kürzel | Sprache | → Deutsch | Deutsch → |
|---|---|---|---|
| FR | Französisch | ✓ | ✓ |
| EN | Englisch | ✓ | ✓ |
| ES | Spanisch | ✓ | ✓ |
| IT | Italienisch | ✓ | ✓ |
| PT | Portugiesisch | ✓ | ✓ |
| NL | Niederländisch | ✓ | ✓ |
| PL | Polnisch | ✓ | ✓ |
| SV | Schwedisch | ✓ | ✓ |
| RO | Rumänisch | ✓ | ✓ |
| HR | Kroatisch | ✓ | ✓ |
| SR | Serbisch | ✓ | — |
| CS | Tschechisch | ✓ | ✓ |
| SK | Slowakisch | ✓ | — |
| EL | Griechisch | ✓ | ✓ |
| HU | Ungarisch | ✓ | ✓ |
| DA | Dänisch | ✓ | — |
| FI | Finnisch | ✓ | — |

---

## 🔧 Häufige Probleme

**Mikrofon wird nicht erkannt:**
```bash
arecord -l        # Verfügbare Mikrofone anzeigen
sudo raspi-config # Audio-Einstellungen öffnen
```

**Sprachausgabe funktioniert nicht:**
```bash
alsamixer         # Lautstärke prüfen
espeak "Hallo"    # espeak direkt testen
```

**API-Fehler:**
- API-Key in `.env` prüfen (kein Leerzeichen)
- Internetverbindung prüfen: `ping google.com`
- Guthaben prüfen: [console.anthropic.com](https://console.anthropic.com)

**pyaudio lässt sich nicht installieren:**
```bash
sudo apt install python3-pyaudio -y
```

---

## 🚀 Autostart beim Booten (optional)

```bash
sudo nano /etc/systemd/system/ki-assistent.service
```

Inhalt:
```
[Unit]
Description=KI-Assistent
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/ki-assistent
ExecStart=/usr/bin/python3 /home/pi/ki-assistent/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Dienst aktivieren:
```bash
sudo systemctl enable ki-assistent
sudo systemctl start ki-assistent
```

---

## 🛠️ Technologien

- **[Claude API](https://www.anthropic.com)** — KI-Modell (claude-opus-4-6)
- **[Flask](https://flask.palletsprojects.com)** — Web-Server
- **[pyttsx3](https://pyttsx3.readthedocs.io)** — Text-to-Speech
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** — Speech-to-Text
- **[espeak](https://espeak.sourceforge.net)** — Sprachsynthese-Engine

---

## ⚠️ Sicherheitshinweise

- Den API-Key **niemals** in den Code schreiben
- Die `.env` Datei **nicht** auf GitHub oder anderen Plattformen hochladen
- Den API-Key **nicht** per Messenger teilen

---

*Schulprojekt — entwickelt mit Claude (Anthropic)*
