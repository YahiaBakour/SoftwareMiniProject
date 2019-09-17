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
5. Run 'python3 -m flask run'
6. Go to http://127.0.0.1:5000/ (or http://localhost:5000/) in your browser
7. Do ‘CTRL+C’ in your terminal to kill the instance.

## Project Design

### Web Framework

### Sensor Simulation

### User Data Storage and Authentication

### Agile Development

