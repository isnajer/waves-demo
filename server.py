"""Backend Server for Waves app."""

from __future__ import print_function
from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from model import connect_to_db, db
from datetime import datetime, timedelta
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, User_Records
from sqlalchemy.exc import IntegrityError
from passlib.hash import argon2
from bs4 import BeautifulSoup
import crud
import os
import re
import requests
import json
import random


import yelp_key 
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# WRITE SOME TESTS FOR ROUTE CALLS....

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
        session['email'] = user.email
        #getting email from object / but has same value as email line 48 (matching)
        # ^ dictionary of user_email: email (as value)
        return render_template("/dashboard.html")
    #if user does not exist then flash message error
    #else user exists check if password is correct


#=============== DASHBOARD ===============#
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


#=============== BWAVES, USER RECORDS, CHARTJS ===============#
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

@app.route("/hype_music")
def hype_music():

    return render_template("hype_music.html")


# Add User Record helper function:
def add_user_record(brain_wave_id):
    user_id = session.get("user_id")
    created_on = datetime.now()
    

    if user_id:

        def get_ip():
            response = requests.get('https://api64.ipify.org?format=json').json()
            return response["ip"]

        def get_location():
            ip_address = get_ip()
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
            location_data = {
                "ip": ip_address,
                "city": response.get("city"),
                "country": response.get("country_name")
            }
            return location_data
        print(get_location())

        user_city = get_location()
        user_country = get_location()

        record = crud.create_user_record(user_id, created_on, brain_wave_id, city=user_city["city"], country=user_country["country"])
        db.session.add(record)
        db.session.commit()


@app.route("/charts")
def show_chartjs():
    
    # TODO: create a function that will pull data from DB and create an images
    # then use this image in your chartjs.html
    """
    def create_chart():
        1) pull data from db for current user
        2) use  python library that creates show_charts based on pulled data from db
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
API_KEY = yelp_key.API_KEY
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

@app.route('/user_search')
def user_search():
    
    zipcode = request.args.get("zipcode")
    holistic = request.args.get("holistic")

    # Define the parameters:
    PARAMETERS = {'term': holistic,
                  'limit': 5,
                  'radius': 20000,
                  'offset': 0,
                  'location': zipcode,
                  'sort_by': "rating"}

    # Make a req. to the Yelp API:
    response = requests.get(url = ENDPOINT,
                            params = PARAMETERS,
                            headers = HEADERS)
    
    # Convert the JSON string to a dictionary:
    business_data = response.json()
    
    search_result = []
    for business in business_data['businesses']:
        # search_result.append(business['name'])
        # search_result.append(business['rating'])
        # search_result.append(business['phone'])
        # search_result.append(business['location']['display_address'])

        Rslt = {'name': business['name'], 
        'location': ", ".join(business['location']['display_address']), 
        'rating': business['rating'],
        'phone': business['phone'],
        'image_url': business['image_url']}
        search_result.append(Rslt)
    print(search_result)
    return jsonify(search_result)


@app.route("/search", methods=["GET", "POST"])
def search():
    """Yelp Search"""

    return render_template('search.html')


@app.route("/about")
def about():
    
    return render_template('about.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


#=============== SESSION BOOKING FUNCTION ===============#
SCOPES = ['https://www.googleapis.com/auth/calendar']

@app.route("/schedule_session")
def schedule_session():
    """Exercises"""

    return render_template('session_invite.html')


@app.route("/session_invite", methods=["POST"])
def session_invite():
    
    # TODO: Incorporate timezone into html.


    #get session, user, and brain_wave IDs for db:
    user_id = session.get("user_id")
    brain_wave_id = request.form.get("brain_wave_id")

    # get start&end times from html: 
    start_session = request.form.get("start_session")
    end_session = request.form.get("end_session")
    
    # converto to ISO format + TimeZone (for now):
    start_session = start_session+":00"
    end_session = end_session+":00"
    print(start_session, end_session)


    """Google Calendar API. Create event"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    ## if flow broken, delete token and re-attempt authorization
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        def get_ip():
            response = requests.get('https://api64.ipify.org?format=json').json()
            return response["ip"]


        def get_location():
            ip_address = get_ip()
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
            location_data = {
                "ip": ip_address,
                "city": response.get("city"),
                "country": response.get("country_name"),
                "timezone": response.get("timezone")
            }
            return location_data
        print(get_location())

        # Convert brain_wave_id to brain_wave_name + location to session_url (once deployed urls need to change!):
        brain_wave_name = None
        session_url = None
        if brain_wave_id == "1":
            brain_wave_name = "Delta"
            session_url = "http://192.168.1.156:5000/delta_waves"
        elif brain_wave_id == "2":
            brain_wave_name = "Theta"
            session_url = "http://192.168.1.156:5000/theta_waves"
        elif brain_wave_id == "3":
            brain_wave_name = "Alpha"
            session_url = "http://192.168.1.156:5000/alpha_waves"
        elif brain_wave_id == "4":
            brain_wave_name = "Beta"
            session_url = "http://192.168.1.156:5000/beta_waves"
        elif brain_wave_id == "5":
            brain_wave_name = "Gamma"
            session_url = "http://192.168.1.156:5000/gamma_waves"
        print(brain_wave_name)

        user_timezone = get_location()
        # Create Calendar Event (need to fetch user timeZone through IP address):
        event = {
        'summary': brain_wave_name + " Waves Sound Therapy Session",
        'location': session_url,
        'description': "Your WAVES session invite.",
        'start': {
            'dateTime': start_session,
            'timeZone': user_timezone["timezone"],
        },
        'end': {
            'dateTime': end_session,
            'timeZone': user_timezone["timezone"],
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': session['email']},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }

        book_session = crud.create_booked_session(start_session=start_session, end_session=end_session, timezone=user_timezone["timezone"], user_id=user_id, brain_wave_id=brain_wave_id)
        db.session.add(book_session)
        db.session.commit()
        flash(brain_wave_name + " Waves Session Booked! Check Your Email/Calendar!")


        event = service.events().insert(calendarId='primary', body=event, sendUpdates="all").execute()
        print(' Session Created: %s' % (event.get('htmlLink')))


        print(book_session)

    except HttpError as error:
        print('An error occurred: %s' % error)

    
    return render_template('session_invite.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)