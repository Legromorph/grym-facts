from __future__ import annotations

import os
from flask import (
    Flask, render_template, request, redirect, url_for,
    jsonify, abort, session, flash
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "facts.db")

# Für Sessions (Cookie-Signing). Für "echt" unbedingt per ENV setzen.
app.config["SECRET_KEY"] = os.environ.get("FACTAPP_SECRET", "dev-secret-change-me")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(16), nullable=False, default="fact")  # "fact" | "loading"
    text = db.Column(db.String(280), nullable=False)


class Setting(db.Model):
    key = db.Column(db.String(64), primary_key=True)
    value = db.Column(db.String(512), nullable=False)


def get_setting(key: str) -> str | None:
    row = Setting.query.get(key)
    return row.value if row else None


def set_setting(key: str, value: str) -> None:
    row = Setting.query.get(key)
    if row:
        row.value = value
    else:
        db.session.add(Setting(key=key, value=value))
    db.session.commit()


def init_db() -> None:
    with app.app_context():
        db.create_all()

        # Seed: normale Facts
        if Fact.query.filter_by(kind="fact").count() == 0:
            seeds = [
                "Tipp: Du kannst jederzeit im Menü speichern.",
                "Wusstest du? Manche Spiele laden schneller mit SSD.",
                "Pro-Tipp: Kurze Pausen verbessern die Reaktionszeit.",
                'Die Länder "Vastoria", "Midien" und "Borland" haben vor Jahren eine Allianz gegründet und werden seitdem im Volksmund als "Das Land der Drei Königinnen" zusammengefasst.',
            ]
            db.session.add_all([Fact(kind="fact", text=s) for s in seeds])
            db.session.commit()

        # Seed: Loading-Lines
        if Fact.query.filter_by(kind="loading").count() == 0:
            loading_lines = [
                "Generiere Trivia…",
                "Entstaube altes Wissen…",
                "Lade Gehirnzellen nach…",
                "Schärfe die Klinge der Erkenntnis…",
                "Kalibriere Faktenkompass…",
                "Sync mit dem Fact-Orakel…",
                "Zähle bis drei…",
                "Lade Ladebildschirm…",
                "Simuliere Fortschritt…",
                "Tue beschäftigt wirkend…",
                "Dieser Text hat keinen Zweck…",
                "Warte auf dramatischen Moment…",
                "Fast fertig… ehrlich!",
                "Noch ein Ladebalken fehlt…",
                "Lade Ladebalken…",
                "Optimiert für unnötige Spannung…",
                "Bitte nicht nervös werden…",
                "Massiere Synapsen…",
                "Öle die Zahnräder im Kopf…",
                "Puste Staub aus dem Kurzzeitgedächtnis…",
                "Starte Denkprozess neu…",
                "Defragmentiere Gehirn…",
                "Ignoriere unnütze Gedanken…",
                "Suche verloren geglaubtes Wissen…",
                "Aktiviere Hirnrinde…",
                "Rüste Wissen aus…",
                "Würfle Erkenntnis…",
                "Buffe Intelligenz +1…",
                "Erhöhe Weisheit um 2 Punkte…",
                "Lade Skilltree…",
                "Resette Cooldown…",
                "Bereite Tutorial-Hinweis vor…",
                "Speichere vor dem Fact…",
                "Opfere Bits an den Prozessor…",
                "Besteche den Algorithmus…",
                "Schiebe Nullen und Einsen herum…",
                "Bitte KI um Erlaubnis…",
                "Streite mit dem Server…",
                "Erfinde temporäre Variablen…",
                "Erhöhe CPU-Lüftergeräusch imaginär…",
                "Rechne sehr kompliziert aus…",
                "Das dauert absichtlich so lange…",
                "Du hättest eh nichts anderes getan…",
                "Zeit für eine Mini-Pause…",
                "Atme ein… atme aus…",
                "Das ist gleich vorbei… vielleicht.",
                "Noch ein ganz kleiner Moment…",
                "Jetzt wirklich fast fertig…",
                "Befrage das Orakel…",
                "Blicke in den Abgrund des Wissens…",
                "Ziehe einen Fact aus dem Hut…",
                "Rühre im Topf der Erkenntnis…",
                "Schüttle die Realität leicht…",
                "Justiere die Wahrheit…",
                "Verhandle mit der Logik…",
                "Kalibriere Unsinnsfaktor…",
                "Validiere Faktenhaftigkeit…",
                "Verifiziere Plausibilität…",
                "Prüfe, ob das interessant ist…",
                "Verwerfe langweilige Fakten…",
                "Lade nur die guten Bits…",
                "Fast da… 🐢",
                "Nicht abstürzen…",
                "Alles unter Kontrolle.",
                "Das ist Teil der Erfahrung.",
                "Hätte schneller sein können.",
                "Jetzt bitte staunen…",
                "Bitte warten… das ist Absicht.",
                "Lade Bildschirmhinweis…",
                "Dieser Ladevorgang ist kosmetisch…",
                "Fast fertig… vermutlich.",
                "Noch ein Moment…",
                "Optimiert für dramatische Spannung…",
                "Simuliere Fortschrittsbalken…",
                "Lade…",
                "Bitte warten…",
                "Bereite Fact vor…",
                "Finalisiere Inhalt…",
                "Fast da…",
                "Einen Augenblick…",
            ]
            db.session.add_all([Fact(kind="loading", text=s) for s in loading_lines])
            db.session.commit()

        # Default Admin-Passwort
        if not get_setting("admin_pw_hash"):
            set_setting("admin_pw_hash", generate_password_hash("admin"))


