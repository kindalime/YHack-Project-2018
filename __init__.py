# Shout-out to @Jagbox3 for helping with location-fetching!
# This program uses this module: https://github.com/m-wrzr/populartimes

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
    get_restaurants(location)
    return "abcabc"

def get_restaurants(location):
    print("a")

    near_restaurants = popular_times(location)
    restaurants_list = []

    for rest in near_restaurants:
        new_rest = {
            "name": rest["name"],
            "address": rest["address"],
            "bars": rest["bars"],
            "stars": rest["stars"],
            "distance": rest["root_distance"],
        }

        restaurants_list.append(new_rest)

@app.route("/results")
def results():
    return render_template('results.html', restaurants=restaurants_list)

if __name__ == "__main__":
    app.run()
