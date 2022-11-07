"""Backend Server for Waves app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from model import connect_to_db, db
import crud
from datetime import datetime, timedelta
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, User_Records
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
    add_user_record(1)
    return render_template("delta_waves.html")

@app.route("/theta_waves", methods=["GET"])
def theta_waves():
    add_user_record(2)
    return render_template("theta_waves.html")

@app.route("/alpha_waves", methods=["GET"])
def alpha_waves():
    add_user_record(3)
    return render_template("alpha_waves.html")

@app.route("/beta_waves", methods=["GET"])
def beta_waves():
    add_user_record(4)
    return render_template("beta_waves.html")

@app.route("/gamma_waves", methods=["GET"])
def gamma_waves():
    add_user_record(5)
    return render_template("gamma_waves.html")
    

@app.route("/chartjs")
def show_chartjs():
    
    # TODO: create a function that will pull data from DB and create an images
    # then use this image in your chartjs.html
    """
    def create_chart():
        1) pull data from db for current user
        2) use  python librarry that creates show_charts based on pulled data from db
        3) save this image locally
        4) return the name of the image or image location

    chart = create_chart()
    return render_template('chartjs.html', chart)
    """
        
    user_id = session.get("user_id")

    """
    SELECT brain_wave_id, COUNT(*) FROM records WHERE user_id=3 GROUP BY brain_wave_id;
     brain_wave_id | count 
---------------+-------
             1 |     4
             5 |     4
    """
    brain_wave_count = {
        1: 0, 2: 0, 3:0, 4:0, 5:0
    }
    user_id = session.get("user_id")

    for bw_id, _ in brain_wave_count.items():
        records_count = User_Records.query.filter_by(brain_wave_id=bw_id, user_id=user_id).count()
        brain_wave_count[bw_id] = records_count
    print(f"=== {brain_wave_count}")

    # used brain_wave_count in the chart

    return render_template(
        'chartjs.html',
        brain_wave_count=brain_wave_count,
        user_id=user_id,
        delta=brain_wave_count[1],)


@app.route("/about")
def about():
    
    return render_template('about.html')


@app.route("/logout")
def logout():

    return render_template('homepage.html')


def add_user_record(brain_wave_id):
    user_id = session.get("user_id")
    created_on = datetime.now()

    # Is user logged in?
    if user_id:
        user = User.query.get(user_id)
        record = crud.create_user_record(user_id, created_on, brain_wave_id)
        db.session.add(record)
        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)