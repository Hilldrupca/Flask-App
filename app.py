from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    print(url_for('recipe_builder'))
    return render_template('home.html')

@app.route('/recipebuilder')
def recipe_builder():
    return render_template('recipe-builder.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/test')
def test():
    return 'test'

if __name__ == '__main__':
    app.run(debug=True)
