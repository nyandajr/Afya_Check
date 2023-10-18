from app import app, db
from flask import render_template, flash
import plotly.graph_objs as go

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Welcome')

@app.route('/check-in')
def check_in():
    items = [
        {
            "id": 1,
            "title": "Consistence fear or worries",
            "options": [
                {
                    "id": 1,
                    "text": "Often feeling overwhelmed with irrational fears, avoiding certain places \
                        due to worries, and frequently feeling scared without a clear reason"
                },
                {
                    "id": 2,
                    "text": "struggles with the fear of experiencing panic attacks"
                },
                {
                    "id": 3,
                    "text": "displays visible trembling or shaking without physical exertion"
                },
                {
                    "id": 4,
                    "text": "struggles with fears of being judged for expressing emotions"
                }
            ]
        },
        {
            "id": 2,
            "title": "Experience of unreal perceptions",
            "options": [
                {
                    "id": 1,
                    "text": "Often hearing voices others can't, being suspicious of others, and \
                        feeling that others can read your thoughts"
                },
                {
                    "id": 2,
                    "text": "exhibits signs of magical thinking, believing in supernatural forces \
                        affecting their lives"
                },
                {
                    "id": 3,
                    "text": "struggles to distinguish between hallucinations and reality"
                }
            ]
        },
        {
            "id": 3,
            "title": "Challenges with memory and cognition",
            "options": [
                {
                    "id": 1,
                    "text": "Challenged in reasoning and problem solving, forgetting names, and frequently unaware of the current date or time"
                }
            ]
        },
        {
            "id": 4,
            "title": "Persistent sadness or hopelessness",
            "options": [
                {
                    "id": 1,
                    "text": "Often contemplating death, consistently feeling anxious, and experiencing \
                         disruptions in appetite"
                },
                {
                    "id": 2,
                    "text": "suffers from disrupted sleep patterns and early morning awakenings"
                },
                {
                    "id": 3,
                    "text": "experiences persistent thoughts of death and suicide"
                },
                {
                    "id": 4,
                    "text": "shows signs of neglecting personal hygiene and appearance"
                }
            ]
        },
        {
            "id": 5,
            "title": "Reliance on substance use",
            "options": [
                {
                    "id": 1,
                    "text": "Difficult to manage tasks without drugs or alcohol, prioritizing drug use, and feeling a constant need to use substances"
                }
            ]
        },
        {
            "id": 6,
            "title": "Extreme Mood Swings",
            "options": [
                {
                    "id": 1,
                    "text": "Experiencing overly happy and sad periods, being very active or talkative, and frequently engaging in risky activities"
                }
            ]
        }
    ]
    return render_template('checkin.html', title='Early Check-In', items=items)

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

def create_gauge_chart(score, max_score=27, assessment_name="Assessment"):
    # Determine tick interval based on max_score
    if max_score <= 10:
        tick_interval = 1
    elif max_score <= 20:
        tick_interval = 2
    elif max_score <= 50:
        tick_interval = 5
    else:
        tick_interval = 10

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': f"Your {assessment_name} Score", 'font': {'size': 24}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_score], 'tickvals': list(range(0, max_score + 1, tick_interval)), 'ticktext': [str(i) for i in range(0, max_score + 1, tick_interval)]},
            'steps': [
                {'range': [0, 0.3*max_score], 'color': 'green'},
                {'range': [0.3*max_score, 0.7*max_score], 'color': 'yellow'},
                {'range': [0.7*max_score, max_score], 'color': 'red'}
            ],
            'bar': {'color': 'black'}
        }
    ))

    fig.update_layout(plot_bgcolor='rgb(45, 52, 65)')

    # Enhancements
    if score <= 0.3 * max_score:
        level = "Low"
    elif score <= 0.7 * max_score:
        level = "Medium"
    else:
        level = "High"
    
    fig.add_annotation(dict(font=dict(color="black", size=30),
        x=0.5,
        y=0.5,
        showarrow=False,
        text=f"{level} Level",
        textangle=0,
        xanchor="center",
        yanchor="middle"
    ))
    
    return fig.to_html(full_html=False)

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
    flash("The username laizer already exists")
    return render_template('register.html', title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    flash("Incorrect username or password")
    return render_template('login.html', title='Login')
