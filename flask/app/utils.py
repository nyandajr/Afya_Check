""" functions ive stollen from the original code"""

import os
import joblib
import plotly.graph_objs as go
from plotly.graph_objects import Layout
from app import app

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

    layout = Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': f"Your {assessment_name} Score", 'font': {'size': 24, 'color': 'white'}},
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
    ),
    layout=layout
    )

    # Enhancements
    if score <= 0.3 * max_score:
        level = "Low"
    elif score <= 0.7 * max_score:
        level = "Medium"
    else:
        level = "High"
    
    fig.add_annotation(dict(font=dict(color="white", size=30),
        x=0.5,
        y=0.5,
        showarrow=False,
        text=f"{level} Level",
        textangle=0,
        xanchor="center",
        yanchor="middle"
    ))
    
    return fig.to_html(full_html=False)

def get_recommended_assessment(predicted_condition):
    # Mapping of predicted conditions to recommended assessments with lowercase keys
    condition_to_assessment_map = {
        "depression": ["Depression", "Anxiety", "Bipolar"],
        "anxiety": ["Anxiety", "Depression", "PTSD"],
        "bipolar disorder": ["Depression", "Bipolar"],
        "schizophrenia": ["Depression", "PSQ"],
        "substance use disorder": ["Drug", "Alcohol", "Depression"],
        "dementia":["Dementia"]
    }
    
    return condition_to_assessment_map.get(predicted_condition, [])

def get_predicted_condition(age, gender, selected_language, selected_symptoms):
    """
    Use the provided information to predict the mental health condition.
    """
    # Process the selected symptoms into a format suitable for the model
    processed_symptoms = ' '.join(selected_symptoms)
    
    path = os.path.join(app.root_path, 'model')

    # Load the trained SVM model and other preprocessing objects
    svm_model = joblib.load(os.path.join(path, 'svm_model.joblib'))
    tfidf_vectorizer = joblib.load(os.path.join(path, 'tfidf_vectorizer.joblib'))
    label_encoder = joblib.load(os.path.join(path, 'label_encoder.joblib'))

    # TF-IDF Encoding for processed symptoms
    user_input_tfidf = tfidf_vectorizer.transform([processed_symptoms])

    # Gender encoding
    if gender == 'Male':
        gender_encoded = [1, 0]
    else:
        gender_encoded = [0, 1]

    # Combine user inputs
    user_inputs = user_input_tfidf.toarray()[0].tolist() + gender_encoded + [age]

    # Make predictions using the SVM modelrender_assessments_page
    svm_prediction = svm_model.predict([user_inputs])
    svm_predicted_condition = label_encoder.inverse_transform(svm_prediction)[0]

    return svm_predicted_condition
