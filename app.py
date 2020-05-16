from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/recipebuilder/')
def recipe_builder():
    return render_template('recipe-builder.html')

if __name__ == '__main__':
    app.run(debug=True)
