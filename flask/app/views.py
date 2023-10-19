from app import app, db
from flask import render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.schema import User, CheckIn
from app.utils import create_gauge_chart, get_predicted_condition, get_recommended_assessment

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Welcome')

@app.route('/check-in', methods=['GET', 'POST'])
def check_in():
    if request.method == "GET":
        items = []
        ci = CheckIn.query.all()
        for c in ci:
            items.append(c.to_dict())
        return render_template('checkin.html', title='Early Check-In', items=items)
    
    # post method
    data = request.form
    age = data.get("age")
    gender = data.get("gender")
    symptoms = data.getlist("symptoms")

    if current_user.is_authenticated:
        age = current_user.age
        gender = current_user.gender

    if int(age) < 13:
        return jsonify({"error": "You must be at least 13 years old to register"})
    
    if len(symptoms) < 1:
        return jsonify({"error": "You must select at least one symptom"})

    selected_language = "English"
    predicted_condition = get_predicted_condition(age, gender, selected_language, symptoms)
    recommended_assessments = get_recommended_assessment(predicted_condition)
    return jsonify(recommended_assessments)

@app.route('/assessments')
def assessments():
    ass = [
        "ADHD", "Alcohol", "Anxiety", "Bipolar", "Depression",
        "Dementia", "Drug", "OCD", "PSQ", "PTSD"
    ]
    return render_template('assessments.html', title='Assessment', ass=ass)

@app.route('/assessment/<string:option>')
def assessment(option):
    ass = {
        "title": "IQCODE Assessment",
        "code": "IQCODE_Assessment",
        "options": [
            {
                "id": 1,
                "name": "IQCODE_Assessment_1", # f"{code}_{id}"
                "prompt": "Does the individual forget recent events?",
                "choices": ["Never", "Rarely", "Sometimes", "Often"]
            },
            {
                "id": 1,
                "name": "IQCODE_Assessment_1", # f"{code}_{id}"
                "prompt": "Does the individual forget recent events?",
                "choices": ["13-24", "25-30", "31-40", "41-45", "45+"]
            }
        ]
    }
    return render_template(
        'assessment.html', 
        title=f"{option} Assessment",
        ass=ass
    )

@app.route('/results', methods=["POST"])
def results():
    res = {
        "title": "ADHD Assessment Score"
    }
    return render_template(
        'results.html', 
        title="Assessment Score", 
        res=res,
        plot=create_gauge_chart(10, max_score=27, assessment_name="ADHD")
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "GET":
        return render_template('register.html', title='Register')
    
    # post method
    username = request.form.get("username").strip()
    age = request.form.get("age")
    gender = request.form.get("gender")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match")
        return render_template('register.html', title='Register')
    
    user = User.query.filter_by(username=username).first()
    if user:
        flash(f"The username {user.username} already exists")
        return render_template('register.html', title='Register')
    
    if len(username) < 4:
        flash("Username must be at least 4 characters")
        return render_template('register.html', title='Register')
    
    if len(password) < 6:
        flash("Password must be at least 6 characters")
        return render_template('register.html', title='Register')
    
    if int(age) < 13:
        flash("You must be at least 13 years old to register")
        return render_template('register.html', title='Register')
    
    user = User(username=username, age=age, gender=gender, password=password)
    db.session.add(user)
    db.session.commit()
    
    flash(f"Welcome, {username}. Please login to continue.")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "GET":
        return render_template('login.html', title='Login')
    
    # post method
    username = request.form.get("username").strip()
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return render_template('index.html', title='Welcome')
    else:
        flash("Incorrect username or password")
        return render_template('login.html', title='Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/scores')
@login_required
def scores():
    return render_template('scores.html', title='Scores')
