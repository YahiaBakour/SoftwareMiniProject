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
    except error.URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('Login'))
        return res.read()
    return redirect(url_for('Login'))

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return redirect(url_for('RegisterPreferences'))
        else:
            return render_template('Login.html')