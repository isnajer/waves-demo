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
        flash("Invalid email address!")
        return redirect('/signup')
    elif user: #if user exists: 
        flash("User with this email already exists. Log in.")
        return redirect('/login')
    else:
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Log in!")
        return render_template('login.html')
    

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
        flash("User email does not exist!")
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
    

@app.route("/sound_therapy")
def sound_therapy():

    return render_template('sound_therapy.html')


#=============== BWAVES, USER RECORDS, CHARTJS ===============#
@app.route("/delta_waves", methods=["GET"])
def delta_waves():
    
    user_id = session.get("user_id")
    if user_id:
        add_user_record(1)
        return render_template("delta_waves.html")
    else:
        flash("You are not logged in.")
        return redirect('/login')
    

@app.route("/theta_waves", methods=["GET"])
def theta_waves():
    user_id = session.get("user_id")
    if user_id:
        add_user_record(2)
    else:
        flash("You are not logged in.")
        return redirect('/login')
    return render_template("theta_waves.html")

@app.route("/alpha_waves", methods=["GET"])
def alpha_waves():
    user_id = session.get("user_id")
    if user_id:
        add_user_record(3)
    else:
        flash("You are not logged in.")
        return redirect('/login')
    return render_template("alpha_waves.html")

@app.route("/beta_waves", methods=["GET"])
def beta_waves():
    user_id = session.get("user_id")
    if user_id:
        add_user_record(4)
    else:
        flash("You are not logged in.")
        return redirect('/login')
    return render_template("beta_waves.html")

@app.route("/gamma_waves", methods=["GET"])
def gamma_waves():
    user_id = session.get("user_id")
    if user_id:
        add_user_record(5)
    else:
        flash("You are not logged in.")
        return redirect('/login')
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
                "country_code": response.get("country_code")
            }
            return location_data
        print(get_location())

        user_city = get_location()
        user_country = get_location()
        
        record = crud.create_user_record(user_id, created_on, brain_wave_id, city=user_city["city"], country_code=user_country["country_code"])
        db.session.add(record)
        db.session.commit()


@app.route("/charts")
def show_chartjs():
    """
    def create_chart():
        1) pull data from db for current user
        2) use  python library that creates show_charts based on pulled data from db
        3) save this image locally
        4) return the name of the image or image location
    chart = create_chart()
    return render_template('chartjs.html', chart)
    """

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


