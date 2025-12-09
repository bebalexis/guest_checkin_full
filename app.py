
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guests.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    party_size = db.Column(db.Integer, default=1)
    checked_in = db.Column(db.Boolean, default=False)

@app.before_first_request
def setup():
    db.create_all()

@app.route("/")
def index():
    guests = Guest.query.all()
    return render_template("index.html", guests=guests)

@app.route("/add", methods=["POST"])
def add():
    g = Guest(name=request.form["name"], party_size=int(request.form.get("party_size",1)))
    db.session.add(g)
    db.session.commit()
    return redirect("/")

@app.route("/toggle_checkin/<int:id>", methods=["POST"])
def toggle(id):
    g = Guest.query.get(id)
    g.checked_in = not g.checked_in
    db.session.commit()
    return redirect("/")

@app.route("/kiosk")
def kiosk():
    guests = Guest.query.all()
    return render_template("kiosk.html", guests=guests)

@app.route("/kiosk_checkin", methods=["POST"])
def kiosk_checkin():
    g = Guest.query.get(int(request.form["guest_id"]))
    g.checked_in = True
    db.session.commit()
    return redirect("/kiosk")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
