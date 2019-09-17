# SoftwareMiniProject

## Yahia Bakour and Gordon Wallace

### 9/20/2019

## Summary of Project ##

We created a web application built using Flask and hosted on Google Cloud that allows users to sign in and view data from temperature and humidity "sensors" in different saved locations.  We simulated these sensors using the Dark Sky API, a weather API that returns weather information from anywhere in the world, in conjunction with the Google Maps API.  Users' locations of interest are stored using MongoDB, and authentication is done through Google OAuth.

## Setup Instructions

The easiest way to use our application is on Google Cloud here: https://senior-design-252116.appspot.com/Login

To run the application locally, clone this repository and do the following:

1. Install Python 3
2. CD into the directory
3. Do pip3 installs for all imports
4. Run 'export FLASK_APP=main.py' or For windows: $env:FLASK_APP = "main.py" , or set FLASK_APP=main.py
5. Create a Config directory within the main directory and add secret keys.  We can email you those.
6. Run 'python3 -m flask run'
7. Go to http://127.0.0.1:5000/ (or http://localhost:5000/) in your browser
8. Do ‘CTRL+C’ in your terminal to kill the instance.

## Project Design

![](https://github.com/YahiaBakour/SoftwareMiniProject/blob/master/images/diagram.JPG)

### Web Framework

Our web app is an instance of Flask, a framework that allows us to easily define webpages within the app that are associated with Python functions we wrote to provide the desired functionality of each page.  We designated functions associated with a landing page, a page to register user locations, a page to display data on those locations, as well as login, logout, and redirect functions.  We fromatted our webpages using HTML and CSS, and used some basic open-source webpage templates to build off of.

### Sensor Simulation

We simulated our sensors using two APIs: the Dark Sky weather API and the Google Maps API.  When a user enters locations to be stored in their list of places, the Google Maps API returns the most likely corresponding latitude and longitude for the phrase the user entered.  This coordinate is then passed to the Dark Sky API, which returns a weather report for the location (including previous days to generate charts).  Our program then parses through the output and displays the temperature and humidity data, along with a plot of the previous days' weather using the flask_googlecharts package.

### User Data Storage and Authentication

A key aspect of this project is that users can save locations of interest and be able to log in and view the weather data for those locations without having to enter them again, and that multiple users can use the system.  We handled authentication for our web app using Google OAuth, a token-based authentication method that allows users to sign into our application using their Google account.

Once the user has signed in, they're prompted to enter a list of locations.  Known users and their saved locations are stored in an instance of MongoDB on the host computer.  MongoDB stores information using document objects that allow for multiple data types, rather than in tables typical to relational databases.  In our case, we defined a User document object with a string field for their email and a list field for their location preferences.  When users first login, our program checks the database to see if there is already as User object associated with that email.  If one is, their stored locations are loaded.  If not, a new User is created.

### Web Hosting

We used Google App Engine on Google Cloud to host our application.  Google App Engine provides an almost no-config deployment option for Python applications, so running it there was straightforward.  It can be accessed at https://senior-design-252116.appspot.com/Login.

### Agile Development

To streamline our collaboration on the app, we used agile development principles.  We used Trello, which allowed us to create cards with tasks allocated to each of us with target completion dates.  We used two one-week sprints to further organize these tasks and keep us on track.

![](https://github.com/YahiaBakour/SoftwareMiniProject/blob/master/images/calendar.JPG)
![](https://github.com/YahiaBakour/SoftwareMiniProject/blob/master/images/trello.JPG)

### User Stories / Acceptance Criteria

As a user, I'd like to be able to display weather data from multiple locations.

As a user, I'd like to be able to log in and save my favorite locations so I don't have to enter them in the future.

As a user, I don't want to have to create a new account to log in.

As a user, I'd like to see a graph of weather data from previous days in my favorite locations.

As a user, I want to be able to access my data anytime on any computer.

As a user, I want a clean UI.

As a user, I want to see a 404 page on incorrect URL entry.

As a user, I want to see some charted data.
