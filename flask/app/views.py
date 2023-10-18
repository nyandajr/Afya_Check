from app import app, db
from flask import render_template

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Welcome')
