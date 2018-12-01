from flask import render_template
from app import app

@app.route('/')
def home():
    return 'get this bread'

@app.route('/canon')
def search():
    return render_template('canon.html')
