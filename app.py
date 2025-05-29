from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Load or create contacts
if not os.path.exists("contacts.json"):
    with open("contacts.json", "w") as f:
        json.dump([], f)

def load_contacts():
    with open("contacts.json", "r") as f:
        return json.load(f)

def save_contacts(contacts):
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=2)

@app.route("/")
def index():
    contacts = load_contacts()
    return render_template("index.html", contacts=contacts)

@app.route("/add", methods=["POST"])
def add():
    contacts = load_contacts()
    contacts.append({
        "name": request.form["name"],
        "phone": request.form["phone"],
        "email": request.form["email"]
    })
    save_contacts(contacts)
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    contacts = load_contacts()
    if 0 <= index < len(contacts):
        contacts.pop(index)
        save_contacts(contacts)
    return redirect(url_for("index"))

# ✅ MOST IMPORTANT: Render-friendly app start
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
