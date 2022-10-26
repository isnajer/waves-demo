"""Backend Server for Waves app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from model import connect_to_db, db, User
from sqlalchemy.exc import IntegrityError
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


#API calls should be in this file through flask routes.

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route("/dashboard")
def user_details():
    """Users dashboard."""

    user_id = session.get("user_id")

    # Is user logged in?
    if user_id:
        user = User.query.get(user_id)
        return render_template("dashboard.html", user=user)

    # If not, redirect to homepage.
    else:
        flash("You are not logged in.")
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    """Check if user exists. Redirect to dashboard."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email==email).first()
    if not user:
        flash("User does not exist.")
        return redirect("/")

    if user.password != bcrypt.hashpw(password.encode(), user.password):
        flash("Incorrect password")
        return redirect("/")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/dashboard")


@app.route('/sign_up', methods= ['POST'])
def sign_up():
    """Add new user into database."""

    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name', '').strip()
    if not name:
        flash("Must enter a name!")
        return redirect('/')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    try:
        new_user = User(email=email, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        flash('User with this email already exists')
        return redirect('/')

    # Add new user to the session
    new_user = User.query.filter(User.email==email).one()
    session['user_id'] = new_user.user_id

    flash("User {} added.".format(name))
    return redirect("/dashboard")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)