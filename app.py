from flask import Flask, request, redirect, url_for, render_template
import json
import os

app = Flask(__name__)
DATA_FILE = "contacts.json"

# Load contacts
def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save contacts
def save_contacts(contacts):
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

@app.route("/")
def index():
    contacts = load_contacts()
    return render_template("index.html", contacts=contacts)

@app.route("/add", methods=["POST"])
def add_contact():
    contacts = load_contacts()
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    contacts[name] = {"Phone": phone, "Email": email}
    save_contacts(contacts)
    return redirect(url_for("index"))

@app.route("/delete/<name>")
def delete_contact(name):
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
    save_contacts(contacts)
    return redirect(url_for("index"))

@app.route("/edit/<name>", methods=["GET", "POST"])
def edit_contact(name):
    contacts = load_contacts()
    if request.method == "POST":
        contacts[name] = {
            "Phone": request.form["phone"],
            "Email": request.form["email"]
        }
        save_contacts(contacts)
        return redirect(url_for("index"))
    contact = contacts.get(name, {})
    return render_template("edit.html", name=name, contact=contact)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
