from flask import Flask, render_template, request, jsonify
from weather import main as get_weather
from cities import is_valid_city
from dotenv import load_dotenv
import os
import json
import openai

load_dotenv()
key = os.getenv('MAPS_KEY')
openai_key = os.getenv('OPENAI_KEY')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        data = get_weather(city, state, country)
    return render_template('index.html', data=data, key=key)

@app.route('/get-weather')
def get_weather_data():
    cities = request.args.getlist('city')
    weather_data = []
    for city in cities:
        if is_valid_city(city):
            weather_data = get_weather(city, "", "")
            if weather_data:
                response_data = {
                    'main': weather_data.main,
                    'description': weather_data.description,
                    'icon': weather_data.icon,
                    'temperature': weather_data.temperature,
                    'lat': weather_data.lat,
                    'lng': weather_data.lng
                }
                return json.dumps(response_data)
            else:
                return 'Weather data not available'
        else:
            pass

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    openai.api_key = openai_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
    )
    reply = response.choices[0].text.strip()
    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True)