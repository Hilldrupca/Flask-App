from flask import Flask, render_template, request, jsonify
import nutrition as nu
import pickle

app = Flask(__name__)


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
    return render_template('account.html')

@app.route('/foodsearch/<string:search>')
def search(search):
    return jsonify(nu.foodsearch(search))

@app.route('/nutritiondata/<string:dbnum>')
def nutrition_data(dbnum):
    return jsonify(nu.nutdata(dbnum))

if __name__ == '__main__':
    app.run(debug=True)
