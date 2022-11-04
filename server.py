"""Backend Server for Waves app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from model import connect_to_db, db
import crud
from datetime import datetime, timedelta
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


@app.route("/signup")
def signup():
    
    return render_template('signup.html')


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    match_obj = re.search(r"(\w+)\@(\w+\.com)", email)
    if match_obj is None:
        flash("Invalid email address")
        return redirect('/signup')
    elif user: #if user exists 
        flash("User with this email already exists.")
        return redirect('/login')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")


@app.route("/login")
def login():
    
    return render_template('login.html')


@app.route("/login", methods=["POST"])
def login_user():
    """Logs user in / Directs them to user dashboard if login successful."""

    email = request.form.get("email") #from HTML
    password = request.form.get("password")

    user = crud.get_user_by_email(email) #<- invoking function from crud.py
    if not user:
        flash("User email does not exist.")
        return redirect("/login")
        # Add hyperlink to redirect to signup
    elif user.password != password:
        flash("Password is incorrect!")
        return redirect("/login")
    else:
        session['user_id'] = user.user_id #getting email from object / but has same value as email line 48 (matching)
        # ^ dictionary of user_email: email (as value)
        return render_template("/dashboard.html")
    #if user does not exist then flash message error
    #else user exists check if password is correct


@app.route("/dashboard")
def user_dashboard():
    """User dashboard."""

    user_id = session.get("user_id")

    # Is user logged in:
    if user_id:
        user = User.query.get(user_id)
        return render_template("dashboard.html", user=user)

    # If not logged in, redirect to homepage:
    else:
        flash("You are not logged in.")
        return redirect('/login')


# TO KEEP RECORD OF USER ACTIVITY:
# before rendering template (while user logged in) save record w/ user_id and brainwave_id:
@app.route("/delta_waves", methods=["GET"])
def delta_waves():

    user_id = session.get("user_id")
    # user_records_id = session.get("user_records_id")
    created_on = datetime.now()

    # Is user logged in?
    if user_id:
        user = User.query.get(user_id)
        record = crud.create_user_record(user_id, created_on, 1)
        db.session.add(record)
        db.session.commit()
        print(record)
        return render_template("delta_waves.html", user=user, record=record)

    # If not, redirect to homepage.
    else:
        flash("You are not logged in.")
        return redirect('/login')


@app.route("/theta_waves")
def theta_waves():

    user_id = session.get("user_id")

    # Is user logged in?
    if user_id:
        user = User.query.get(user_id)
        return render_template("theta_waves.html", user=user)

    # If not, redirect to homepage.
    else:
        flash("You are not logged in.")
        return redirect('/login')


@app.route("/alpha_waves")
def alpha_waves():

    user_id = session.get("user_id")

    # Is user logged in?
    if user_id:
        user = User.query.get(user_id)
        return render_template("alpha_waves.html", user=user)

    # If not, redirect to homepage.
    else:
        flash("You are not logged in.")
        return redirect('/login')


@app.route("/beta_waves")
def beta_waves():

    user_id = session.get("user_id")

    # Is user logged in?
    if user_id:
        user = User.query.get(user_id)
        return render_template("beta_waves.html", user=user)

    # If not, redirect to homepage.
    else:
        flash("You are not logged in.")
        return redirect('/login')


@app.route("/gamma_waves")
def gamma_waves():

    user_id = session.get("user_id")

    # Is user logged in?
    if user_id:
        user = User.query.get(user_id)
        return render_template("gamma_waves.html", user=user)

    # If not, redirect to homepage.
    else:
        flash("You are not logged in.")
        return redirect('/login')
    

@app.route("/chartjs")
def show_chartjs():

    return render_template('chartjs.html')


@app.route("/about")
def about():
    
    return render_template('about.html')


@app.route("/logout")
def logout():

    return render_template('homepage.html')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)