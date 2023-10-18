from app import app, db
from flask import render_template

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
                "prompt": "Does the individual forget recent events?"
            },
            {
                "id": 1,
                "name": "IQCODE_Assessment_1", # f"{code}_{id}"
                "prompt": "Does the individual forget recent events?"
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
    return render_template('results.html')
