""" functions ive stollen from the original code"""

import os
import joblib
import openai
from dotenv import load_dotenv
import plotly.graph_objs as go
from plotly.graph_objects import Layout
from app import app

import plotly.graph_objects as go

import plotly.graph_objects as go

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

    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f27100'))
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={
            'text': f"Alama zako {assessment_name}" if selected_language == "Swahili" else f"Your {assessment_name} Score",
            'font': {'size': 24, 'color': '#f27100'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_score], 'tickvals': list(range(0, max_score + 1, tick_interval)), 'ticktext': [str(i) for i in range(0, max_score + 1, tick_interval)]},
            'steps': [
                {'range': [0, 0.3 * max_score], 'color': 'green'},
                {'range': [0.3 * max_score, 0.7 * max_score], 'color': 'yellow'},
                {'range': [0.7 * max_score, max_score], 'color': 'red'}
            ],
            'bar': {'color': '#f27100'}
        }
    ),
    layout=layout
    )

    # Enhancements
    if score <= 0.3 * max_score:
        level_text = "Low Level "
        emoji = "👏👏👏"  # Sad emoji for low score
        if selected_language == "Swahili":
            level_text = "Alama ya  Chini"
    elif score <= 0.7 * max_score:
        level_text = "Medium Level Score"
        emoji = "😓😓😓"  # Neutral emoji for average score
        if selected_language == "Swahili":
            level_text = "Alama ya  Kati"
    else:
        level_text = "High Level Score"
        emoji = "😢😢😢😢😢😢😢"  # Happy emoji for high score
        if selected_language == "Swahili":
            level_text = "Alama ya Juu"

    fig.add_annotation(dict(font=dict(color="#f27100", size=15),
                             x=0.5,
                             y=0.34,
                             showarrow=False,
                             text=f"{score}/{max_score} - {level_text} {emoji}",  # Emoji included
                             textangle=0,
                             xanchor="center",
                             yanchor="middle"
                             ))

    return fig.to_html(full_html=False)  # Example using ID



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

def get_predicted_condition(age, gender, selected_symptoms):
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
    api_key = os.environ.get("OPENAI_API_KEY")
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
                {"role": "system", "content":'''You are a mental health assistant with knowledge about various mental health conditions. Provide responses that are sensitive, empathetic, and non-diagnostic
                 in your responses don't forget to encourage users to seek help from mental facilities and hospitals in Tanzania such as, Mirembe hospital, Amana Hospital, 
                 Temeke, Muhimbili and you must mention other therapy facilities in Tanzania. 
                 
                 Encourage me that the condition am facing can be cured so I should not feel stigmatized
                 And for a particular condition mention some practical examples of the symptoms of that condition'''},
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
  "After completing the YMRS (Young Mania Rating Scale) for bipolar disorder, my score is {score} out of 60 indicating: '{result_text}'. Please provide:
1. An empathetic response that assesses the severity of my score, offering specific advice, and if high, recommending a hospital visit.
2. A brief explanation of bipolar disorder, its early symptoms, and its impact on life.
3. Coping strategies for bipolar disorder and positive recognition of my effort in taking the YMRS assessment."

