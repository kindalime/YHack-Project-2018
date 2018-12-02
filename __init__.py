from flask import Flask, render_template, request
import random
from pop_times import popular_times

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

@app.route('/')
def index():
    return render_template('index.html', name = random.randint(0, 9999))


@app.route("/location", methods=['POST'])
def location():
    location = [request.get_json()['latitude'], request.get_json()['longitude']]
    make_database(location)
    return "abcabc"

def make_database(location):
    print("a")
    near_restaurants = popular_times(location)

