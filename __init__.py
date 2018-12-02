# Shout-out to @Jagbox3 for helping with location-fetching!
# This program uses this module: https://github.com/m-wrzr/populartimes

from flask import Flask, render_template, request
import random
from pop_times import popular_times

app = Flask(__name__)
location = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/location", methods=['POST'])
def location():
    global location
    location = [request.get_json()['latitude'], request.get_json()['longitude']]
    print(location)
    return "Redirecting..."

def get_restaurants(location):
    near_restaurants = popular_times(location)
    global restaurants_list
    restaurants_list = []

    for rest in near_restaurants:
        new_rest = {
            "name": rest["name"],
            "address": rest["address"],
            "bars": rest["bars"],
            "stars": rest["stars"],
            # "distance": rest["root_distance"],
        }

        restaurants_list.append(new_rest)

    return restaurants_list

@app.route("/results")
def results():
    return render_template('results.html', restaurants = get_restaurants(location))

@app.route("/results_loader")
def results_loader():
    return render_template("results_loader.html", name = random.randint(0, 9999))

if __name__ == "__main__":
    app.run()