init_db()


def require_admin():
    if not session.get("is_admin"):
        return redirect(url_for("login", next=request.path))
    return None


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/random_fact")
def random_fact():
    fact = Fact.query.filter_by(kind="fact").order_by(func.random()).first()
    if not fact:
        return jsonify({"text": "Keine Facts vorhanden. Bitte im Admin-Bereich hinzufügen."})
    return jsonify({"text": fact.text})


@app.get("/api/random_loading")
def random_loading():
    line = Fact.query.filter_by(kind="loading").order_by(func.random()).first()
    if not line:
        return jsonify({"text": "Lade…"})
    return jsonify({"text": line.text})


@app.get("/login")
def login():
    next_url = request.args.get("next") or url_for("admin")
    return render_template("login.html", next_url=next_url)


@app.post("/login")
def login_post():
    pw = request.form.get("password") or ""
    next_url = request.form.get("next_url") or url_for("admin")

    pw_hash = get_setting("admin_pw_hash")
    if pw_hash and check_password_hash(pw_hash, pw):
        session["is_admin"] = True
        return redirect(next_url)

    flash("Falsches Passwort.")
    return redirect(url_for("login", next=next_url))


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.get("/admin")
def admin():
    gate = require_admin()
    if gate:
        return gate

    facts = Fact.query.filter_by(kind="fact").order_by(Fact.id.asc()).all()
    loading = Fact.query.filter_by(kind="loading").order_by(Fact.id.asc()).all()
    return render_template("admin.html", facts=facts, loading=loading)


@app.post("/admin/add")
def add_fact():
    gate = require_admin()
    if gate:
        return gate

    text = (request.form.get("text") or "").strip()
    kind = (request.form.get("kind") or "fact").strip()

    if kind not in ("fact", "loading"):
        abort(400, "Ungültiger Typ.")
    if not text:
        return redirect(url_for("admin"))
    if len(text) > 280:
        abort(400, "Text zu lang (max 280 Zeichen).")

    db.session.add(Fact(kind=kind, text=text))
    db.session.commit()
    return redirect(url_for("admin"))


@app.get("/admin/edit/<int:fact_id>")
def edit_fact_page(fact_id: int):
    gate = require_admin()
    if gate:
        return gate

    fact = Fact.query.get_or_404(fact_id)
    return render_template("edit.html", fact=fact)


@app.post("/admin/edit/<int:fact_id>")
def edit_fact_save(fact_id: int):
    gate = require_admin()
    if gate:
        return gate

    fact = Fact.query.get_or_404(fact_id)
    text = (request.form.get("text") or "").strip()

    if not text:
        abort(400, "Text darf nicht leer sein.")
    if len(text) > 280:
        abort(400, "Text zu lang (max 280 Zeichen).")

    fact.text = text
    db.session.commit()
    return redirect(url_for("admin"))


@app.post("/admin/delete/<int:fact_id>")
def delete_fact(fact_id: int):
    gate = require_admin()
    if gate:
        return gate

    fact = Fact.query.get_or_404(fact_id)
    db.session.delete(fact)
    db.session.commit()
    return redirect(url_for("admin"))


@app.post("/admin/change_password")
def change_password():
    gate = require_admin()
    if gate:
        return gate

    current_pw = request.form.get("current_pw") or ""
    new_pw = request.form.get("new_pw") or ""
    new_pw2 = request.form.get("new_pw2") or ""

    pw_hash = get_setting("admin_pw_hash")
    if not pw_hash or not check_password_hash(pw_hash, current_pw):
        flash("Aktuelles Passwort stimmt nicht.")
        return redirect(url_for("admin"))

    if len(new_pw) < 6:
        flash("Neues Passwort zu kurz (mind. 6 Zeichen).")
        return redirect(url_for("admin"))

    if new_pw != new_pw2:
        flash("Neues Passwort stimmt nicht überein.")
        return redirect(url_for("admin"))

    set_setting("admin_pw_hash", generate_password_hash(new_pw))
    flash("Passwort geändert ✅")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
