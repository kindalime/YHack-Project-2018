# Shout-out to @Jagbox3 for helping with location-fetching!
# This program uses this module: https://github.com/m-wrzr/populartimes

from flask import Flask, render_template, request
import random
import pop_times

app = Flask(__name__)
loc = []
restaurants_list = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/location", methods=['POST'])
def location():
    global loc
    loc = [request.get_json()['latitude'], request.get_json()['longitude']]
    return "Redirecting..."

def get_restaurants(loc):
    near_restaurants = pop_times.append_new_info(loc, pop_times.popular_times(loc))
    global restaurants_list
    restaurants_list = []

    for rest in near_restaurants:
        new_rest = {
            "name": rest["name"],
            "address": rest["address"],
            "bars": rest["bars"],
            "rating": rest["rating"],
            "stars": rest["stars"],
            "file_exists": rest["file_exists"],
        }

        restaurants_list.append(new_rest)

    return restaurants_list

@app.route("/results")
def results():
    return render_template('results.html', restaurants = get_restaurants(loc))

@app.route("/results_loader")
def results_loader():
    return render_template("results_loader.html", name = random.randint(0, 9999))

@app.route('/rating', methods = ['GET'])
def rating():
   return render_template('results.html', restaurants = pop_times.sort_rating(restaurants_list))

@app.route('/business')
def business():
   return render_template('results.html', restaurants = pop_times.sort_busy(restaurants_list))

@app.route('/alphabetical')
def alphabetical():
   return render_template('results.html', restaurants = pop_times.sort_alphabet(restaurants_list))

@app.route('/distance')
def distance():
   return render_template('results.html', restaurants = pop_times.sort_distance(restaurants_list))

@app.route('/dist_1')
def distance_1():
   return render_template('results.html', restaurants = pop_times.filter_distance_1(restaurants_list))

@app.route('/dist_5')
def distance_5():
   return render_template('results.html', restaurants = pop_times.filter_distance_5(restaurants_list))

@app.route('/dist_10')
def distance_10():
   return render_template('results.html', restaurants = pop_times.filter_distance_10(restaurants_list))

@app.route('/rating_5')
def rating_5():
   return render_template('results.html', restaurants = pop_times.filter_rating_4to5(restaurants_list))

@app.route('/rating_4')
def rating_4():
   return render_template('results.html', restaurants = pop_times.filter_rating_3to4(restaurants_list))

@app.route('/rating_3')
def rating_3():
   return render_template('results.html', restaurants = pop_times.filter_rating_0to3(restaurants_list))

if __name__ == "__main__":
    app.run()
