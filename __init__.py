from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from pop_times import popular_times

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name = random.randint(0, 9999))


@app.route("/location", methods=['POST'])
def location():
    near_restaurants = popular_times((request.get_json()['latitude'], request.get_json()['longitude']))

    db = SQLAlchemy(app)

    class Restaurant(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        google_id = db.Column(db.String(120))
        name = db.Column(db.String(120))
        address = db.Column(db.String(180), unique=True)
        types = db.Column(db.ARRAY(String))
        lat = db.Column(db.Float)
        lng = db.Column(db.Float)
        rating = db.Column(db.Float)
        rating_n = db.Column(db.Float)
        international_phone_number = db.Column(db.String(25))
        time_spent = db.Column(db.ARRAY(db.Integer))
        current_popularity = db.Column(db.Float)
        pop_mon = db.Column(db.ARRAY(Integer))
        pop_tue = db.Column(db.ARRAY(Integer))
        pop_wed = db.Column(db.ARRAY(Integer))
        pop_thr = db.Column(db.ARRAY(Integer))
        pop_fri = db.Column(db.ARRAY(Integer))
        pop_sat = db.Column(db.ARRAY(Integer))
        pop_sun = db.Column(db.ARRAY(Integer))
        time_mon = db.Column(db.ARRAY(Integer))
        time_tue = db.Column(db.ARRAY(Integer))
        time_wed = db.Column(db.ARRAY(Integer))
        time_thr = db.Column(db.ARRAY(Integer))
        time_fri = db.Column(db.ARRAY(Integer))
        time_sat = db.Column(db.ARRAY(Integer))
        time_sun = db.Column(db.ARRAY(Integer))

        def __repr__(self):
            return '<Restaurant %r>' % self.name

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

    db.create_all()
    db.session.commit()

    for rest in near_restaurants:
        db.session.add(make_restaurant(rest))
    restaurants = Restaurant.query.all()
    print(restaurants)

    return "Hello, world!"