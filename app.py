from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/recipebuilder/')
def recipe_builder():
    return render_template('recipe-builder.html')

@app.route('/account/')
def account():
    return render_template('account.html')

@app.route('/sign-in/')
def sign_in():
    return render_template('sign-in.html')

@app.route('/create-account/')
def create_account():
    return render_template('create-account.html')

if __name__ == '__main__':
    app.run(debug=True)
