from app import app, db
from flask import render_template

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Welcome')

@app.route('/check-in')
def check_in():
    return render_template('checkin.html', title='Early Check-In')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html', title='Assessment')
