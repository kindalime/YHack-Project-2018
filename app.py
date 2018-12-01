# Shout-out to @Jagbox3 for helping me with location-fetching!

from flask import Flask, jsonify, render_template, request
import os
import random
app = Flask(__name__)

from flask import request


@app.route('/')
def index():
    return render_template('index.html', name = random.randint(0, 9999))


@app.route("/location", methods=['POST'])
def location():
    print(request.get_json()['latitude'])
    print(request.get_json()['longitude'])
    return "Hello!"