#=============== MAP ===============#    
@app.route("/map")
def show_mapjs():
    """
    SELECT country, COUNT(*) FROM records GROUP BY country;
       country | count
---------------+-------
             1 |     4
             5 |     4
    """


    country_count = {
        'TV': 0, 'SA': 0, 'CH': 0, 'KH': 0, 'NG': 0, 'SS': 0, 'TT': 0, 
        'BT': 0, 'BA': 0, 'BQ': 0, 'SK': 0, 'PW': 0, 'LK': 0, 'BY': 0, 
        'FI': 0, 'HM': 0, 'MG': 0, 'TW': 0, 'TH': 0, 'BE': 0, 'RU': 0, 
        'KN': 0, 'NF': 0, 'CU': 0, 'KZ': 0, 'KR': 0, 'BM': 0, 'ZA': 0, 
        'PM': 0, 'DZ': 0, 'MU': 0, 'LV': 0, 'GF': 0, 'CI': 0, 'CR': 0, 
        'MP': 0, 'ZM': 0, 'NC': 0, 'TG': 0, 'NI': 0, 'BZ': 0, 'CV': 0, 
        'DK': 0, 'MQ': 0, 'BR': 0, 'ST': 0, 'AF': 0, 'PL': 0, 'UM': 0, 
        'ZW': 0, 'FR': 0, 'DO': 0, 'CC': 0, 'NO': 0, 'TZ': 0, 'ER': 0, 
        'GT': 0, 'UG': 0, 'ET': 0, 'GM': 0, 'KI': 0, 'PT': 0, 'TD': 0, 
        'FO': 0, 'VA': 0, 'US': 0, 'VG': 0, 'EH': 0, 'IM': 0, 'YT': 0, 
        'MX': 0, 'AG': 0, 'BJ': 0, 'NR': 0, 'KM': 0, 'GW': 0, 'HU': 0, 
        'BW': 0, 'AQ': 0, 'LS': 0, 'LU': 0, 'GQ': 0, 'PF': 0, 'AS': 0, 
        'KG': 0, 'GA': 0, 'TN': 0, 'BO': 0, 'AE': 0, 'IE': 0, 'MS': 0, 
        'BF': 0, 'AI': 0, 'JO': 0, 'UA': 0, 'PE': 0, 'GY': 0, 'FM': 0, 
        'PS': 0, 'SI': 0, 'PK': 0, 'EG': 0, 'TR': 0, 'MZ': 0, 'MA': 0, 
        'AX': 0, 'AT': 0, 'AO': 0, 'SC': 0, 'GE': 0, 'MH': 0, 'SL': 0, 
        'FJ': 0, 'VC': 0, 'GD': 0, 'PR': 0, 'GG': 0, 'MO': 0, 'TO': 0, 
        'BD': 0, 'BG': 0, 'SZ': 0, 'PY': 0, 'CL': 0, 'NP': 0, 'MK': 0, 
        'TJ': 0, 'HR': 0, 'GU': 0, 'HK': 0, 'BH': 0, 'MY': 0, 'PA': 0, 
        'MT': 0, 'RE': 0, 'NZ': 0, 'SM': 0, 'HN': 0, 'MN': 0, 'AD': 0, 
        'GN': 0, 'UZ': 0, 'CX': 0, 'AZ': 0, 'CD': 0, 'GP': 0, 'BB': 0, 
        'ID': 0, 'ML': 0, 'NU': 0, 'MV': 0, 'SD': 0, 'AW': 0, 'CY': 0, 
        'DE': 0, 'SY': 0, 'MM': 0, 'MC': 0, 'TC': 0, 'VI': 0, 'VN': 0, 
        'IT': 0, 'MD': 0, 'IR': 0, 'YE': 0, 'NL': 0, 'LC': 0, 'TL': 0, 
        'HT': 0, 'MF': 0, 'RS': 0, 'CG': 0, 'AM': 0, 'CW': 0, 'SV': 0, 
        'GH': 0, 'GL': 0, 'SB': 0, 'KY': 0, 'KW': 0, 'SR': 0, 'SX': 0, 
        'KP': 0, 'SE': 0, 'LA': 0, 'VE': 0, 'MW': 0, 'CN': 0, 'UY': 0, 
        'BI': 0, 'IQ': 0, 'DM': 0, 'BV': 0, 'CM': 0, 'JM': 0, 'JE': 0, 
        'LI': 0, 'CK': 0, 'RO': 0, 'QA': 0, 'IL': 0, 'KE': 0, 'SH': 0, 
        'GS': 0, 'IN': 0, 'FK': 0, 'LB': 0, 'TK': 0, 'AU': 0, 'AR': 0, 
        'EE': 0, 'PG': 0, 'SO': 0, 'SJ': 0, 'PN': 0, 'IO': 0, 'CA': 0, 
        'PH': 0, 'GR': 0, 'JP': 0, 'LR': 0, 'AL': 0, 'GB': 0, 'NE': 0, 
        'EC': 0, 'GI': 0, 'WF': 0, 'TF': 0, 'RW': 0, 'CF': 0, 'LT': 0, 
        'BS': 0, 'WS': 0, 'LY': 0, 'CO': 0, 'SG': 0, 'ES': 0, 'MR': 0, 
        'NA': 0, 'CZ': 0, 'ME': 0, 'VU': 0, 'BN': 0, 'DJ': 0, 'OM': 0, 
        'BL': 0, 'TM': 0, 'IS': 0, 'SN': 0
        }

    country_code = session.get("country_code")
    for country_code, _ in country_count.items():
        records_count = User_Records.query.filter_by(country_code=country_code).count()
        country_count[country_code] = records_count
        print(f"=== {country_count}")
    
    country_list = []
    for country, count in country_count.items():
        country_list.append({"id": country, "value": count})
    
    #Serializing JSON:
    json_object = json.dumps(country_list)
    
    return json_object
    

@app.route('/mapjs')
def map():
    """View map"""

    return render_template('mapjs.html')


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
                  'limit': 15,
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
        
        Rslt = {'name': business['name'], 
        'location': ", ".join(business['location']['display_address']), 
        'rating': business['rating'],
        'phone': business['phone'],
        'image_url': business['image_url'],
        'url': business['url']}
        search_result.append(Rslt)

    
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

@app.route("/book_session")
def book_session():
    """Book Session"""

    return render_template('session_invite.html')


@app.route("/session_invite", methods=["POST"])
def session_invite():
    
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
                "countryCode": response.get("country_code"),
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
        flash(brain_wave_name + " session booked! Invite sent to your email.")
        


        event = service.events().insert(calendarId='primary', body=event, sendUpdates="all").execute()
        print(' Session Created: %s' % (event.get('htmlLink')))


        print(book_session)

    except HttpError as error:
        print('An error occurred: %s' % error)

    
    return render_template('session_invite.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)