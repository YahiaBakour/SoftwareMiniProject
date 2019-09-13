'''
SET UP INFO:
1. Install Python 3
2. CD into the directory
3. Run 'pip3 install Flask'
4. Run 'pip3 install pymongo' -- To be used soon
5. Run 'export FLASK_APP=main.py' or For windows: $env:FLASK_APP = "main.py" , or set FLASK_APP=main.py
6. Run 'python3 -m flask run'
7. Go to http://127.0.0.1:5000/ (or http://localhost:5000/) in your browser
8. Do ‘CTRL+C’ in your terminal to kill the instance.
9. To auto update the instance once you save ,export FLASK_DEBUG=1 or windows:  $env:FLASK_DEBUG = "main.py"
'''
# [START gae_python37_app]

from flask import Flask , request,jsonify, redirect,render_template, url_for, session
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin, LoginManager
from Config import config
from flask_oauth import OAuth
from urllib.request import urlopen
from urllib import request as URLLib_request
from urllib import error
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, InputRequired
from APIs import GooglePlacesApi,WeatherApi
import json
import pymongo
from flask_mongoengine import MongoEngine, Document
from flask_googlecharts import GoogleCharts, LineChart

app = Flask(__name__)

charts = GoogleCharts(app)

csrf = CSRFProtect()

csrf.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

app.config['MONGODB_SETTINGS'] = {
    'db': config.DB_NAME,
    'host': config.DB_URL
}
app.config['SECRET_KEY'] = '_no_one_cared_til_i_put_on_the_mask_'
db = MongoEngine(app)


class User(UserMixin, db.Document):
    meta = {'collection': 'Accounts'}
    email = db.StringField(max_length=30)
    location_preferences = db.ListField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
# Forms
class PreferenceForm(FlaskForm):
    area = StringField('locations',  validators=[InputRequired(), Length(max=100)])


# Google Authentication code
oauth = OAuth()
GOOGLE_CLIENT_ID = config.Google_Client_ID
GOOGLE_CLIENT_SECRET = config.Google_Client_Secret
REDIRECT_URI = '/oauth2callback'
SECRET_KEY = 'SOMETHINGRANDOM_IHATEOAUTH'
google = oauth.remote_app('google',
base_url='https://www.google.com/accounts/',
authorize_url='https://accounts.google.com/o/oauth2/auth',
request_token_url=None,
request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
'response_type': 'code'},
access_token_url='https://accounts.google.com/o/oauth2/token',
access_token_method='POST',
access_token_params={'grant_type': 'authorization_code'},
consumer_key=GOOGLE_CLIENT_ID,
consumer_secret=GOOGLE_CLIENT_SECRET)
access_token = [""]

@app.route('/Googlelogin')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for("landing_page"))

@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route("/")
def landing_page():
    access_token = session.get('access_token')
    ## Check if user is logged in or not
    if access_token is None:
        return redirect(url_for('Login'))
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth '+access_token}
    req = URLLib_request.Request('https://www.googleapis.com/oauth2/v1/userinfo',headers= headers)
    try:
        opener = URLLib_request.build_opener()
        res = opener.open(req)
        result =  json.loads(res.read().decode('utf-8'))["email"]
        session["email"] = result
    except error.URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('Login'))
        return res.read()
    ## Check if user is first time login or not
    existing_user = User.objects(email=session.get("email")).first()
    if existing_user is None:
        return redirect(url_for('RegisterPreference'))
    else:
        return redirect(url_for('LoadPreference'))
    return redirect(url_for('RegisterPreference'))

@app.route("/RegisterPreference")
def RegisterPreference():
    Name = None
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('Login'))
    try:
        Name = session.get("email").split("@")[0]
    except Exception as e:
        Name = None
    form = PreferenceForm()
    return render_template("register_preference.html", form = form, loggedin = True, name = Name)

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return redirect(url_for('RegisterPreference'))
        else:
            return render_template('login.html', Homepage = "active")

@app.route('/logout', methods = ['GET'])
def logout():
    del session['access_token']
    logout_user()
    return redirect(url_for("Login"))



@app.route('/LoadPreference', methods = ['GET' , 'POST'])
def LoadPreference():
    try:
        Name = None
        access_token = session.get('access_token')
        if access_token is None:
            return redirect(url_for('Login'))
        if request.method == "POST":
            existing_user = User.objects(email=session.get("email")).first()
            data = request.form['area']
            result = HandleRequestData(data)
            if existing_user is None:
                newUser = User(email=session.get("email"), location_preferences = result.keys()).save()
            else:
                existing_user.update(location_preferences=result.keys())
            try:
                Name = session.get("email").split("@")[0]
            except Exception as e:
                Name = None
            chartdata = MultipleTemp(data)
            chartnames = []
            for dat in chartdata:
                CHART = LineChart(dat.strip().replace(" ", "_"), options={'title': 'Humidity vs Day'})
                CHART.add_column("number", "Day")
                CHART.add_column("number", "Humidity")
                CHART.add_rows(chartdata[dat])
                chartnames.append(dat.strip().replace(" ", "_"))
                charts.register(CHART)
            return render_template("load_preferences.html", data = result,loggedin=True,name = Name, onLoadPreferencesPage = True,chartnames =  chartnames)
        else:
            existing_user = User.objects(email=session.get("email")).first()
            if existing_user is None:
                return redirect(url_for('RegisterPreference'))
            else:
                data = existing_user.location_preferences
                result = HandleRequestData(data)
                Name = None
                chartdata = MultipleTemp(data)
                chartnames = []
                for dat in chartdata:
                    CHART = LineChart(dat.strip().replace(" ", "_"), options={'title': 'Humidity vs Day'})
                    CHART.add_column("number", "Day")
                    CHART.add_column("number", "Humidity")
                    CHART.add_rows(chartdata[dat])
                    chartnames.append(dat.strip().replace(" ", "_"))
                    charts.register(CHART)
                return render_template("load_preferences.html", data = result,loggedin=True,name = Name , onLoadPreferencesPage = True,chartnames =  chartnames )
    except Exception as e:
        return redirect(url_for("exception_error"))


@app.errorhandler(404)
def page_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
@app.route('/error', methods = ['GET'])
def exception_error():
    return render_template('500.html'), 500

def HandleRequestData(data):
    result = {}
    if isinstance(data,str):
        for dat in data.split(','):
            temp =  WeatherApi.returnWeatherData(GooglePlacesApi.get_coords(dat))
            result[dat] = {"Temperature" : temp.temperature, "Humidity" : temp.humidity}
        return result
    elif isinstance(data,list):
        for dat in data:
            temp =  WeatherApi.returnWeatherData(GooglePlacesApi.get_coords(dat))
            result[dat] = {"Temperature" : temp.temperature, "Humidity" : temp.humidity}
    return result

def MultipleTemp(data):
    result = {}
    count = 0
    if isinstance(data,str):
        for dat in data.split(','):
            count = 0
            res = []
            temp =  WeatherApi.returnWeatherDataforpast(GooglePlacesApi.get_coords(dat))
            for DATA in temp.data:
                res.append([count,DATA.humidity])
                count+=1
            result[dat] = res
        return result
    elif isinstance(data,list):
        for dat in data:
            count = 0
            res = []
            temp =  WeatherApi.returnWeatherDataforpast(GooglePlacesApi.get_coords(dat))
            for DATA in temp.data:
                res.append([count,DATA.humidity])
                count+=1
            result[dat] = res
        return result

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
