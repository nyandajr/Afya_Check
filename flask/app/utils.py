""" functions ive stollen from the original code"""

import os
import joblib
import openai
from dotenv import load_dotenv
import plotly.graph_objs as go
from plotly.graph_objects import Layout
from app import app

def create_gauge_chart(score, max_score=27, assessment_name="Assessment", selected_language="English"):
    # Determine tick interval based on max_score
    if max_score <= 10:
        tick_interval = 1
    elif max_score <= 20:
        tick_interval = 2
    elif max_score <= 50:
        tick_interval = 5
    else:
        tick_interval = 10

    layout = Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--white-color)'))
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={
            'text': f"Alama zako {assessment_name}" if selected_language=="Swahili" else f"Your {assessment_name} Score", 
            'font': {'size': 24, 'color': 'var(--white-color)'}},
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
        if selected_language == "Swahili":
            level = "Chini"
    elif score <= 0.7 * max_score:
        level = "Medium"
        if selected_language == "Swahili":
            level = "Kati"
    else:
        level = "High"
        if selected_language == "Swahili":
            level = "Juu"
    
    fig.add_annotation(dict(font=dict(color="var(--white-color)", size=30),
        x=0.5,
        y=0.5,
        showarrow=False,
        text=f"Kiwango cha {level}" if selected_language=="Swahili" else f"{level} Level",
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

def age_group_from_age(age:int):
    if age >= 15 and age <= 24:
        return "15-24"
    elif age >= 25 and age <= 34:
        return "25-34"
    elif age >= 35 and age <= 44:
        return "35-44"
    elif age >= 45 and age <= 54:
        return "45-54"
    elif age >= 55:
        return "55+"

def initialize_openai():
    path = os.path.join(app.root_path, '.env')
    load_dotenv(path)
    openai.api_key = os.getenv("API_KEY")
    
    load_dotenv(path)
    api_key = os.getenv("API_KEY")
    print(f"API Key Value: {api_key}")  # This will print the fetched API key value

    openai.api_key = api_key


def get_gpt3_response(prompt, language="English", temperature=0.3):
    if language == "Swahili":
        prompt += " Please respond in Swahili."

    try:
        # Use the chat model endpoint for GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You are a mental health assistant with knowledge about various mental health conditions. Provide responses that are sensitive, empathetic, and non-diagnostic."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        if language == "Swahili":
            return "Samahani, tatizo limejitokeza. Tafadhali jaribu tena baadae."
        return "Sorry, there was an issue fetching a response. Please try again later."
    
def gpt_response_to_html(gpt_response):
    # Split the GPT response into paragraphs based on the numbers (e.g., "1. ", "2. ", etc.)
    paragraphs = gpt_response.split('\n')
    
    # Initialize the HTML content
    html_content = "<div>"
    
    # Iterate through the paragraphs and add them to the HTML content
    for paragraph in paragraphs:
        if paragraph.strip():
            # Extract the number and text content
            parts = paragraph.split('. ', 1)
            if len(parts) == 2:
                number, text = parts
                html_content += f"<p><strong>{number}. </strong>{text}</p>"
            else:
                # If there's no number, just add the text
                html_content += f"<p>{paragraph}</p>"
    
    # Close the HTML container
    html_content += "</div>"
    
    return html_content

def create_gpt_prompt(assessment, score, result_text, selected_language="English"):
    if assessment["title"] == "Bipolar Assessment (YMRS)":
        return f'''gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have completed the bipolar assessment, scoring {score} out of {assessment['max_score']}, indicating: '{result_text}'.
        1. Provide an empathetic response based on my  score and tell me if my score is high or low.
        2. Define bipolar disorder in a broader scope.
        3. List negative symptoms of bipolar disorder and explain how it affects daily life.
        4. Offer insights and coping strategies and natural ways for managing bipolar disorder.
        5. Commend me for undertaking the assessment.
        6. If my score is high encourage me to go to the hospital.
        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''
    elif assessment["title"] == "Anxiety Assessment (GAD-7)":
        return f''' gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have taken an anxiety assessment, scoring {score} out of a maximum of {assessment['max_score']}, suggesting: '{result_text}'.
        1. Provide an empathetic response based on my score, mentioning the score out of 21.
        2. Explain the nature of anxiety and the examples people with anxieties experience
        3. List detailed negative impacts of untreated anxiety.
        4. Offer coping strategies and natural ways  into managing anxiety.

        5. Mention actions one should and shouldn't undertake when interacting with someone experiencing anxiety.
        """
        '''
    elif assessment["title"] == "AUDIT (Alcohol Use Disorders Identification Test)":
        return f'''gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have completed the AUDIT assessment, scoring {score} out of {assessment['max_score']}, indicating: '{result_text}'.
        1. Offer an empathetic response based on my score, and acknowledge my score out of 40.
        2. Explain Substance Alcohol Use Disorder. and early signs of this problem.
        3. List detailed negative consequences of untreated alcohol addiction in daily life.
        4. Offer coping strategies, natural ways and insights into managing alcohol addiction.
        5. Commend me for undertaking the assessment.
        7. Advise and encourage me to seek hospital help if my score is high.
        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''
    elif assessment["title"] == "OCD Assessment (Y-BOCS)":
        return f'''gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have completed the OCD assessment, achieving a score of {score}, leading to the interpretation: '{result_text}'.
        1. Based on my score, provide an appropriate empathetic response. And tell me if my score is high or low or moderate. If it is high advise me to go to the hospital.
        2. Define Obsessive-Compulsive Disorder (OCD) and provide an example of its symptoms especially early symptoms.
        3. Detail negative  impacts of OCD on daily life if not addressed.
        4. Suggest detailed natural coping mechanisms and strategies for managing OCD.
        5. Acknowledge me on my  efforts in taking the assessment.
        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''
    elif assessment["title"] == "PTSD Assessment (Post-Traumatic Stress Disorder)":
        return f'''gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have completed the PTSD assessment, achieving a score of {score}, which suggests: '{result_text}'.
        1. Define Post-Traumatic Stress Disorder (PTSD) and provide examples of its symptoms especially early signs.
        2. Detail negative significant impacts of untreated PTSD on an individual's daily life.
        3. Offer insights and advice tailored for the user's score and potential condition.
        4. Acknowledge the user's initiative in taking the assessment.
        5. Provide 10 guidelines on supporting individuals with PTSD, keeping in mind Tanzanian cultural contexts.
        6. Recommend dos and don'ts when interacting with someone diagnosed with PTSD.
        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''
    elif assessment["title"] == "DAST-10 Assessment (Drug Abuse Screening Test)":
        return f"""
            As an informed mental health assistant:
            I have completed the DAST-10 drug abuse assessment, obtaining a score of {score} out of {assessment['max_score']}. 
            1. Greet me and Tell me if my score is high or low or moderate.
            2. Define Drug Abuse Disorder and provide a brief overview and early signs and symptoms.
            3. List detailed negative significant impacts of unchecked drug abuse on one's daily life and health.
            4. Offer insights, coping strategies, and advice tailored to the  score and potential condition.
            5. Acknowledge the my  effort and initiative in taking the assessment.
            6.If my score is too high advise me to vist hospital immediately
            """
    elif assessment["title"] == "ASRS-v1.1 Assessment (Adult ADHD Self-Report Scale)":
        return f"""
            As an informed mental health assistant:
            I have completed ADHD assessment, obtaining a score of {score} out of {assessment['max_score']}.
            1. Based on the score tell me if my score is high or low
            2. Define ADHD  and provide a brief overview.
            3. List negative significant impacts of unchecked ADHD on one's daily life and health.
            4. Offer insights, natural coping strategies, and advice tailored to the user's score and potential condition.
            5. Acknowledge my effort and initiative in taking the assessment.
            6. Suggest  strategies to support individuals struggling with drug addiction.
            """
    elif assessment["title"] == "Psychosis Screening Questionnaire (PSQ) Assessment":
        return f'''
        As a knowledgeable mental health assistant:
        I have taken  a Shizophrenia assessment and achieved a score of {score} out of a maximum possible score of {assessment['max_score']}. 

        1) Tell me if my score is high or low
        2) What is Shizophrenia and what are the symptoms and early signs.
        3)Encourage me to go to the hospital for detailed check up

        Lastly, acknowledge my  initiative in taking the assessment and emphasize the importance of mental well-being.
        '''
    elif assessment["title"] == "Depression Assessment (PHQ-9)":
        return f'''As a helpful mental health assistant, consider the following: 
        I have taken a depression assessment and scored {score} out of a maximum of {assessment['max_score']}, suggesting: '{result_text}'.
        1. Provide an empathetic response based on my  score and tell me if my score is high, low or moderate.
        2. Explain what depression is and its potential consequences if not addressed.
        3. Offer coping natural strategies and insights.
        4. List pieces of advice on supporting individuals with depression, reflecting Tanzanian culture.
        5. Mention things one should and shouldn't do when interacting with someone struggling with depression.
        6.Congratulate me for taking this test. And if my score is high advice me to go to the hospital.
        '''
    elif assessment["title"] == "IQCODE Assessment":
        return f'''gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have completed the IQCODE(Cognitive Decline)  assessment for my relative, scoring {score} out of {assessment['max_score']}, indicating: '{result_text}'.
        1. Provide an empathetic response based on their score.
        2. Explain the concept of cognitive decline.
        3. List  common signs especially early signs of cognitive decline and their impact on daily life.
        4. Offer tips for maintaining cognitive health.
        5. Commend the user for taking the assessment.
        6. Suggest 10 strategies for supporting individuals with cognitive decline.
        7. Highlight dos and don'ts when interacting with someone experiencing cognitive decline and emphasize on going to the hospital
        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''

def create_result_text(assessment, score, selected_language="English"):
    if assessment["title"] == "Bipolar Assessment (YMRS)":
        if selected_language == "English":
            if score <= 12:
                return "Your score suggests Minimal or no manic symptoms."
            elif score <= 20:
                return "Your score suggests Mild manic symptoms."
            elif score <= 30:
                return "Your score suggests Moderate manic symptoms."
            else:
                return "Your score suggests Severe manic symptoms."
        elif selected_language == "Swahili":
            if score <= 12:
                return "Alama zako zinaonyesha dalili ndogo au hakuna dalili za bipolar."
            elif score <= 20:
                return "Alama zako zinaonyesha dalili za wastani za bipolar."
            elif score <= 30:
                return "Alama zako zinaonyesha dalili kali za bipolar."
            else:
                return "Alama zako zinaonyesha dalili kali sana za bipolar."


    elif assessment["title"] == "Anxiety Assessment (GAD-7)":
        interpretations = {
            "English": [
                "Your score suggests Minimal anxiety.",
                "Your score suggests Mild anxiety.",
                "Your score suggests Moderate anxiety.",
                "Your score suggests Severe anxiety."
            ],
            "Swahili": [
                "Alama zako zinaonyesha wasiwasi mdogo.",
                "Alama zako zinaonyesha wasiwasi wa wastani.",
                "Alama zako zinaonyesha wasiwasi wa kati.",
                "Alama zako zinaonyesha wasiwasi mkubwa."
            ]
        }
        boundaries = [4, 9, 14]

        for i, boundary in enumerate(boundaries):
            if assessment["max_score"] <= boundary:
                return interpretations[selected_language][i]
        else:
            return interpretations[selected_language][3]
        

    elif assessment["title"] == "AUDIT (Alcohol Use Disorders Identification Test)":
        if selected_language == "English":
            if score <= 7:
                return "Your score suggests Low level of alcohol problems or dependence."
            elif score <= 15:
                return "Your score suggests Medium level of alcohol problems or dependence."
            elif score <= 19:
                return "Your score suggests High level of alcohol problems or dependence."
            else:
                return "Your score suggests Very High level of alcohol problems or dependence."
        elif selected_language == "Swahili":
            if score <= 7:
                return "Alama zako zinaonyesha kiwango cha chini cha uraibu wa pombe."
            elif score <= 15:
                return "Alama zako zinaonyesha kiwango cha wastani cha uraibu wa pombe."
            elif score <= 19:
                return "Alama zako zinaonyesha kiwango cha juu cha uraibu."
            else:
                return "Alama zako zinaonyesha kiwango cha juu sana cha uraibu."


    elif assessment["title"] == "OCD Assessment (Y-BOCS)":
        if selected_language == "English":
            if score <= 7:
                return "Result: Subclinical"
            elif score <= 15:
                return "Result: Mild"
            elif score <= 23:
                return "Result: Moderate"
            elif score <= 31:
                return "Result: Severe"
            else:
                return "Result: Extreme"
                
        elif selected_language == "Swahili":
            if score <= 7:
                return "Matokeo: Subkliniki"
            elif score <= 15:
                return "Matokeo: Nyepesi"
            elif score <= 23:
                return "Matokeo: Wastani"
            elif score <= 31:
                return "Matokeo: Kali"
            else:
                return "Matokeo: Kali mno"


    elif assessment["title"] == "PTSD Assessment (Post-Traumatic Stress Disorder)":
        if score >= 3:
            if selected_language == "English":
                return "Your score suggests that PTSD is likely. Further assessment is warranted."
            elif selected_language == "Swahili":
                return "Alama zako zinaonyesha kuwa PTSD inawezekana. Uchunguzi zaidi unahitajika."
        else:
            if selected_language == "English":
                return "Your score suggests that PTSD is less likely. Monitor and re-assess if necessary."
            elif selected_language == "Swahili":
                return "Alama zako zinaonyesha kuwa PTSD ni chini ya uwezekano. Fuatilia na tathmini tena ikiwa ni lazima."


    elif assessment["title"] == "DAST-10 Assessment (Drug Abuse Screening Test)":
        return ""
    

    elif assessment["title"] == "ASRS-v1.1 Assessment (Adult ADHD Self-Report Scale)":
        if score == 0:
            return "No problems reported. Suggested action: None at this time." if selected_language == "English" else "Hakuna matatizo yaliyoripotiwa. Hatua iliyopendekezwa: Hakuna kwa wakati huu."
        elif score <= 2:
            return "Low level of problems. Suggested action: Monitor, re‐assess at a later date." if selected_language == "English" else "Kiwango cha chini cha matatizo. Hatua iliyopendekezwa: Fuatilia, tathmini tena baadaye."
        elif score <= 4:
            return "Moderate level of problems. Suggested action: Further investigation." if selected_language == "English" else "Kiwango cha wastani cha matatizo. Hatua iliyopendekezwa: Uchunguzi zaidi."
        else:
            return "Substantial level of problems. Suggested action: Intensive assessment." if selected_language == "English" else "Kiwango kikubwa cha matatizo. Hatua iliyopendekezwa: Tathmini ya kina."


    elif assessment["title"] == "Psychosis Screening Questionnaire (PSQ) Assessment":
        if score >= 2:
            return "Your score suggests the presence of significant psychotic symptoms. Further assessment by a mental health professional is recommended." if selected_language == "English" else "Alama zako zinaonyesha uwepo wa dalili kubwa za wazimu. Inapendekezwa kufanyiwa tathmini zaidi na mtaalamu wa afya ya akili."
        else:
            return "Your score suggests no significant psychotic symptoms. Continue to monitor your well-being." if selected_language == "English" else "Alama zako zinaonyesha hakuna dalili kubwa za wazimu. Endelea kufuatilia ustawi wako."


    elif assessment["title"] == "Depression Assessment (PHQ-9)":
        interpretations = {
            "English": [
                "Your score suggests Minimal depression.",
                "Your score suggests Mild depression.",
                "Your score suggests Moderate depression.",
                "Your score suggests Moderately severe depression.",
                "Your score suggests Severe depression."
            ],
            "Swahili": [
                "Alama zako zinaonyesha sonona ndogo.",
                "Alama zako zinaonyesha sonona ya wastani.",
                "Alama zako zinaonyesha sonona ya kati.",
                "Alama zako zinaonyesha sonona kali ya wastani.",
                "Alama zako zinaonyesha sonona kali sana."
            ]
        }
        boundaries = [4, 9, 14, 19]

        for i, boundary in enumerate(boundaries):
            if score <= boundary:
                return interpretations[selected_language][i]
        else:
            return interpretations[selected_language][4]


    elif assessment["title"] == "IQCODE Assessment":
        if selected_language == "English":
            if score <= 15:
                return "Your score suggests minimal or no cognitive decline."
            elif score <= 30:
                return "Your score suggests mild cognitive decline."
            elif score <= 45:
                return "Your score suggests moderate cognitive decline."
            else:
                return "Your score suggests severe cognitive decline."
        elif selected_language == "Swahili":
            if score <= 15:
                return "Alama zako zinaonyesha dalili ndogo au hakuna upungufu wa kiakili."
            elif score <= 30:
                return "Alama zako zinaonyesha upungufu wa kiakili wa wastani."
            elif score <= 45:
                return "Alama zako zinaonyesha upungufu wa kiakili wa kati."
            else:
                return "Alama zako zinaonyesha upungufu wa kiakili mkali."

