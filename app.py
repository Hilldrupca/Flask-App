from flask import Flask, render_template, request, jsonify
import nutrition as nu

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/recipebuilder')
def recipe_builder():
    return render_template('recipe-builder.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/search/<string:search>', methods=['GET'])
def search(search):
    return jsonify(nu.foodsearch(search))

if __name__ == '__main__':
    app.run(debug=True)
