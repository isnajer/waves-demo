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


@app.route("/login", methods=["POST"])
def user_login():
    """Logs user in"""

    email = request.form.get("email") #from HTML
    password = request.form.get("password")

    user = crud.get_user_by_email(email) #<- invoking function from crud.py
    if not user or user.password != password:
        return render_template("dashboard.html", user=user)
    else:
        session['user_email'] = user.email #getting email from object / but has same value as email line 48 (matching)
        # ^ dictionary of user_email: email (as value)
        flash("Logged in succesfully!")

    #if user does not exist then flash message error
    #else user exists check if password is correct
        return redirect("/dashboard.html")


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user: #if user exists 
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)




### CHANGE TO THESE WHEN EVERYTHING WORKS! ###

# @app.route('/login', methods=['POST'])
# def login():
#     """Check if user exists. Redirect to dashboard."""

#     email = request.form.get('email')
#     password = request.form.get('password')

#     # user = crud.get_user_by_email(email)
#     user = User.query.filter(User.email==email).first()
#     if not user:
#         flash("User does not exist.")
#         return redirect("/")

#     if user.password != bcrypt.hashpw(password.encode(), user.password):
#         flash("Incorrect password")
#         return redirect("/")

#     session["user_id"] = user.user_id

#     flash("Logged in sucesfully!")
#     return redirect("/dashboard")


# @app.route('/sign_up', methods= ['POST'])
# def sign_up():
#     """Add new user into database."""

#     email = request.form.get('email')
#     password = request.form.get('password')
#     name = request.form.get('name', '').strip()
#     if not name:
#         flash("Must enter a name!")
#         return redirect('/')

#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode(), salt)
#     try:
#         new_user = User(email=email, password=hashed_password, name=name)
#         db.session.add(new_user)
#         db.session.commit()
#     except IntegrityError:
#         flash('User with this email already exists')
#         return redirect('/')

#     # Add new user to the session
#     new_user = User.query.filter(User.email==email).one()
#     session['user_id'] = new_user.user_id

#     flash("User {} added.".format(name))
#     return redirect("/dashboard")