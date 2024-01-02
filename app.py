from flask import Flask, render_template, request, redirect, url_for
from fuzzywuzzy import fuzz
import requests

app = Flask(__name__)

MEAL_API_URL = 'https://www.themealdb.com/api/json/v1/1/search.php'
MEAL_DETAILS_API_URL = 'https://www.themealdb.com/api/json/v1/1/lookup.php'

def fetch_meals(query):
    params = {'s': query}
    response = requests.get(MEAL_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json().get('meals', [])
        return data
    else:
        return []

def fetch_meal_details(meal_id):
    params = {'i': meal_id}
    response = requests.get(MEAL_DETAILS_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json().get('meals', [])
        return data[0] if data else None
    else:
        return None

def fuzzy_search(query, meals):
    results = []
    for meal in meals:
        similarity_score = fuzz.partial_ratio(query.lower(), meal['strMeal'].lower())
        if similarity_score >= 70: 
            results.append(meal)
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            meals = fetch_meals(query)
            return redirect(url_for('search_results', query=query))

    return render_template('index.html', meals=[], query='')

@app.route('/search_results/<query>')
def search_results(query):
    meals = fetch_meals(query)
    results = fuzzy_search(query, meals)
    return render_template('search_results.html', results=results, query=query)

@app.route('/meal/<meal_id>')
def meal_detail(meal_id):
    meal = fetch_meal_details(meal_id)
    return render_template('meal_detail.html', meal=meal)

if __name__ == '__main__':
    app.run(debug=True)
