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
import re

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


#API calls should be in this file through flask routes.

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    match_obj = re.search(r"(\w+)\@(\w+\.com)", email)
    if match_obj is None:
        flash("Invalid email address")
        return redirect('/')
    elif user: #if user exists 
        flash("User with this email already exists.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")

### ASK IF I STILL NEED CODE IN THIS:
# @app.route("/dashboard")
# def user_details():
#     """Users dashboard."""
#     # return "THIS IS THE DASHBOARD!"
#     user_id = session.get("user_id")

#     # Is user logged in?
#     if user_id:
#         user = User.query.get(user_id)
#         return render_template("dashboard.html", user=user)

#     # If not, redirect to homepage.
#     else:
#         flash("You are not logged in.")
#         return redirect('/')


@app.route("/dashboard", methods=["POST"])
def login():
    """Logs user in / Directs them to user details dashboard if login successful."""

    email = request.form.get("email") #from HTML
    password = request.form.get("password")

    user = crud.get_user_by_email(email) #<- invoking function from crud.py
    if not user:
        flash("User email does not exist.")
        return redirect("/")
    elif user.password != password:
        flash("Password is incorrect!")
        return redirect("/")
    else:
        session['user_email'] = user.email #getting email from object / but has same value as email line 48 (matching)
        # ^ dictionary of user_email: email (as value)
        return render_template("/dashboard.html")
    #if user does not exist then flash message error
    #else user exists check if password is correct
        



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)