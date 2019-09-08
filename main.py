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

from flask import Flask , request,jsonify, redirect,render_template, url_for, session
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Config import config
from flask_oauth import OAuth
from urllib.request import urlopen
from urllib import request as URLLib_request
from urllib import error

app = Flask(__name__)

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
    return render_template("register_preference.html")

@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route("/")
def landing_page():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('Login'))
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth '+access_token}
    req = URLLib_request.Request('https://www.googleapis.com/oauth2/v1/userinfo',headers= headers)
    try:
        opener = URLLib_request.build_opener()
        res = opener.open(req)
        print(res)
    except error.URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('Login'))
        return res.read()
    return redirect(url_for('RegisterPreference'))

@app.route("/RegisterPreference")
def RegisterPreference():
    return render_template("register_preference.html")

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return redirect(url_for('RegisterPreference'))
        else:
            return render_template('Login.html')

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    try:
        del session['access_token']
    except Exception:
        pass
    return redirect("/Login")
