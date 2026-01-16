# 🎮 GrymFacts – Loading-Screen Facts App

**GrymFacts** ist eine kleine, stylische Desktop-App mit integrierter Weboberfläche, die zufällige „Loading-Screen Facts“ wie aus Videospielen anzeigt – inklusive animiertem Ladebalken, humorvollen Lade-Texten und Admin-Interface.

Die App läuft lokal, speichert ihre Daten selbstständig und kann als **eigenständige Windows-EXE** gebaut werden.

---

## ✨ Features

- 🎲 Zufällige Facts wie aus Game-Loading-Screens
- ⏳ Animierter Ladebildschirm mit witzigen Lade-Texten
- 🧠 Zwei Datenkategorien:
  - **Facts** (angezeigter Inhalt)
  - **Loading-Texte** (während des Ladebalkens)
- 🔐 Passwortgeschützter Admin-Bereich
- ✏️ Facts & Loading-Texte direkt im Web-UI bearbeiten
- 💾 Lokale SQLite-Datenbank (keine Cloud, kein Tracking)
- 🖥️ Optimiert für Desktop & Mobile (Dark Mode UI)
- 📦 Als **Windows-EXE** ohne Python installierbar

---

## 🚀 Nutzung (als EXE)

1. `GrymFacts.exe` starten  
2. Browser öffnet sich automatisch unter  
   👉 `http://127.0.0.1:5000`
3. Button **„Random Fact“** drücken 🎉

> ⚠️ Beim ersten Start kann Windows SmartScreen warnen  
> → „Weitere Informationen“ → „Trotzdem ausführen“

---

## 🔐 Admin-Bereich

- Zugriff über **„Admin“** Button
- **Default-Passwort:** `admin`  
  👉 **Bitte direkt ändern!**
- Im Admin-Bereich kannst du:
  - Facts hinzufügen / bearbeiten / löschen
  - Loading-Texte verwalten
  - Admin-Passwort ändern

---

## 💾 Daten & Speicherort

Die App speichert Daten automatisch im Benutzerverzeichnis:

- **Windows:**  
  `%APPDATA%\GrymFacts\facts.db`
- **Linux:**  
  `~/.local/share/GrymFacts/facts.db`

➡️ Updates oder neue EXE-Versionen löschen **keine** Daten.

---

## 🛠️ Entwicklung (lokal)

### Voraussetzungen
- Python **3.11+**
- Git

### Setup

```bash
git clone https://github.com/<dein-user>/<repo-name>.git
cd <repo-name>

python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# oder
.\.venv\Scripts\activate   # Windows

pip install -r requirements.txt
python app.py