Your response should be compassionate and actionable, guiding me towards the appropriate next steps, especially if my score suggests an urgent need for professional medical assistance.

        
        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''
    elif assessment["title"] == "Anxiety Assessment (GAD-7)":
        return f''' gpt3_prompt = f"""
       As an expert mental health assistant, after completing the GAD-7 anxiety assessment with a score of {score} out of 21, I need a response that:
        1. Provides empathetic support reflecting on the anxiety score and briefly describes anxiety, including typical experiences.
        2. Outlines the risks of untreated anxiety and natural coping strategies in a concise manner.
        3. Lists notable mental health facilities in Tanzania, like Mirembe, Amana, and Temeke hospitals, for additional help.

        The response should be swift yet empathetic, combining comfort with essential guidance, and highlight the importance of professional health advice.


        """
        '''
    elif assessment["title"] == "AUDIT (Alcohol Use Disorders Identification Test)":
       return f''' gpt3_prompt = f"""
     As an experienced mental health assistant, I've taken the AUDIT assessment score of {score} out of 40:
    1. Analyse or Interpret my score, with a straightforward categorization as high, moderate, or low, including a strong recommendation for a hospital visit if the score is high. Combine this with a clear definition of Substance Alcohol Use Disorder and its early signs.
    2. Highlight the negative impacts of unchecked alcohol addiction.
    3. Suggest a range of coping strategies to combat alcohol addiction, commend the proactive step of taking the assessment.'''
    
    elif assessment["title"] == "OCD Assessment (Y-BOCS)":
        return f'''gpt3_prompt = f"""
       As an expert mental health assistant, I've scored {score} on the OCD assessment out of the maximum 40 . Please provide a response that:
        1. Combines an empathetic acknowledgement of my score level (high, moderate, or low) with clear guidance, especially advising hospital visitation if the score is high.
        2. Offers a concise explanation of Obsessive-Compulsive Disorder, including typical early symptoms with exampleskjl and briefly touches on the potential daily life impacts if left unmanaged.
        3. Proposes natural coping strategies for OCD and commends my proactive approach in taking the assessment.

Your reply should be empathetic, succinct, and directive, prioritizing immediate understanding and action where necessary.

        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''
    elif assessment["title"] == "PTSD Assessment (Post-Traumatic Stress Disorder)":
        return f'''gpt3_prompt = f"""
        "Upon completing the PTSD assessment, I received a score of {score}, which suggests: '{result_text}'. I need guidance on:
        1. An evaluation of my score as high or low, and if it's high, a gentle encouragement to seek help at a hospital.
        2. A general overview of PTSD, including its early symptoms and the potential consequences if it remains untreated.
        3. Reassurance to alleviate any fears or hesitations about visiting a hospital for further assistance.

        Please offer a supportive response that helps me understand my situation and encourages appropriate steps while reducing any anxiety about seeking professional help."

        """
        gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        '''
    elif assessment["title"] == "DAST-10 Assessment (Drug Abuse Screening Test)":
        return f"""
            "Having completed the DAST-10 drug abuse assessment with a score of {score} out of {assessment['max_score']}, I'm seeking:
            1. An immediate understanding of whether my score is considered high, moderate, or low, including direct advice on whether a hospital visit is necessary.
            2. A succinct definition of Drug Abuse Disorder, with an overview of early signs and potential health and life implications if left unaddressed.
            3. Recognition of my initiative in taking this assessment and personalized guidance on coping strategies tailored to my score.

Please provide a response that is both informative and supportive, guiding me towards the best course of action for my health."

            """
    elif assessment["title"] == "ASRS-v1.1 Assessment (Adult ADHD Self-Report Scale)":
        return f""" 
            "After completing the ASRS-v1.1 (Adult ADHD Self-Report Scale) assessment, my score is {score} out of {assessment['max_score']}. I'm seeking:
1. An interpretation of my ASRS-v1.1 score to understand if it is high, moderate, or low, and the implications for my ADHD symptoms.
2. An explanation of ADHD, its symptoms in adults, and the potential consequences of leaving it unmanaged.
3. Acknowledgment of my initiative in taking the ASRS-v1.1 assessment and personalized advice for coping with ADHD.

Your response should be prompt and provide me with clear, empathetic guidance based on my score and the proactive steps I've already taken."

            """
    elif assessment["title"] == "Psychosis Screening Questionnaire (PSQ) Assessment":
        return f'''gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have taken  a schizophrenia assessment and achieved a score of {score} out of a maximum possible score of {assessment['max_score']}. 

        1) Tell me if my score is high or low
        2) What is schizophrenia and what are the symptoms and early signs.
        3)Encourage me to go to the hospital for detailed check up

        Lastly, acknowledge my  initiative in taking the assessment and emphasize the importance of mental well-being.
        '''
    elif assessment["title"] == "Depression Assessment (PHQ-9)":
      return f'''gpt3_prompt = f"""
    "Having completed the Depression(sonona) PHQ-9 assessment, my score is {score} out of a potential 27. Could you:
                        1. Interpret my PHQ-9 score with empathy, indicating if it's considered high, moderate, or low, and explain the nature of depression along with its potential consequences if neglected.
                        2. Provide natural coping strategies and culturally sensitive advice for supporting someone with depression in Tanzania.
                        3. Recognize my effort in taking this step towards mental wellness, and if necessary, guide me on seeking professional help, especially if my score is on the higher end."

        '''
    else:
       return f'''gpt3_prompt = f"""
        As a knowledgeable mental health assistant:
        I have completed the IQCODE(Cognitive Decline)  Dementia assessment for my relative, scoring {score} out of 48'.
        1. Interpret my score by telling me if it is high or low
        2. Explain the concept of dementia, what is it and how can it be avoided and natural ways to help my relative.
        3. Encourage the person to go to the hospital if the score is high
        
              
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
          if score <= boundary:
             return interpretations[selected_language][i]


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
                return "Matokeo: Hali isiyo dhahiri"
            elif score <= 15:
                return "Matokeo: Hali ya chini"
            elif score <= 23:
                return "Matokeo: Hali ya wastani"
            elif score <= 31:
                return "Matokeo: Hali mbaya"
            else:
                return "Matokeo: Hali mbaya sana"

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
        if selected_language == "English":
            if score == 0:
                return "Your score suggests no problem related to drug abuse."
            elif score <= 2:
                return "Your score suggests a low level of drug abuse."
            elif score <= 5:
                return "Your score suggests a moderate level of drug abuse."
            elif score <= 8:
                return "Your score suggests a substantial level of drug abuse."
            else:
                return "Your score suggests a severe level of drug abuse."
        elif selected_language == "Swahili":
            if score == 0:
                return "Alama zako zinaonyesha hakuna tatizo linalohusiana na matumizi ya dawa za kulevya."
            elif score <= 2:
                return "Alama zako zinaonyesha kiwango cha chini cha matumizi ya dawa za kulevya."
            elif score <= 5:
                return "Alama zako zinaonyesha kiwango cha wastani cha matumizi ya dawa za kulevya."
            elif score <= 8:
                return "Alama zako zinaonyesha kiwango kikubwa cha matumizi ya dawa za kulevya."
            else:
                return "Alama zako zinaonyesha kiwango cha juu sana cha matumizi ya dawa za kulevya."


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
            return "Your score suggests the presence of significant psychotic symptoms. Further assessment by a mental health professional is recommended." if selected_language == "English" else "Alama zako zinaonyesha uwepo wa dalili kubwa za shizofrenia. Inapendekezwa kufanyiwa tathmini zaidi na mtaalamu wa afya ya akili."
        else:
            return "Your score suggests no significant psychotic symptoms. Continue to monitor your well-being." if selected_language == "English" else "Alama zako zinaonyesha hakuna dalili kubwa za shizofrenia. Endelea kufuatilia ustawi wako."


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


    else:  # This now handles the Dementia Assessment by default
        if selected_language == "English":
            if score <= 15:
                return "Your score suggests minimal or no cognitive decline."
            elif score <= 30:
                return "Your score suggests mild cognitive decline."
            elif score <= 48:
                return "Your score suggests moderate cognitive decline."
            else:
                return "Your score suggests severe cognitive decline."
        elif selected_language == "Swahili":
            if score <= 15:
                return "Kiwango cha chini au kisicho na kuzorota kwa akili."
            elif score <= 30:
                return "Kuzorota kwa wastani kwa akili."
            elif score <= 48:
                return "Kuzorota kwa akili kwa kiasi kikubwa."
            else:
                return "Kuzorota kwa akili kwa kiasi kikubwa sana."
