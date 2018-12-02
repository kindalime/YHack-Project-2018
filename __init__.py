from flask import Flask, render_template, request
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
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

    db = SQLAlchemy(app)

    print("b")

    class Restaurant(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        google_id = db.Column(db.String(120))
        name = db.Column(db.String(120))
        address = db.Column(db.String(180), unique=True)
        types = db.Column(ARRAY(db.String(30)))
        lat = db.Column(db.Float)
        lng = db.Column(db.Float)
        rating = db.Column(db.Float)
        rating_n = db.Column(db.Float)
        international_phone_number = db.Column(db.String(25))
        time_spent = db.Column(ARRAY(db.Integer))
        current_popularity = db.Column(db.Float)
        pop_mon = db.Column(ARRAY(db.Integer))
        pop_tue = db.Column(ARRAY(db.Integer))
        pop_wed = db.Column(ARRAY(db.Integer))
        pop_thr = db.Column(ARRAY(db.Integer))
        pop_fri = db.Column(ARRAY(db.Integer))
        pop_sat = db.Column(ARRAY(db.Integer))
        pop_sun = db.Column(ARRAY(db.Integer))
        time_mon = db.Column(ARRAY(db.Integer))
        time_tue = db.Column(ARRAY(db.Integer))
        time_wed = db.Column(ARRAY(db.Integer))
        time_thr = db.Column(ARRAY(db.Integer))
        time_fri = db.Column(ARRAY(db.Integer))
        time_sat = db.Column(ARRAY(db.Integer))
        time_sun = db.Column(ARRAY(db.Integer))

        def __repr__(self):
            return '<Restaurant %r>' % self.name

    print("c")

    def make_restaurant(rest):
        return Restaurant(
            rest["id"],
            rest["name"],
            rest["address"],
            rest["types"],
            rest["coordinates"]["lat"],
            rest["coordinates"]["lng"],
            rest["rating"],
            rest["rating_n"],
            rest["international_phone_number"],
            rest["time_spent"],
            rest["current_popularity"],
            rest["popular_times"][0]["data"],
            rest["popular_times"][1]["data"],
            rest["popular_times"][2]["data"],
            rest["popular_times"][3]["data"],
            rest["popular_times"][4]["data"],
            rest["popular_times"][5]["data"],
            rest["popular_times"][6]["data"],
            rest["time_wait"][0]["data"],
            rest["time_wait"][1]["data"],
            rest["time_wait"][2]["data"],
            rest["time_wait"][3]["data"],
            rest["time_wait"][4]["data"],
            rest["time_wait"][5]["data"],
            rest["time_wait"][6]["data"],
        )

    print("d")

    db.create_all()
    db.session.commit()

    print("e")

    for rest in near_restaurants:
        db.session.add(make_restaurant(rest))
    restaurants = Restaurant.query.all()

    print("f")

    print(restaurants)

    return restaurants

if __name__ == "__main__":
    app.run()