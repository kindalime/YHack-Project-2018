from flask import render_template, jsonify, request
import os
import random
from app import app

@app.route('/')
def index():
    return render_template('index.html', name = random.randint(0, 9999))


@app.route("/location", methods=['POST'])
def location():
    print(request.get_json()['latitude'])
    print(request.get_json()['longitude'])
    return "Hello!"
