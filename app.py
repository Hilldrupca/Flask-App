from flask import Flask, render_template, request, jsonify, session
from flask_login import LoginManager, logout_user
from user import User
import nutrition as nu
import pickle

app = Flask(__name__)
app.secret_key = b'@;\xc3\xbaR\x98J\xd2\x86\xb6J\xa8\xee\x9a\r\xba'
app.SESSION_TYPE='filesystem'
login_manager = LoginManager()
login_manager.init_app(app)

directory = {'/': 'home.html', '/recipebuilder': 'recipe-builder.html', '/account': 'account.html'}

@login_manager.user_loader
def load_user(user_id):
    usr = User(user_id)
    if usr.username:
        return usr
    return None

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/recipebuilder')
def recipe_builder():
    profiles = pickle.load(open('profiles.p','rb'))
    return render_template('recipe-builder.html', macros= nu.macros,\
            vitamins= nu.vitamins, minerals= nu.minerals, p= profiles)

@app.route('/account')
def account():
    print(session.items(),flush=True)
    return render_template('account.html')

@app.route('/foodsearch/<string:search>')
def search(search):
    return jsonify(nu.foodsearch(search))

@app.route('/nutritiondata/<string:dbnum>')
def nutrition_data(dbnum):
    return jsonify(nu.nutdata(dbnum))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usr = User()
        usr.validate_credentials(username, password)
        
        if usr.is_authenticated:
            from flask_login import login_user
            login_user(usr)
            
            refer = directory.get(request.referrer.split('http://127.0.0.1:5000')[1])
                
            return render_template('home.html')
        
@app.route('/logout')
def logout():
    logout_user()
    return render_template('home.html')

@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    return 'hi'
