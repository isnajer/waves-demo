"""Backend Server for Waves app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from model import connect_to_db, db
import crud
from datetime import datetime, timedelta
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, User_Records
from sqlalchemy.exc import IntegrityError
import bcrypt
import os
import re
import requests
import json 

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#API calls should be in this file through flask routes.


#=============== IDX, SIGN UP, LOGIN ===============#
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

    fname = request.form.get("fname")
    lname = request.form.get("lname")
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
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")


@app.route("/login")
def login():
    
    return render_template('login.html')


@app.route("/login", methods=["POST", "GET"])
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
        session['user_id'] = user.user_id
        session['fname'] = user.fname
        #getting email from object / but has same value as email line 48 (matching)
        # ^ dictionary of user_email: email (as value)
        return render_template("/dashboard.html")
    #if user does not exist then flash message error
    #else user exists check if password is correct


#=============== DASHBOARD, BWAVES, CHARTJS ===============#
@app.route("/dashboard")
def user_dashboard():
    """User dashboard."""

    user_id = session.get("user_id")
    fname = session.get("fname")
    # ^ to display user name on pages....and add it to render_temp below (fname=fname)

    # Is user logged in:
    if user_id and fname:

        return render_template("dashboard.html")

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
    

@app.route("/charts")
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

    for brain_wave_id, _ in brain_wave_count.items():
        records_count = User_Records.query.filter_by(brain_wave_id=brain_wave_id, user_id=user_id).count()
        brain_wave_count[brain_wave_id] = records_count
    print(f"=== {brain_wave_count}")
    
    return brain_wave_count


@app.route("/chartjs")
def chart():
    
    return render_template('chartjs.html')


#=============== YELP BUSINESS API, ABOUT, LOGOUT ===============#
# Define a business ID:
business_id = ' '

# Define the API key::
API_KEY = 'fXyaeMmVOoXwDawXFDUqTlE9N8rzF4ocxWBqiQGeXKXyAj7-TIQaWbcu_-r1gfFC54Vg744qnh9xjU03lSrxzassUeIzG5fqRxYdGA7kK1cAqUlmg5qRx9UHC_9qY3Yx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

@app.route('/user_search')
def user_search():

    zipcode = request.args.get("zipcode")
    holistic = request.args.get("holistic")

    # Define the parameters:
    PARAMETERS = {'term': holistic,
                  'limit': 10,
                  'radius': 20000,
                  'offset': 0,
                  'location': zipcode}

    # Make a req. to the Yelp API:
    response = requests.get(url = ENDPOINT,
                            params = PARAMETERS,
                            headers = HEADERS)
    
    # Convert the JSON string to a dictionary:
    business_data = response.json()

    search_result = []
    for business in business_data['businesses']:
        Rslt = {'Name': business['name'], 'Location': business['location']['display_address']}
        search_result.append(Rslt)
    print(search_result)
    return jsonify(search_result)

# print(business_data.keys())

# for biz in business_data['businesses']:
#     print(biz['name']) # <-- or whatever attribute of the business you want...

# Print the response:
# print(json.dumps(business_data, indent = 3))
# OR:
# Write a response file:
# f = open('.\\apis\\yelp_results.txt', 'w')
# f.write(json.dumps(business_data, indent = 3))
# f.close()

# Business Search - FULL LIST:
# PARAMETERS = {'term': 'good food',
#               'location': 'Los Angeles',
#               'latitude': 32.715,
#               'longitude': -117.161,
#               'radius': 100000,
#               'categories': 'bars,french',
#               'locale': 'en_US',
#               'limit': 50,
#               'offset': 150,
#               'sort_by': 'best_match',
#               'price': '1',
#               'open_now': True,
#               'open_at': 1546215674,
#               'attributes': 'hot_and_new'}


@app.route("/search", methods=["GET", "POST"])
def search():
    """Yelp Search"""

    # zipcode = request.form.get("zipcode")
    # holistic = request.form.get("holisitc")
    # offset = int(request.form.get("offset", 0))

    # data = get_search_by_zip(zipcode, holistic)
    # business = data['businesses']
    return render_template('search.html')


@app.route("/about")
def about():
    
    return render_template('about.html')


@app.route("/logout")
def logout():
    # session['fname'] = None
    # session['user_id'] = None
    session.clear()
    return redirect('/')


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