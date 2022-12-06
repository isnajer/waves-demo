# WAVES - Sound Therapy On-Demand

For many, wellness services are unaffordable, inaccessible, and require advanced planning.
WAVES’s mission is to expand access to free holistic wellness services and connect people directly to at-home and in-person wellness practices.
WAVES is designed to embed wellbeing into your daily routine, customized to your goals.
Users have on-demand access to a variety of brainwave targetted sound freuencies, the ability to book sound therapy sessions in advance, and 
personalized charts to track their progress over time. 

# Table of Contents

### 💻 Technologies:
- Backend: Python, Flask, PostgreSQL, SQLAlchemy, JS
- Frontend: JS, Bootstrap, HTML, CSS, Jinja2
- APIs: SoundCloud, GoogleCalendar, YelpFusion, IP Address & Geolocation, Chart.js, AnyCharts

### 🚀 Features: 
- [Check out the video demo](https://youtu.be/blIehXRR2Sc) 🎥


## Login/Sign Up
<img width="723" alt="Screen Shot 2022-12-05 at 7 42 34 PM" src="https://user-images.githubusercontent.com/99369436/205812569-75dcd2c5-6481-4ddb-b7fd-9d79ee2f9859.png">


## Dashboard
Now that we are successfully logged in, we are brought to the dashboard which <br /> 
provides the following set of options for engaging with WAVES and a randomized <br />
inspirational quote generator.<br /> <br />
<img width="723" alt="Screen Shot 2022-12-05 at 8 19 58 PM" src="https://user-images.githubusercontent.com/99369436/205812703-daeafa77-472e-482c-a2cf-b6f2afc521fc.png"> <br />

Start Sound Therapy Session: Users can choose from 5 types of sound frequencies, <br />
according to their personal goals.<br /> <br />
<img width="723" alt="Screen Shot 2022-12-05 at 8 30 06 PM" src="https://user-images.githubusercontent.com/99369436/205815220-666f6b92-16dc-4193-bb07-28a2ed7b48b5.png"> <br />

Book Session: Users pick a date and length of session, choose the type of wave they <br />
want to focus on, then click ‘Book Session’ and WAVES will send an invitation to their <br />
email address and calendar. <br /> <br />
<img width="723" alt="Screen Shot 2022-12-05 at 8 35 16 PM" src="https://user-images.githubusercontent.com/99369436/205816004-93936c7e-a681-4254-8bdf-8870f5cc91c0.png"> <br /> 

In-Person Holistic Therapies: Gives users the ability to search for sound therapy and <br />
other holistic services in their area.<br /> <br />
<img width="723" alt="Screen Shot 2022-12-05 at 8 36 03 PM" src="https://user-images.githubusercontent.com/99369436/205816184-53221091-93ea-4646-972f-047422fbb55d.png"> <br /> 

Track My Progress: Renders a bar chart created with Chart.JS that allows users to see which <br />
frequencies they have listened to and how many times. An AJAX fetch request queries the Postgres <br /> 
database to return the user records over time. <br /> <br />
<img width="723" alt="Screen Shot 2022-12-05 at 8 36 30 PM" src="https://user-images.githubusercontent.com/99369436/205816310-8baf4aba-5dc5-4218-837c-3356c15321b9.png"> <br />

About: Includes additional information about this project and its reach. Users can see where <br />
other people around the world are using WAVES.<br /> <br />
<img width="723" alt="Screen Shot 2022-12-05 at 8 38 29 PM" src="https://user-images.githubusercontent.com/99369436/205816789-79dd15e9-5ed7-44cf-bf12-5a95bd6cf873.png"> <br />

## Set Up
Clone or fork repo:<br />
`https://github.com/isnajer/waves-demo.git`

Create and activate a vritual environment inside project directory:<br />
`virtualenv env
source env/bin/activate`

Install project dependencies:<br />
`pip install -r requirements.txt`

Set up database:<br />
`python3 seed_database.py`

Run WAVES:<br />
`make run` or `python3 server.py`

Open 'localhost:5000/' to access the WAVES web application

## About Me
Hi, I'm Isis. WAVES is my first full-stack web application. It took me 5 weeks to complete as part of a 12-week software engineering program with Hackbright Academy.
