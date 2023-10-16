#Imports
import streamlit as st
import openai
import os
import plotly.graph_objs as go
import uuid
import joblib

## CSS STYLING
def set_css():
    # First set of styles
    st.markdown("""
        <style>
            div[data-baseweb="select"] > div {
                cursor: pointer !important;
            }
            body {
                background-color: #E0E5E9 !important;
                font: normal 1em Arial, sans-serif !important;
                color: black !important;  /* Default text color */
            }
            .stButton>button {
    width: 220px !important;
    height: 60px !important;
    background-color: #4CAF50 !important;
    color: white !important;
    padding: 0.6em 1.2em !important;
    border: none !important;
    cursor: pointer !important;
    border-radius: 20px !important;
    font-size: 2.1em !important;
    font-weight: bold !important;
    margin: 16px !important; /* Adjust the margin to your preferred spacing */
}

.stButton>button:hover {
    background-color: #45a049 !important;
}

             .submit-button, .back-button {
                width: 200px;
                /* ... other styles for the buttons ... */
            }
            /* Style for select boxes */
            label[for="streamlit-widgets"] {
                font-size: 2.5em !important;  /* Increase font size */
                font-weight: bold !important; /* Bold font */
            }
            
            /* Border around the select boxes */
            div.row-widget.stRadio > div, div.row-widget.stSelectbox > div {
                border: 2px solid green !important;
                border-radius: 20px !important;  /* Rounded corners */
                padding: 10px !important;
            }

            /* Add some space between the select boxes */
            div.row-widget.stRadio, div.row-widget.stSelectbox {
                margin-bottom: 10px !important;
            }
            /* Styling the collapsed dropdown */
        div[data-baseweb="select"] > div {
            background-color: #f5f5f5 !important;  /*  background */
            color: black !important;  /* Black font color */
            border: 1px solid #d1d1d1 !important;  /* Border color */
            font-size: 1.1em !important;  /* Font size */
        }

        /* Styling the options inside the dropdown */
        div[data-baseweb="menu"] > div {
            background-color: #f5f5f5 !important;  /* Light gray background */
        }

        /* Styling individual options */
        div[data-baseweb="menu"] > div > div {
            color: black !important;  /* Black font color for options */
        }

        /* Styling options on hover */
        div[data-baseweb="menu"] > div > div:hover {
            background-color: #black !important;  /* Darker gray background on hover */
        }
         /* Adding margins around the Streamlit buttons */
        .stButton>button {
        border-radius: 20px !important;  /* Rounded corners */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;  /* Drop shadow */
        margin: 16px !important;  /* Space around each button */
        background-color: #4CAF50 !important;  /* Button color */
        color: white !important;  /* Text color */
        font-size: 1em !important;
        padding: 10px 20px !important;  /* Vertical and horizontal padding */
    }
    

    """, unsafe_allow_html=True)

# DATABASE CONFIG
import pymongo

# Connect to the MongoDB instance running on your machine.
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access your database. If it doesn't exist, it'll be created.
db = client["mental_health_db"]

# Access the 'users' collection from your database. If it doesn't exist, it'll be created.
users = db["users"]





# Load the trained SVM model and other preprocessing objects
svm_model = joblib.load('svm_model.joblib')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')
label_encoder = joblib.load('label_encoder.joblib')
set_css()

st.markdown("""
<style>
    .reportview-container .main .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 20px 0px;
    }
    div[data-baseweb="checkbox"] {
        border: 1px solid rgba(0, 165, 255, 0.9);
        border-radius: 5px;
        padding: 6px;
        margin-bottom: 8px;
        transition: background-color 0.3s;
    }
    div[data-baseweb="checkbox"]:hover {
        background-color: rgba(0, 165, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)


# Create a mapping from Swahili to English symptoms with headers
swahili_to_english_mapping = {
    "Consistence fear or worries.": {
        "Unapambana na hofu zisizo za kawaida, unajiepusha kufanya shughuli kama kuendesha gari au kusafiri kwa hofu, na mara nyingi unahisi kuwa pekee yako au kutengwa": "Often feeling overwhelmed with irrational fears, avoiding certain places due to worries, and frequently feeling scared without a clear reason",
        "Unapata shida kwa hofu ya kupata mashambulio ya hofu.": "struggles with the fear of experiencing panic attacks",
        "Unaonesha kutetemeka au kutikisika dhahiri bila jitihada za kimwili.": "displays visible trembling or shaking without physical exertion",
        "Unapata shida kwa hofu ya kuhukumiwa kwa kujieleza mbele za watu.": "struggles with fears of being judged for expressing emotions"
    },
    "Experience of unreal perceptions": {
        "Unasikia sauti ambazo wengine hawasikii, una wasiwasi kwamba watu wanakufuatilia, na unaamini wengine wanaweza kusoma mawazo yako": "Often hearing voices others can't, being suspicious of others, and feeling that others can read your thoughts",
        "Unaonesha dalili za mawazo ya kichawi, Ukiamini nguvu ziziso za kawaida (Supernatural) zinaathiri maisha yako.": "exhibits signs of magical thinking, believing in supernatural forces affecting their lives",
        "Unapata shida kutofautisha kati ya ndoto na uhalisia.": "struggles to distinguish between hallucinations and reality"
    },
    "Challenges with memory and cognition": {
        "Unaonyesha kupungua kwa uwezo wa kufikiria, unapata shida kukumbuka majina, na mara nyingi haujatambua tarehe au wakati wa sasa": "Challenged in reasoning and problem solving, forgetting names, and frequently unaware of the current date or time"
    },
    "Persistent sadness or hopelessness": {
       "Mara nyingi unafikiria kifo, unahisi wasiwasi kila wakati, na una usumbufu katika hamu ya kula": "Often contemplating death, consistently feeling anxious, and experiencing disruptions in appetite",
        "Unateseka na kusumbuka kupata usingizi kutokana na mitindo ya usingizi iliyovurugika.": "suffers from disrupted sleep patterns and early morning awakenings",
        "Unapitia mawazo endelevu ya kifo na kujiua.": "experiences persistent thoughts of death and suicide",
        "Unaonesha dalili za kupuuza usafi wa kibinafsi na muonekano.": "shows signs of neglecting personal hygiene and appearance"
    },
    "Reliance on substance use": {
        "Unapata shida kusimamia kazi bila kutumia dawa au pombe, unapendelea dawa za kulevya, na unahisi haja ya kutumia dawa au pombe kila wakati": "Difficult to manage tasks without drugs or alcohol, prioritizing drug use, and feeling a constant need to use substances"
    },
    "Extreme Mood Swings": {
        "Una vipindi vya kuhisi furaha sana na huzuni sana, unakuwa mchangamfu au mpole kulingana na wakati, na mara nyingi unajihusisha na shughuli hatari": "Experiencing overly happy and sad periods, being very active or talkative, and frequently engaging in risky activities"
    }
}


# English Symptoms List
symptoms_list_english = {key: list(val.values()) for key, val in swahili_to_english_mapping.items()}


# English Headers
english_headers = [
    "Consistence fear or worries.",
    "Experience of unreal perceptions",
    "Challenges with memory and cognition",
    "Persistent sadness or hopelessness",
    "Reliance on substance use",
    "Extreme Mood Swings"
]

# Swahili Headers
swahili_headers = [
    "Hisia za wasiwasi na woga",
    "Hisia za kuona vitu ambavyo si halisi",
    "Matatizo ya kusahau / Kupoteza kumbukumbu",
    "Hisia za huzuni kali na kukata tamaa",
    "Uraibu wa pombe na madawa",
    "Kubadilika badilika kwa hisia"
]

# Swahili to English Headers Mapping
swahili_to_english_headers = {
    "Hisia za wasiwasi na woga": "Consistence fear or worries.",
    "Hisia za kuona vitu ambavyo si halisi": "Experience of unreal perceptions",
    "Matatizo ya kusahau / Kupoteza kumbukumbu": "Challenges with memory and cognition",
    "Hisia za huzuni kali na kukata tamaa": "Persistent sadness or hopelessness",
    "Uraibu wa pombe na madawa": "Reliance on substance use",
    "Kubadilika badilika kwa hisia": "Extreme Mood Swings"
}

# Function to get headers based on language
def get_headers_by_language(language="English"):
    if language == 'Swahili':
        return swahili_headers
    else:
        return english_headers



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



def set_age_input_style():
    st.markdown("""
    <style>
        div[data-testid="stNumberInput"] input {
            height: 3em !important;
            border-radius: 0.9em !important;
            border: 2px solid #006400 !important;
            padding: 0.5em !important;
            font-size: 1.2em !important;
        }
    </style>
    """, unsafe_allow_html=True)


def navigate_back_to_menu(selected_language):
    """
    Display a "Back to main menu" button and handle its click.
    """
    back_button_label, _ = get_button_labels(selected_language)
    if st.button(back_button_label):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu


    
def collect_symptoms(selected_language="English"):
    # Deciding which symptom list to use based on language selection
    symptoms_list = symptoms_list_english if selected_language == 'English' else {key: list(val.keys()) for key, val in swahili_to_english_mapping.items()}

    # Displaying the checkboxes for symptoms
    selected_symptoms = []
    for condition, symptoms in symptoms_list.items():
        st.write(f"**{condition} Symptoms:**")
        for symptom in symptoms:
            if st.checkbox(symptom):
                selected_symptoms.append(symptom)
                
    return selected_symptoms




def collect_user_data(selected_language="English"):
    # Generating User ID
    user_id = str(uuid.uuid4())
    
    # Defining options based on selected_language
    if selected_language == "English":
        age_group_options = ["Select Age Group", "15-24", "25-34", "35-44", "45-54", "55+"]
        gender_options = ["Select Gender", "Male", "Female"]
    elif selected_language == "Swahili":
        age_group_options = ["Chagua Kundi la Umri", "15-24", "25-34", "35-44", "45-54", "55+"]
        gender_options = ["Chagua Jinsia", "Mwanaume", "Mwanamke"]

    age_group = st.selectbox(age_group_options[0], age_group_options)
    gender = st.selectbox(gender_options[0], gender_options)

    if age_group == age_group_options[0]:  
        age_group = None
    if gender == gender_options[0]:  
        gender = None

    return user_id, age_group, gender


def get_button_labels(selected_language):
    if selected_language == "Swahili":
        return "Rudi Menyu kuu", "Wasilisha"
    else:
        return "Back to main menu", "Submit"



def store_data_in_database(user_id, age_group, gender, assessment_data):
    # Check if the user already exists in the database
    existing_user = users.find_one({'user_id': user_id})
    
    if existing_user:
        # Update the user's assessments
        users.update_one({'user_id': user_id}, {'$push': {'assessments': assessment_data}})
    else:
            # Insert a new user
        new_user = {
            'user_id': user_id,
            'age_group': age_group,
            'gender': gender,
            'predicted_condition': st.session_state.get('predicted_condition', None),  # Use get() to provide a default value
            'assessments': [assessment_data]
        }
        users.insert_one(new_user)




import plotly.graph_objs as go


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
    
    
    return fig

def sanitize_text(text):
    return text.replace("\u2014", "--")  # replace em dash with double hyphen

# Initialize the OpenAI API key
def initialize_openai():
    openai.api_key = os.environ.get('OPENAI_API_KEY')

# Generate GPT-3 response
def get_gpt3_response(prompt, language="English", temperature=0.7):
    if language == "Swahili":
        prompt += " Please respond in Swahili."

    try:
        # Use the chat model endpoint for GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You are a mental health assistant with knowledge about various mental health conditions. Provide responses that are sensitive, empathetic, and non-diagnostic."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        return "Sorry, there was an issue fetching a response. Please try again later."
    
def get_predicted_condition(age, gender, selected_language, selected_symptoms):
    """
    Use the provided information to predict the mental health condition.
    """
    # Convert Swahili symptoms to English if necessary
    if selected_language == 'Swahili':
        converted_symptoms = []
        for symptom in selected_symptoms:
            for cond, symps in swahili_to_english_mapping.items():
                if symptom in symps:
                    converted_symptoms.append(symps[symptom])
                    break
        selected_symptoms = converted_symptoms

    # Process the selected symptoms into a format suitable for the model
    processed_symptoms = ' '.join(selected_symptoms)

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


def anxiety_assessment(selected_language):
     # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data(selected_language)
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender
    if selected_language == "English":
        st.write("### Anxiety Assessment (GAD-7)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya Wasiwasi (GAD-7)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)
    # GAD-7 Questions and response options
    questions = {
        "English": [
            "Feeling nervous, anxious, or on edge?",
            "Not being able to stop or control worrying?",
            "Worrying too much about different things?",
            "Trouble relaxing?",
            "Being so restless that it's hard to sit still?",
            "Becoming easily annoyed or irritable?",
            "Feeling afraid as if something awful might happen?"
        ],
        "Swahili": [
            "Kujisikia mwenye wasiwasi, wasiwasi, au kwenye ukingo?",
            "Kutoweza kusimamisha au kudhibiti wasiwasi?",
            "Kujali sana juu ya vitu tofauti?",
            "Matatizo ya kupumzika?",
            "Kuwa mwenye wasiwasi sana hivi kwamba ni ngumu kukaa kimya?",
            "Kuwa mwepesi wa kukasirika au kuwa na hasira?",
            "Kuhisi hofu kama kitu kibaya kinaweza kutokea?"
        ]
    }

    options = {
        "English": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Swahili": ["Hapana Kabisa", "Siku kadhaa", "Zaidi ya nusu ya siku", "Karibu kila siku"]
    }
    
    
    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options=options[selected_language], index=0)
        scores.append(options[selected_language].index(score))
    
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)

    col1, col2 = st.columns(2)
    
    # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu


    
    

    if col1.button(submit_button_label):  # Place the "Submit" button in the left column
        with st.spinner('Processing your answers...'):
            # Keep the rest of your existing logic for processing the form submission here...
            # This includes summing the scores, generating the interpretation, etc.

        
            total_score = sum(scores)
            assessment_data = {
                'name': 'Anxiety Assessment',
                'score': total_score
            }

            # Interpretation based on the total score
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
                if total_score <= boundary:
                    user_interpretation = interpretations[selected_language][i]
                    break
            else:
                user_interpretation = interpretations[selected_language][3]
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=21)  
            st.plotly_chart(fig)

          
            # Store in database
            store_data_in_database(user_id, age_group, gender, assessment_data)
            # Feedback and advice using GPT-3
            gpt3_prompt = f"You are a help full assistant"
            gpt3_prompt = f''' gpt3_prompt = f"""
As a knowledgeable mental health assistant:
I have taken an anxiety assessment, scoring {total_score} out of a maximum of 21, suggesting: '{user_interpretation}'.
1. Provide an empathetic response based on my score, mentioning the score out of 21.
2. Explain the nature of anxiety and the examples people with anxieties experience
3. List detailed negative impacts of untreated anxiety.
4. Offer coping strategies and natural ways  into managing anxiety.

5. Mention actions one should and shouldn't undertake when interacting with someone experiencing anxiety.
"""

'''
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            st.write(user_interpretation)
            st.write(f"{gpt3_response}")

    reminder_text = {
            "English": """
         <span style="color:green">**Reminder:** These insights are based on the provided conversation and are for informational purposes only. 
        They are not a definitive diagnosis. Please consult with a healthcare professional for a comprehensive assessment.</span>
        """,
        "Swahili": """
        <span style="color:green">**Kumbusho:** Kumbuka kwamba mazungumzo yaliyotolewa na ni kwa madhumuni ya taarifa pekee.
        Hayawakilishi utambuzi wala tathmini  kamili ya kitabibu. Tafadhali shauriana na mtaalamu wa afya kwa tathmini kamili.</span>
        """
}

    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()


def alcohol_addiction_assessment(selected_language):
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
        user_id, age_group, gender = collect_user_data(selected_language)          
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender

        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender
    if selected_language == "English":
        st.write("### AUDIT (Alcohol Use Disorders Identification Test)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### AUDIT (Tathmini ya  Kutambua Uraibu wa Matumizi ya Pombe)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)
    # AUDIT Questions and response options
    questions = {
        "English": [
            "How often do you have a drink containing alcohol?",
            "How many drinks containing alcohol do you have on a typical day when you are drinking?",
            "How often do you have six or more drinks on one occasion?",
            "How often during the last year have you found that you were not able to stop drinking once you had started?",
            "How often during the last year have you failed to do what was normally expected of you because of drinking?",
            "How often during the last year have you needed a first drink in the morning to get yourself going after a heavy drinking session?",
            "How often during the last year have you had a feeling of guilt or remorse after drinking?",
            "How often during the last year have you been unable to remember what happened the night before because of your drinking?",
            "Have you or someone else been injured because of your drinking?",
            "Has a relative, friend, doctor, or other healthcare worker been concerned about your drinking or suggested you cut down?"
        ],
        "Swahili": [
            "Mara ngapi unakunywa kinywaji kilicho na pombe?",
            "Unakunywa vinywaji vingapi vyenye pombe siku ya kawaida unapokuwa unakunywa?",
            "Mara ngapi unakunywa vinywaji sita au zaidi kwa mara moja?",
            "Mara ngapi mwaka uliopita uligundua kuwa hukuweza kuacha kunywa mara tu ulipoanza?",
            "Mara ngapi mwaka uliopita umeshindwa kufanya kilichotarajiwa kwako kwa sababu ya kunywa?",
            "Mara ngapi mwaka uliopita umehitaji kinywaji cha kwanza asubuhi ili kujiweka sawa baada ya kikao kizito cha kunywa?",
            "Mara ngapi mwaka uliopita umekuwa na hisia za hatia au majuto baada ya kunywa?",
            "Mara ngapi mwaka uliopita umeshindwa kukumbuka kilichotokea usiku uliotangulia kwa sababu ya kunywa kwako?",
            "Je, wewe au mtu mwingine ameumizwa kwa sababu ya kunywa kwako?",
            "Je, ndugu, rafiki, daktari, au mfanyakazi mwingine wa afya amekuwa na wasiwasi kuhusu kunywa kwako au amependekeza upunguze?"
        ]
    }

    options = {
        "English": [
            ["Never", "Monthly or less", "2-4 times a month", "2-3 times a week", "4 or more times a week"],
            ["1 or 2", "3 or 4", "5 or 6", "7 to 9", "10 or more"],
            ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"],
            ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"],
            ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"],
            ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"],
            ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"],
            ["Never", "Less than monthly", "Monthly", "Weekly", "Daily or almost daily"],
            ["No", "Yes, but not in the last year", "Yes, during the last year"],
            ["No", "Yes, but not in the last year", "Yes, during the last year"]
        ],
        "Swahili": [
            ["Kamwe", "Mara moja kwa mwezi au chini ya hapo", "Mara 2-4 kwa mwezi", "Mara 2-3 kwa wiki", "Mara 4 au zaidi kwa wiki"],
            ["1 au 2", "3 au 4", "5 au 6", "7 hadi 9", "10 au zaidi"],
            ["Kamwe", "Chini ya mara moja kwa mwezi", "Mara moja kwa mwezi", "Kila wiki", "Kila siku au karibu kila siku"],
            ["Kamwe", "Chini ya mara moja kwa mwezi", "Mara moja kwa mwezi", "Kila wiki", "Kila siku au karibu kila siku"],
            ["Kamwe", "Chini ya mara moja kwa mwezi", "Mara moja kwa mwezi", "Kila wiki", "Kila siku au karibu kila siku"],
            ["Kamwe", "Chini ya mara moja kwa mwezi", "Mara moja kwa mwezi", "Kila wiki", "Kila siku au karibu kila siku"],
            ["Kamwe", "Chini ya mara moja kwa mwezi", "Mara moja kwa mwezi", "Kila wiki", "Kila siku au karibu kila siku"],
            ["Kamwe", "Chini ya mara moja kwa mwezi", "Mara moja kwa mwezi", "Kila wiki", "Kila siku au karibu kila siku"],
            ["Hapana", "Ndiyo, lakini si mwaka uliopita", "Ndiyo, mwaka uliopita"],
            ["Hapana", "Ndiyo, lakini si mwaka uliopita", "Ndiyo, mwaka uliopita"]
        ]
    }

    scores = []
    for idx, question in enumerate(questions[selected_language]):
        score = st.selectbox(question, options=options[selected_language][idx], index=0)
        scores.append(options[selected_language][idx].index(score))

    if selected_language == "Swahili":
        button_label = "Wasilisha"
    else:
        button_label = "Submit"

    col1, col2 = st.columns(2)
    
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu



   

    if col1.button(button_label):  # Placing "Submit" in the left column
        

        with st.spinner('Processing your answers...'):
            total_score = sum(scores)
           
            assessment_data = {
                'name': 'AUDIT (Alcohol Use Disorders Identification Test)',
                'score': total_score
            }
            store_data_in_database(user_id, age_group, gender, assessment_data)

                        
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=40)  # Assuming AUDIT max score is 40
            st.plotly_chart(fig)

            # AUDIT Interpretation based on total score and language
            if selected_language == "English":
                if total_score <= 7:
                    result_text = "Your score suggests Low level of alcohol problems or dependence."
                elif total_score <= 15:
                    result_text = "Your score suggests Medium level of alcohol problems or dependence."
                elif total_score <= 19:
                    result_text = "Your score suggests High level of alcohol problems or dependence."
                else:
                    result_text = "Your score suggests Very High level of alcohol problems or dependence."
            elif selected_language == "Swahili":
                if total_score <= 7:
                    result_text = "Alama zako zinaonyesha kiwango cha chini cha uraibu wa pombe."
                elif total_score <= 15:
                    result_text = "Alama zako zinaonyesha kiwango cha wastani cha uraibu wa pombe."
                elif total_score <= 19:
                    result_text = "Alama zako zinaonyesha kiwango cha juu cha uraibu."
                else:
                    result_text = "Alama zako zinaonyesha kiwango cha juu sana cha uraibu."

            # Feedback and advice using GPT-3
            gpt3_prompt = f"You are a help full assistant"
            gpt3_prompt = f'''gpt3_prompt = f"""
As a knowledgeable mental health assistant:
I have completed the AUDIT assessment, scoring {total_score} out of 40, indicating: '{result_text}'.
1. Offer an empathetic response based on my score, and acknowledge my score out of 40.
2. Explain Substance Alcohol Use Disorder. and early signs of this problem.
3. List detailed negative consequences of untreated alcohol addiction in daily life.
4. Offer coping strategies, natural ways and insights into managing alcohol addiction.
5. Commend me for undertaking the assessment.
7. Advise and encourage me to seek hospital help if my score is high.
"""
gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
'''
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            st.write(result_text)
            st.write(f"{gpt3_response}")

            reminder_text = {
            "English": """
         <span style="color:green">**Reminder:** These insights are based on the provided conversation and are for informational purposes only. 
        They are not a definitive diagnosis. Please consult with a healthcare professional for a comprehensive assessment.</span>
        """,
        "Swahili": """
        <span style="color:green">**Kumbusho:** Kumbuka kwamba mazungumzo yaliyotolewa na ni kwa madhumuni ya taarifa pekee.
        Hayawakilishi utambuzi wala tathmini  kamili ya kitabibu. Tafadhali shauriana na mtaalamu wa afya kwa tathmini kamili.</span>
        """
}

            st.markdown(reminder_text[selected_language], unsafe_allow_html=True)    
            
     
    
    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()

def ocd_assessment(selected_language):
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data(selected_language)  # Passing the selected_language
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender
    if selected_language == "English":
        st.write("### OCD Assessment (Y-BOCS)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya OCD (Y-BOCS)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)

    

    # Y-BOCS Questions and response options (OCDs Assessment)
    questions = {
        "English": [
            "How much of your time is occupied by obsessive thoughts?",
            "How much do your obsessive thoughts interfere with your work, school, social, or other important role functioning? Is there anything that you don’t do because of them?",
            "How much distress do your obsessive thoughts cause you?",
            "How much of an effort do you make to resist the obsessive thoughts? How often do you try to disregard or turn your attention away from these thoughts as they enter your mind?",
            "How much control do you have over your obsessive thoughts? How successful are you in stopping or diverting your obsessive thinking? Can you dismiss them?",
            "How much time do you spend performing compulsive behaviors? How much longer than most people does it take to complete routine activities because of your rituals? How frequently do you do rituals?",
            "How much do your compulsive behaviors interfere with your work, school, social, or other important role functioning? Is there anything that you don’t do because of the compulsions?",
            "How would you feel if prevented from performing your compulsion(s)? How anxious would you become?",
            "How much of an effort do you make to resist the compulsions?",
            "How strong is the drive to perform the compulsive behavior? How much control do you have over the compulsions?"
        ],
        "Swahili": [
            "Ni kiasi gani cha wakati wako kinachochukuliwa na mawazo ya kulazimisha?",
            "Mawazo yako ya kulazimisha yanaingilia kiasi gani kazi yako, shule, kijamii, au utendaji wa majukumu mengine muhimu? Kuna chochote ambacho hufanyi kwa sababu yao?",
            "Mawazo yako ya kulazimisha yanasababisha kiasi gani cha dhiki kwako?",
            "Unajaribu kiasi gani kupinga mawazo ya kulazimisha? Mara ngapi unajaribu kupuuza au kugeuza mawazo yako mbali na mawazo haya wanapoingia akilini mwako?",
            "Una kiasi gani cha udhibiti juu ya mawazo yako ya kulazimisha? Unafanikiwa kiasi gani katika kuacha au kuelekeza mawazo yako ya kulazimisha? Unaweza kuyapuuza?",
            "Unatumia muda gani kutekeleza tabia za kulazimisha? Inachukua muda gani zaidi kuliko watu wengi kukamilisha shughuli za kawaida kwa sababu ya mila yako? Unafanya mila mara ngapi?",
            "Tabia zako za kulazimisha zinaingilia kiasi gani kazi yako, shule, kijamii, au utendaji wa majukumu mengine muhimu? Kuna chochote ambacho hufanyi kwa sababu ya kulazimisha?",
            "Ungehisije ikiwa ungezuiwa kufanya kulazimisha kwako? Ungekuwa na wasiwasi kiasi gani?",
            "Unajaribu kiasi gani kupinga kulazimisha?",
            "Nguvu gani ya kuendesha tabia ya kulazimisha? Una kiasi gani cha udhibiti juu ya kulazimisha?"
        ]
    }

    options = {
        "English": ["0", "1", "2", "3", "4"],
        "Swahili": ["0", "1", "2", "3", "4"]
    }

    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options=options[selected_language], index=0)
        scores.append(options[selected_language].index(score))

        if selected_language == "Swahili":
            submit_button_label = "Wasilisha"
    else:
        submit_button_label = "Submit"

    col1, col2 = st.columns(2)  # Create two columns for the buttons
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu



    if col1.button(submit_button_label):  # Place the "Submit" button in the left column
        # The rest of your existing logic for processing the form submission remains here...
        # This includes summing the scores, generating the interpretation, etc.

        
        total_score = sum(scores)
        assessment_data = {
        'name': 'OCD Assessment (Y-BOCS)',
        'score': total_score
    }
        store_data_in_database(user_id, age_group, gender, assessment_data)

        with st.spinner('Processing your answers...'):
            
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=40)  # Assuming Y-BOCS max score is 40
            st.plotly_chart(fig)
            
            # Y-BOCS Interpretation based on total score and language
            if selected_language == "English":
                if total_score <= 7:
                    result_text = "Result: Subclinical"
                elif total_score <= 15:
                    result_text = "Result: Mild"
                elif total_score <= 23:
                    result_text = "Result: Moderate"
                elif total_score <= 31:
                    result_text = "Result: Severe"
                else:
                    result_text = "Result: Extreme"
                    
            elif selected_language == "Swahili":
                if total_score <= 7:
                    result_text = "Matokeo: Subkliniki"
                elif total_score <= 15:
                    result_text = "Matokeo: Nyepesi"
                elif total_score <= 23:
                    result_text = "Matokeo: Wastani"
                elif total_score <= 31:
                    result_text = "Matokeo: Kali"
                else:
                    result_text = "Matokeo: Kali mno"

            #st.write(result_text)
            # Feedback and advice using GPT-3
            gpt3_prompt = f"You are a help full assistant"
            gpt3_prompt = f'''gpt3_prompt = f"""
As a knowledgeable mental health assistant:
I have completed the OCD assessment, achieving a score of {total_score}, leading to the interpretation: '{result_text}'.
1. Based on my score, provide an appropriate empathetic response. And tell me if my score is high or low or moderate. If it is high advise me to go to the hospital.
2. Define Obsessive-Compulsive Disorder (OCD) and provide an example of its symptoms especially early symptoms.
3. Detail negative  impacts of OCD on daily life if not addressed.
4. Suggest detailed natural coping mechanisms and strategies for managing OCD.
5. Acknowledge me on my  efforts in taking the assessment.

"""
gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
'''
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            #st.write(result_text)
            st.write(f"{gpt3_response}")

            reminder_text = {
            "English": """
         <span style="color:green">**Reminder:** These insights are based on the provided conversation and are for informational purposes only. 
        They are not a definitive diagnosis. Please consult with a healthcare professional for a comprehensive assessment.</span>
        """,
        "Swahili": """
        <span style="color:green">**Kumbusho:** Kumbuka kwamba mazungumzo yaliyotolewa na ni kwa madhumuni ya taarifa pekee.
        Hayawakilishi utambuzi wala tathmini  kamili ya kitabibu. Tafadhali shauriana na mtaalamu wa afya kwa tathmini kamili.</span>
        """
}

            st.markdown(reminder_text[selected_language], unsafe_allow_html=True)

    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()
            
def ptsd_assessment(selected_language):
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data(selected_language)  # Passing the selected_language
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender
    if selected_language == "English":
        st.write("### PTSD Assessment (Post-Traumatic Stress Disorder)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya PTSD (Matatizo ya Msongo Baada ya Tukio Baya)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)

  

    #st.title("PTSD Assessment")
    
    questions = {
        "English": [
            "In the past month, have you had nightmares about the event(s) or thought about the event(s) when you did not want to?",
            "In the past month, have you tried hard not to think about the event(s) or went out of your way to avoid situations that reminded you of the event(s)?",
            "In the past month, have you been constantly on guard, watchful, or easily startled?",
            "In the past month, have you felt numb or detached from people, activities, or your surroundings?",
            "In the past month, have you felt guilty or unable to stop blaming yourself or others for the event(s) or any problems the event(s) may have caused?"
        ],
        "Swahili": [
            "Umewahi kuota ndoto mbaya kuhusu tukio hilo au kufikiria juu ya tukio hilo wakati hutaki?",
            "Umewahi kujaribu sana kutofikiria juu ya tukio hilo au ukaepuka hali zinazokumbusha tukio hilo?",
            "Umewahi kuwa na wasiwasi kila mara, makini, au unashtuka kwa urahisi?",
            "Umewahi kuhisi ganzi au kutengwa na watu, shughuli, au mazingira yako?",
            "Umewahi kuhisi hatia au huwezi kuacha kujilaumu au wengine kwa tukio hilo au matatizo yoyote ambayo tukio hilo linaweza kusababisha?"
        ]
    }

    options = {
        "English": ["No", "Yes"],
        "Swahili": ["Hapana", "Ndiyo"]
    }

    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options[selected_language], index=0)
        scores.append(options[selected_language].index(score))
    if selected_language == "Swahili":
        submit_button_label = "Wasilisha"
    else:
        submit_button_label = "Submit"

    col1, col2 = st.columns(2)  # Create two columns for the buttons
    
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu



    if col1.button(submit_button_label):  # Place the "Submit" button in the left column
        # The rest of your existing logic for processing the form submission remains here...
        # This includes summing the scores, generating the interpretation, etc.

        total_score = sum(scores)
        assessment_data = {
                'name': 'PTSD Assessment (Post-Traumatic Stress Disorder)',
                'score': total_score
            }
        store_data_in_database(user_id, age_group, gender, assessment_data)

        
        with st.spinner('Processing your answers...'):
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=4)  # Assuming PTSD max score is 4
            st.plotly_chart(fig)
            # Interpretation based on total score and language
            if total_score >= 3:
                if selected_language == "English":
                    result_text = "Your score suggests that PTSD is likely. Further assessment is warranted."
                elif selected_language == "Swahili":
                    result_text = "Alama zako zinaonyesha kuwa PTSD inawezekana. Uchunguzi zaidi unahitajika."
            else:
                if selected_language == "English":
                    result_text = "Your score suggests that PTSD is less likely. Monitor and re-assess if necessary."
                elif selected_language == "Swahili":
                    result_text = "Alama zako zinaonyesha kuwa PTSD ni chini ya uwezekano. Fuatilia na tathmini tena ikiwa ni lazima."
            
            # Feedback and advice using GPT-3
            gpt3_prompt = f'''gpt3_prompt = f"""
As a knowledgeable mental health assistant:
I have completed the PTSD assessment, achieving a score of {total_score}, which suggests: '{result_text}'.
1. Define Post-Traumatic Stress Disorder (PTSD) and provide examples of its symptoms especially early signs.
2. Detail negative significant impacts of untreated PTSD on an individual's daily life.
3. Offer insights and advice tailored for the user's score and potential condition.
4. Acknowledge the user's initiative in taking the assessment.
5. Provide 10 guidelines on supporting individuals with PTSD, keeping in mind Tanzanian cultural contexts.
6. Recommend dos and don'ts when interacting with someone diagnosed with PTSD.
"""
gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
'''
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            st.write(result_text)
            st.write(f"{gpt3_response}")
            

    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()

def drug_use_addiction_assessment(selected_language):
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data(selected_language)  # Passing the selected_language
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender
    if selected_language == "English":
        st.write("### DAST-10 Assessment (Drug Abuse Screening Test)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya DAST-10 (Tathmini ya  Uchunguzi wa Matumizi ya Dawa za Kulevya)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)


    #st.subheader("DAST-10 Assessment")
    
    if selected_language == "English":
        st.write("These questions refer to the past 12 months.")
    else:  # Swahili
        st.write("Maswali haya yanahusu miezi 12 iliyopita.")
    
    # Questions and options for DAST-10
    questions = {
        "English": [
            "Have you used drugs other than those required for medical reasons?",
            "Do you abuse more than one drug at a time?",
            "Are you always able to stop using drugs when you want to? (If never use drugs, answer “Yes.”)",
            "Have you had 'blackouts' or 'flashbacks' as a result of drug use?",
            "Do you ever feel bad or guilty about your drug use? (If never use drugs, choose “No.”)",
            "Does your spouse (or parents) ever complain about your involvement with drugs?",
            "Have you neglected your family because of your use of drugs?",
            "Have you engaged in illegal activities in order to obtain drugs?",
            "Have you ever experienced withdrawal symptoms (felt sick) when you stopped taking drugs?",
            "Have you had medical problems as a result of your drug use (e.g., memory loss, hepatitis, convulsions, bleeding, etc.)?"
        ],
        "Swahili": [
            "Umewahi kutumia dawa zingine zaidi ya zile zinazohitajika kwa sababu za kiafya?",
            "Je, unatumia dawa zaidi ya moja kwa wakati mmoja?",
            "Je, unaweza kuacha kutumia dawa unapotaka? (Ikiwa haujawahi kutumia dawa, jibu “Ndiyo.”)",
            "Je, umepata 'kupoteza fahamu' au 'kurejea nyuma' kama matokeo ya matumizi ya dawa?",
            "Je, unawahi kujisikia vibaya au hatia kuhusu matumizi yako ya dawa? (Ikiwa haujawahi kutumia dawa, chagua “Hapana.”)",
            "Je, mwenzi wako (au wazazi) analalamika juu ya uhusiano wako na dawa?",
            "Je, umewapuuza familia yako kwa sababu ya matumizi yako ya dawa?",
            "Je, umeshiriki katika shughuli haramu ili kupata dawa?",
            "Je, umewahi kupata dalili za kujiondoa (kuhisi mgonjwa) unapoacha kuchukua dawa?",
            "Je, umepata matatizo ya kiafya kama matokeo ya matumizi yako ya dawa (kwa mfano, kupoteza kumbukumbu, hepatitis, kifafa, kutokwa na damu, nk)?"
        ]
    }
    
    options = {
        "English": ["No", "Yes"],
        "Swahili": ["Hapana", "Ndiyo"]
    }
    
    # Capture the scores for each question
    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options[selected_language], index=0)
        scores.append(options[selected_language].index(score))

    if selected_language == "Swahili":
        submit_button_label = "Wasilisha"
    else:
        submit_button_label = "Submit"

    col1, col2 = st.columns(2)  # Create two columns for the buttons
    
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu



    if col1.button(submit_button_label, key="submit_drug_use"):  # Unique key added and "Submit" button in the left column
        with st.status(state="running", label="Processing your answers..."):
            # Handle the special case for question 3
            scores[2] = 1 - scores[2]

            # Computing the total score
            total_score = sum(scores)
            
           
            assessment_data = {
                'name': 'Drug DAST-10 Assessment',
                'score': total_score
            }
            store_data_in_database(user_id, age_group, gender, assessment_data)

            
            
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=10)  # Setting DAST-10 max score to 10
            
            # Sending the result to GPT-3 for insights and advice
            gpt3_prompt = f"""
            As an informed mental health assistant:
            I have completed the DAST-10 drug abuse assessment, obtaining a score of {total_score} out of 10. 
            1. Greet me and Tell me if my score is high or low or moderate.
            2. Define Drug Abuse Disorder and provide a brief overview and early signs and symptoms.
            3. List detailed negative significant impacts of unchecked drug abuse on one's daily life and health.
            4. Offer insights, coping strategies, and advice tailored to the  score and potential condition.
            5. Acknowledge the my  effort and initiative in taking the assessment.
            6.If my score is too high advise me to vist hospital immediately
           
            """
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
        
        # After processing, directly display the results
        st.plotly_chart(fig)  # Displaying the gauge chart
        
        # Displaying the result based on the total score
        if total_score == 0:
            st.write("No problems reported. Suggested action: None at this time." if selected_language == "English" else "Hakuna matatizo yaliyoripotiwa. Hatua iliyopendekezwa: Hakuna kwa wakati huu.")
        elif total_score <= 2:
            st.write("Low level of problems. Suggested action: Monitor, re‐assess at a later date." if selected_language == "English" else "Kiwango cha chini cha matatizo. Hatua iliyopendekezwa: Fuatilia, tathmini tena baadaye.")
        elif total_score <= 4:
            st.write("Moderate level of problems. Suggested action: Further investigation." if selected_language == "English" else "Kiwango cha wastani cha matatizo. Hatua iliyopendekezwa: Uchunguzi zaidi.")
        else:
            st.write("Substantial level of problems. Suggested action: Intensive assessment." if selected_language == "English" else "Kiwango kikubwa cha matatizo. Hatua iliyopendekezwa: Tathmini ya kina.")
        
        st.write(f"{gpt3_response}")  # Displaying the GPT-3 insights

   
        
    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()

def adhd_assessment(selected_language):
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data(selected_language)  # Passing the selected_language
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender

    
    if selected_language == "English":
        st.write("### ASRS-v1.1 Assessment (Adult ADHD Self-Report Scale)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya ASRS-v1.1 (Kipimo cha Kujitathmini ADHD kwa Watu Wazima)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)

    # Continueing  with the ASRS-v1.1 Questions and response options
    questions = {
        "English": [
            "How often do you have trouble wrapping up the final details of a project, once the challenging parts have been done?",
            "How often do you have difficulty getting things in order when you have to do a task that requires organization?",
            "How often do you have problems remembering appointments or obligations?",
            "When you have a task that requires a lot of thought, how often do you avoid or delay getting started?",
            "How often do you fidget or squirm with your hands or feet when you have to sit down for a long time?",
            "How often do you feel overly active and compelled to do things, like you were driven by a motor?"
        ],
        "Swahili": [
            "Mara ngapi unapata shida kukamilisha au kumalizia mradi (Project), mara tu sehemu ngumu zimekwishafanywa?",
            "Mara ngapi unapata shida kupangilia vitu unapohitaji kufanya kazi inayohitaji mpangilio?",
            "Mara ngapi una shida kukumbuka miadi au majukumu?",
            "Unapofanya kazi inayohitaji mawazo mengi, mara ngapi unaepuka au kuahirisha kuanza?",
            "Mara ngapi unasisitiza au kusonga na mikono yako au miguu unapolazimika kukaa kwa muda mrefu?",
            "Mara ngapi unahisi kuwa na nguvu sana na kulazimika kufanya mambo, kana kwamba unaendeshwa na injini?"
        ]
    }

    options = {
        "English": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "Swahili": ["Kamwe", "Mara chache", "Wakati mwingine", "Mara nyingi", "Mara nyingi sana"]
    }

    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options[selected_language], index=0)
        scores.append(options[selected_language].index(score))

    if selected_language == "Swahili":
            submit_button_label = "Wasilisha"
    else:
        submit_button_label = "Submit"

    col1, col2 = st.columns(2)  # Create two columns for the buttons
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu


    if col1.button(submit_button_label, key="Asrs_Assesment"):  # Unique key added and "Submit" button in the left column
        # Handle the special case for question 3
        scores[2] = 1 - scores[2]

        # Computing the total score
        total_score = sum(scores)
    
     
        assessment_data = {
            'name': 'ADHD Assessment',
            'score': total_score
        }
        store_data_in_database(user_id, age_group, gender, assessment_data)


        with st.status(state="running", label="Processing your answers..."):
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=10)  # Setting DAST-10 max score to 10
            st.plotly_chart(fig) 
        
            # Displaying the result based on the total score
            if total_score == 0:
                st.write("No problems reported. Suggested action: None at this time." if selected_language == "English" else "Hakuna matatizo yaliyoripotiwa. Hatua iliyopendekezwa: Hakuna kwa wakati huu.")
            elif total_score <= 2:
                st.write("Low level of problems. Suggested action: Monitor, re‐assess at a later date." if selected_language == "English" else "Kiwango cha chini cha matatizo. Hatua iliyopendekezwa: Fuatilia, tathmini tena baadaye.")
            elif total_score <= 4:
                st.write("Moderate level of problems. Suggested action: Further investigation." if selected_language == "English" else "Kiwango cha wastani cha matatizo. Hatua iliyopendekezwa: Uchunguzi zaidi.")
            else:
                st.write("Substantial level of problems. Suggested action: Intensive assessment." if selected_language == "English" else "Kiwango kikubwa cha matatizo. Hatua iliyopendekezwa: Tathmini ya kina.")
            
            # Sending the result to GPT-3 for insights and advice
            gpt3_prompt = f"""
            As an informed mental health assistant:
            I have completed ADHD assessment, obtaining a score of {total_score} out of 10.
            1. Based on the score tell me if my score is high or low
            2. Define ADHD  and provide a brief overview.
            3. List negative significant impacts of unchecked ADHD on one's daily life and health.
            4. Offer insights, natural coping strategies, and advice tailored to the user's score and potential condition.
            5. Acknowledge my effort and initiative in taking the assessment.
            6. Suggest  strategies to support individuals struggling with drug addiction.
         
            """
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
            st.write(f"{gpt3_response}")

    
    
        
    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()
                
def psq_assessment(selected_language):
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data(selected_language)  # Passing the selected_language
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender

    if selected_language == "English":
        st.write("### Psychosis Screening Questionnaire (PSQ) Assessment")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya Maswali ya Kuchunguza Wazimu (PSQ)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)

    # PSQ Questions and response options
    psq_questions = {
        "English": [
            "Over the past year, have there been times when you felt very happy indeed without a break for days on end?",
            "Over the past year, have you ever felt that your thoughts were directly interfered with or controlled by some outside force or person?",
            "Over the past year, have there been times when you felt that people were against you?",
            "Over the past year, have there been times when you felt that something strange was going on?",
            "Over the past year, have there been times when you heard or saw things that other people couldn’t?"
        ],
        "Swahili": [
            "Katika kipindi cha mwaka uliopita, je, kumekuwa na wakati ambapo umehisi furaha sana bila mapumziko kwa siku kadhaa mfululizo?",
            "Katika kipindi cha mwaka uliopita, je, umewahi kuhisi kuwa mawazo yako yalipingwa moja kwa moja au kudhibitiwa na nguvu au mtu wa nje?",
            "Katika kipindi cha mwaka uliopita, je, kumekuwa na wakati ambapo umehisi watu wanakupinga?",
            "Katika kipindi cha mwaka uliopita, je, kumekuwa na wakati ambapo umehisi kuna jambo la kushangaza linaendelea?",
            "Katika kipindi cha mwaka uliopita, je, kumekuwa na wakati ambapo umesikia au kuona vitu ambavyo watu wengine hawawezi?"
        ]
    }

    options = {
        "English": ["No", "Yes"],
        "Swahili": ["Hapana", "Ndiyo"]
    }

    psq_scores = []
    for question in psq_questions[selected_language]:
        score = st.selectbox(question, options[selected_language], index=0)
        psq_scores.append(options[selected_language].index(score))

        if selected_language == "Swahili":
            submit_button_label = "Wasilisha"
        else:
            submit_button_label = "Submit"

    col1, col2 = st.columns(2)  # Create two columns for the buttons
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu



    if col1.button(submit_button_label, key="submit_ptsd"):  
        total_psq_score = sum(psq_scores)
        
       
        assessment_data = {
            'name': 'Ptsd Assessment',
            'score': total_psq_score
        }
        store_data_in_database(user_id, age_group, gender, assessment_data)

        
        with st.spinner('Processing your answers...'):
            # Create and display the gauge chart
            max_psq_score = len(psq_questions[selected_language])  # assuming each question can have a max score of 1
            fig = create_gauge_chart(total_psq_score, max_score=max_psq_score)
            st.plotly_chart(fig)
            
            # Interpretation based on total PSQ score and language
            # Note: The interpretation criteria below is just a placeholder and might need to be adjusted based on clinical guidelines.
            if total_psq_score >= 2:
                result_text = "Your score suggests the presence of significant psychotic symptoms. Further assessment by a mental health professional is recommended." if selected_language == "English" else "Alama zako zinaonyesha uwepo wa dalili kubwa za wazimu. Inapendekezwa kufanyiwa tathmini zaidi na mtaalamu wa afya ya akili."
            else:
                result_text = "Your score suggests no significant psychotic symptoms. Continue to monitor your well-being." if selected_language == "English" else "Alama zako zinaonyesha hakuna dalili kubwa za wazimu. Endelea kufuatilia ustawi wako."

            st.write(result_text)
            gpt3_prompt = f"You are a help full assistant"
            gpt3_prompt = f'''
As a knowledgeable mental health assistant:
I have taken  a Shizophrenia assessment and achieved a score of {total_psq_score} out of a maximum possible score of {max_psq_score}. 

1) Tell me if my score is high or low
2) What is Shizophrenia and what are the symptoms and early signs.
3)Encourage me to go to the hospital for detailed check up

Lastly, acknowledge my  initiative in taking the assessment and emphasize the importance of mental well-being.
 '''

            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            st.write(f"{gpt3_response}")



    
    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()
            
            
def depression_assessment(selected_language):
    
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data(selected_language)  # Passing the selected_language
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender

    if selected_language == "English":
        st.write("### Depression Assessment (PHQ-9)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya Sonona (PHQ-9)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)

    # PHQ-9 Questions and response options
    questions = {
        "English": [
            "Little interest or pleasure in doing things?",
            "Feeling down, depressed, or hopeless?",
            "Trouble falling or staying asleep, or sleeping too much?",
            "Feeling tired or having little energy?",
            "Poor appetite or overeating?",
            "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
            "Trouble concentrating on things, such as reading the newspaper or watching television?",
            "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual?",
            "Thoughts that you would be better off dead, or of hurting yourself?"
        ],
        "Swahili": [
            "Unaonyesha kupoteza hamu au raha katika kufanya mambo?",
            "Unahisi huzuni, unyonge, au kukata tamaa?",
            "Una Matatizo ya Kukosa Usingizi, au kulala sana?",
            "Kujihisi umechoka au kukosa nguvu?",
            "Hamu ndogo ya kula au kula kupita kiasi?",
            "Kujisikia vibaya kuhusu wewe mwenyewe — au kwamba umeshindwa au umewaangusha familia yako?",
            "Matatizo ya kuzingatia mambo, kama kusoma gazeti au kutazama televisheni?",
            "Kutembea au kuzungumza polepole sana kiasi kwamba watu wengine wangeweza kutambua? Au kinyume chake — kuwa na wasiwasi sana au kutulia kiasi kwamba umekuwa ukitembea sana kuliko kawaida?",
            "Mawazo kwamba ingekuwa bora kwako kufa, au ya kujiumiza?"
        ]
    }

    options = {
        "English": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Swahili": ["Hapana Kabisa", "Baadhi ya siku", "Zaidi ya nusu ya siku", "Karibu kila siku"]
    }

    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options=options[selected_language], index=0)
        scores.append(options[selected_language].index(score))
    
    if selected_language == "Swahili":
            submit_button_label = "Wasilisha"
    else:
        submit_button_label = "Submit"


    col1, col2 = st.columns(2)  # Create two columns for the buttons
    
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu



    

    if col1.button(submit_button_label, key="submit_depression"):
    
        total_score = sum(scores)
        
       
        assessment_data = {
            'name': 'Depression Assessment',
            'score': total_score
        }
        store_data_in_database(user_id, age_group, gender, assessment_data)

        with st.spinner('Processing the input and generating predictions...'):
       

            # Displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=27)
            st.plotly_chart(fig)

            # Get Interpretation based on the total score
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
                if total_score <= boundary:
                    user_interpretation = interpretations[selected_language][i]
                    break
            else:
                user_interpretation = interpretations[selected_language][4]

            # Feedback and advice using GPT-3
            gpt3_prompt = f"You are a help full assistant"
            gpt3_prompt = f'''As a helpful mental health assistant, consider the following: 
I have taken a depression assessment and scored {total_score} out of a maximum of 27, suggesting: '{user_interpretation}'.
1. Provide an empathetic response based on my  score and tell me if my score is high, low or moderate.
2. Explain what depression is and its potential consequences if not addressed.
3. Offer coping natural strategies and insights.
4. List pieces of advice on supporting individuals with depression, reflecting Tanzanian culture.
5. Mention things one should and shouldn't do when interacting with someone struggling with depression.
6.Congratulate me for taking this test. And if my score is high advice me to go to the hospital.
'''

            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            st.write(user_interpretation)
            st.write(f"{gpt3_response}")
            
            reminder_text = {
            "English": """
         <span style="color:green">**Reminder:** These insights are based on the provided conversation and are for informational purposes only. 
        They are not a definitive diagnosis. Please consult with a healthcare professional for a comprehensive assessment.</span>
        """,
        "Swahili": """
        <span style="color:green">**Kumbusho:** Kumbuka kwamba mazungumzo yaliyotolewa na ni kwa madhumuni ya taarifa pekee.
        Hayawakilishi utambuzi wala tathmini  kamili ya kitabibu. Tafadhali shauriana na mtaalamu wa afya kwa tathmini kamili.</span>
        """
}
            st.markdown(reminder_text[selected_language], unsafe_allow_html=True)

   
  
    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()
                
def iqcode_assessment(selected_language):
    # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
        user_id, age_group, gender = collect_user_data()
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender

    if selected_language == "English":
        st.write("### IQCODE Assessment")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya IQCODE")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)

    # IQCODE Questions and response options
    questions = {
        "English": [
            "Does the individual forget recent events?",
            "Does the individual repeat the same questions or stories within a short period?",
            "Does the individual have difficulty remembering names of family members or close friends?",
            "Does the individual have difficulty finding their way around familiar places?",
            "Does the individual forget to pay bills or manage finances?",
            "Does the individual have difficulty using household appliances or tools?",
            "Does the individual forget appointments or important dates?",
            "Does the individual have trouble recognizing familiar faces?",
            "Does the individual become confused about the time, date, or place?",
            "Does the individual misplace items frequently?",
            "Does the individual struggle to follow a conversation or TV show?",
            "Does the individual have difficulty learning how to use new devices or gadgets?",
            "Does the individual have trouble dressing appropriately for the weather or occasion?",
            "Does the individual forget to eat or prepare meals?",
            "Does the individual have difficulty with personal hygiene and grooming?",
            "Does the individual exhibit changes in personality or behavior?"
        ],
        "Swahili": [
            "Je, mtu anasahau matukio ya hivi karibuni?",
            "Je, mtu anarudia maswali au hadithi zilezile kwa muda mfupi?",
            "Je, mtu anashindwa kumbuka majina ya wanafamilia au marafiki wa karibu?",
            "Je, mtu anapotea kutafuta njia katika maeneo ya kawaida?",
            "Je, mtu anasahau kulipa bili au kusimamia fedha?",
            "Je, mtu anapata shida kutumia vifaa au zana za nyumbani?",
            "Je, mtu anasahau mikutano au tarehe muhimu?",
            "Je, mtu anapata shida kutambua nyuso za familia na marafiki wa karibu?",
            "Je, mtu anakuwa na mkanganyiko kuhusu wakati, tarehe, au mahali?",
            "Je, mtu anaweka vitu mahali pasipofaa mara kwa mara?",
            "Je, mtu anapata shida kufuatilia mazungumzo au kipindi cha TV?",
            "Je, mtu anasumbuliwa na kujifunza jinsi ya kutumia vifaa vipya au vitu?",
            "Je, mtu anashindwa kuvaa kwa usahihi kulingana na hali ya hewa au tukio?",
            "Je, mtu anasahau kula au kuandaa chakula?",
            "Je, mtu anapata shida na usafi binafsi na urembo?",
            "Je, mtu anabadilisha tabia au mwenendo wake?"
        ]
    }

    options = {
        "English": ["Never", "Rarely", "Sometimes", "Often"],
        "Swahili": ["Kamwe", "Mara chache", "Wakati mwingine", "Mara nyingi"]
    }

    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options=options[selected_language], index=0)
        scores.append(options[selected_language].index(score))

    col1, col2 = st.columns(2)  # Create two columns for the buttons

    # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)

    # Use the language-specific labels for buttons
    if col2.button(back_button_label, key='back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu

    if col1.button('Submit', key="submit_iqcode"):  # Unique key added and "Submit" button in the left column
        total_score = sum(scores)
        assessment_data = {
            'name': 'IQCODE Assessment',
            'score': total_score
        }
        store_data_in_database(user_id, age_group, gender, assessment_data)

        with st.spinner('Processing the input and generating predictions...'):
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=64)  # Assuming IQCODE max score is 64
            st.plotly_chart(fig)

            # IQCODE Interpretation based on total score and language
            if selected_language == "English":
                if total_score <= 15:
                    result_text = "Your score suggests minimal or no cognitive decline."
                elif total_score <= 30:
                    result_text = "Your score suggests mild cognitive decline."
                elif total_score <= 45:
                    result_text = "Your score suggests moderate cognitive decline."
                else:
                    result_text = "Your score suggests severe cognitive decline."
            elif selected_language == "Swahili":
                if total_score <= 15:
                    result_text = "Alama zako zinaonyesha dalili ndogo au hakuna upungufu wa kiakili."
                elif total_score <= 30:
                    result_text = "Alama zako zinaonyesha upungufu wa kiakili wa wastani."
                elif total_score <= 45:
                    result_text = "Alama zako zinaonyesha upungufu wa kiakili wa kati."
                else:
                    result_text = "Alama zako zinaonyesha upungufu wa kiakili mkali."

            # Feedback and advice using GPT-3
            gpt3_prompt = f"You are a helpful assistant"
            gpt3_prompt = f'''gpt3_prompt = f"""
As a knowledgeable mental health assistant:
I have completed the IQCODE(Cognitive Decline)  assessment for my relative, scoring {total_score} out of 64, indicating: '{result_text}'.
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
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            st.write(result_text)
            st.write(f"{gpt3_response}")
            reminder_text = {
                "English": """
             <span style="color:green">**Reminder:** These insights are based on the provided conversation and are for informational purposes only. 
            They are not a definitive diagnosis. Please consult with a healthcare professional for a comprehensive assessment.</span>
            """,
                "Swahili": """
                <span style="color:green">**Kumbusho:** Kumbuka kwamba mazungumzo yaliyotolewa na ni kwa madhumuni ya taarifa pekee.
                Hayawakilishi utambuzi wala tathmini  kamili ya kitabibu. Tafadhali shauriana na mtaalamu wa afya kwa tathmini kamili.</span>
                """
            }

            st.markdown(reminder_text[selected_language], unsafe_allow_html=True)
       
    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()

def bipolar_assessment(selected_language):
     # 1. Collect user data at the beginning
    if 'user_id' not in st.session_state or not st.session_state.get('age_group') or not st.session_state.get('gender'):
    
        user_id, age_group, gender = collect_user_data()
        st.session_state.user_id = user_id
        st.session_state.age_group = age_group
        st.session_state.gender = gender
        # Check if both Age Group and Gender are selected
        if not age_group or not gender:
            st.warning("Please select both Age Group and Gender to proceed.")
            return  # Exit the function early without displaying the questions
    else:
        user_id = st.session_state.user_id
        age_group = st.session_state.age_group
        gender = st.session_state.gender

    if selected_language == "English":
        st.write("### Bipolar Assessment (YMRS)")
        st.write("""
        **Disclaimer:** This tool is for informational purposes and is not a diagnostic tool. 
        The results from this tool do not replace professional medical advice. 
        Always consult with a healthcare professional for a comprehensive assessment.
        """)
    elif selected_language == "Swahili":
        st.write("### Tathmini ya Bipolar (YMRS)")
        st.write("""
        **Onyo:** Zana hii ni kwa madhumuni ya taarifa na sio zana ya utambuzi.
        Matokeo kutoka kwa zana hii hayachukui nafasi ya ushauri wa matibabu wa kitaalamu.
        Shauriana daima na mtaalamu wa afya kwa tathmini kamili.
        """)

    # Continue with the YMRS Questions and response options
    # Bipolar Questions and response options
    questions = {
        "English": [
            "Is there abnormally cheerful, euphoric, or high mood?",
            "Is there increased motor activity? Does the individual pace around the room, fidget, or tap fingers?",
            "Does the individual exhibit more energy than usual? Is there an increased need for physical activity?",
            "Is there an increase in initiating activities? Is the individual more socially engaged or taking on new projects?",
            "Is there an increase in sexual interest or activity?",
            "Is there a significant reduction in sleep? Is there a decrease in the need for sleep?",
            "Is the individual irritable or easily annoyed? Does he or she respond aggressively or with anger to minor annoyances?",
            "Is there an increase in the amount of speech? Is the individual talking more quickly or more loudly than usual?",
            "Does the individual experience racing thoughts, flight of ideas, or incoherent speech?",
            "Does the thought content indicate grandiosity, delusions, or other abnormal beliefs?",
            "Is the behavior disturbing to others? Is there evidence of impaired judgment or disruptive behavior?"
        ],
        "Swahili": [
            "Je, kuna hali ya kufurahi, euphoria, au hisia za juu zisizo za kawaida?",
            "Je, kuna ongezeko la shughuli za mwili? Je, mtu huzunguka chumbani, kutapatapa, au kubonyeza vidole?",
            "Je, mtu anaonyesha nishati zaidi kuliko kawaida? Je, kuna ongezeko la haja ya shughuli za mwili?",
            "Je, kuna ongezeko la kuanzisha shughuli? Je, mtu anashiriki zaidi kijamii au kuchukua miradi mipya?",
            "Je, kuna ongezeko la maslahi au shughuli za kingono?",
            "Je, kuna upungufu mkubwa wa usingizi? Je, kuna kupungua kwa haja ya kulala?",
            "Je, mtu ni mwenye kukerwa au kuchokozeka kwa urahisi? Je, anajibu kwa hasira au ghadhabu kwa maudhi madogo?",
            "Je, kuna ongezeko la kiasi cha usemi? Je, mtu anazungumza kwa haraka au kwa sauti kubwa kuliko kawaida?",
            "Je, mtu anapata mawazo yanayokimbia, wazo la kuruka, au usemi usio na mpangilio?",
            "Je, maudhui ya mawazo yanaonyesha kiburi, wazimu, au imani nyingine zisizo za kawaida?",
            "Je, tabia inawasumbua wengine? Je, kuna ushahidi wa hukumu iliyopunguzwa au tabia yenye kuvuruga?"
        ]
    }

    options = {
        "English": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Swahili": ["Hapana Kabisa", "Siku kadhaa", "Zaidi ya nusu ya siku", "Karibu kila siku"]
    }

    scores = []
    for question in questions[selected_language]:
        score = st.selectbox(question, options=options[selected_language], index=0)
        scores.append(options[selected_language].index(score))

    col1, col2 = st.columns(2)  # Create two columns for the buttons
    
      # Get the button labels based on the language
    back_button_label, submit_button_label = get_button_labels(selected_language)
    
     # Use the language-specific labels for buttons
    if col2.button(back_button_label, key = 'back'):  # "Back to main menu"
        st.session_state.page = "menu"  # Set the page state to "menu"
        st.experimental_rerun()  # Rerun the app to go to the main menu



    if col1.button('Submit', key="submit_bipolar"):  # Unique key added and "Submit" button in the left column
        
        total_score = sum(scores)
        assessment_data = {
            'name': 'Bipolar Assesment',
            'score': total_score
        }
        store_data_in_database(user_id, age_group, gender, assessment_data)

        with st.spinner('Processing the input and generating predictions...'):

  
            # Creating and displaying the gauge chart
            fig = create_gauge_chart(total_score, max_score=60)  # Assuming YMRS max score is 60
            st.plotly_chart(fig)

            # YMRS Interpretation based on total score and language
            if selected_language == "English":
                if total_score <= 12:
                    result_text = "Your score suggests Minimal or no manic symptoms."
                elif total_score <= 20:
                    result_text = "Your score suggests Mild manic symptoms."
                elif total_score <= 30:
                    result_text = "Your score suggests Moderate manic symptoms."
                else:
                    result_text = "Your score suggests Severe manic symptoms."
            elif selected_language == "Swahili":
                if total_score <= 12:
                    result_text = "Alama zako zinaonyesha dalili ndogo au hakuna dalili za bipolar."
                elif total_score <= 20:
                    result_text = "Alama zako zinaonyesha dalili za wastani za bipolar."
                elif total_score <= 30:
                    result_text = "Alama zako zinaonyesha dalili kali za bipolar."
                else:
                    result_text = "Alama zako zinaonyesha dalili kali sana za bipolar."

            # Feedback and advice using GPT-3
            gpt3_prompt = f"You are a help full assistant"
            gpt3_prompt = f'''gpt3_prompt = f"""
As a knowledgeable mental health assistant:
I have completed the bipolar assessment, scoring {total_score} out of 40, indicating: '{result_text}'.
1. Provide an empathetic response based on my  score and tell me if my score is high or low.
2. Define bipolar disorder in a broader scope.
3. List negative symptoms of bipolar disorder and explain how it affects daily life.
4. Offer insights and coping strategies and natural ways for managing bipolar disorder.
5. Commend me for undertaking the assessment.
6. If my score is high encourage me to go to the hospital.
"""
gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)
'''
            gpt3_response = get_gpt3_response(gpt3_prompt, selected_language)

            st.write(result_text)
            st.write(f"{gpt3_response}")
            reminder_text = {
            "English": """
         <span style="color:green">**Reminder:** These insights are based on the provided conversation and are for informational purposes only. 
        They are not a definitive diagnosis. Please consult with a healthcare professional for a comprehensive assessment.</span>
        """,
        "Swahili": """
        <span style="color:green">**Kumbusho:** Kumbuka kwamba mazungumzo yaliyotolewa na ni kwa madhumuni ya taarifa pekee.
        Hayawakilishi utambuzi wala tathmini  kamili ya kitabibu. Tafadhali shauriana na mtaalamu wa afya kwa tathmini kamili.</span>
        """
}

            st.markdown(reminder_text[selected_language], unsafe_allow_html=True)
 
    # Determine the labels based on the selected language
    if selected_language == "English":
        return_label = "Return to recommended assessments"
        
    else:  # Swahili
        return_label = "Rudi kwenye tathmini zilizopendekezwa"
   
    
    # Place the "Return to recommended assessments" button at the beginning of your function
    if 'from_model_recommendation' in st.session_state and st.session_state.from_model_recommendation:
        if st.button(return_label):
            st.session_state.selected_assessment = None  # Reset the selected assessment
            st.session_state.page = "assessments"
            st.experimental_rerun()
            
            
def render_assessments_page(selected_language):
    """
    Render the assessments page based on the selected language.
    """

    # Display title based on selected language
    title = "<h3 style='text-align: center;'>Chagua Tathmini:</h3>" if selected_language == "Swahili" else "<h3 style='text-align: center;'>Choose an assessment:</h3>"
    st.markdown(title, unsafe_allow_html=True)
    
    assessments = [
        ("Depression", "depression"),
        ("Anxiety", "anxiety"),
        ("Bipolar", "bipolar"),
        ("Alcohol", "alcohol_addiction"),
        ("Drug", "drug_use_addiction"),
        ("OCD", "ocd"),
        ("PTSD", "ptsd"),
        ("ADHD", "adhd"),
        ("PSQ", "psq"),
        ("Dementia", "iqcode")
    ]

    # Filter assessments based on recommendations
    if 'recommended_assessments' in st.session_state:
        recommended = [assessment for assessment in assessments if assessment[0] in st.session_state.recommended_assessments]
        
        # Create a row of buttons for the recommended assessments
        cols = st.columns(len(recommended))
        for idx, assessment in enumerate(recommended):
            if cols[idx].button(assessment[0], key=f'btn_{assessment[1]}'):
                st.session_state.selected_assessment = assessment[1]
                st.experimental_rerun()

        # Add some spacing
        st.write("\n\n")

        col1, col2, col3 = st.columns([1, 2, 1])

        # Check the selected_language and set the appropriate button label
        if selected_language == "English":
            back_button_label = "Back to Main Menu"
        else:
            back_button_label = "Rudi kwenye Menu Kuu"

        # Use the set button label
        if col2.button(back_button_label):
            st.session_state.page = "menu"
            st.experimental_rerun()
    else:
        for i in range(0, len(assessments), 2):  # Go through the assessments in pairs
            col1, col2 = st.columns(2)
            if col1.button(assessments[i][0], key=f'btn_{assessments[i][1]}'):
                st.session_state.selected_assessment = assessments[i][1]
                st.experimental_rerun()
            if i+1 < len(assessments) and col2.button(assessments[i+1][0], key=f'btn_{assessments[i+1][1]}'):
                st.session_state.selected_assessment = assessments[i+1][1]
                st.experimental_rerun()

        # Add the Back to Main Menu button at the end
        if st.button("Back to Main Menu"):
            st.session_state.page = "menu"
            st.experimental_rerun()
    # Display the chosen assessment based on session state
    if 'selected_assessment' in st.session_state and st.session_state.selected_assessment:
        if 'selected_assessment' in st.session_state:
            if st.session_state.selected_assessment == 'depression':
                depression_assessment(selected_language)
            elif st.session_state.selected_assessment == 'anxiety':
                anxiety_assessment(selected_language)
            elif st.session_state.selected_assessment == 'bipolar':
                bipolar_assessment(selected_language)
            elif st.session_state.selected_assessment == 'alcohol_addiction':
                alcohol_addiction_assessment(selected_language)
            elif st.session_state.selected_assessment == 'drug_use_addiction':
                drug_use_addiction_assessment(selected_language)
            elif st.session_state.selected_assessment == 'ocd':
                ocd_assessment(selected_language)
            elif st.session_state.selected_assessment == 'ptsd':
                ptsd_assessment(selected_language)
            elif st.session_state.selected_assessment == 'adhd':
                adhd_assessment(selected_language)
            elif st.session_state.selected_assessment == 'psq':
                psq_assessment(selected_language)
            elif st.session_state.selected_assessment == 'iqcode':
                iqcode_assessment(selected_language)
                
            
def main():
    set_css()
    initialize_openai()

    selected_language = st.selectbox("Choose your language:", ["English", "Swahili"], key='language_select')
    
    
    if "page" not in st.session_state:
        st.session_state.page = "menu"

    if st.session_state.page == "menu":
        render_main_menu(selected_language)
    elif st.session_state.page == "model_prediction":
        render_model_prediction_page(selected_language)
    elif st.session_state.page == "assessments":
        render_assessments_page(selected_language)




    
    
def render_main_menu(selected_language):
    st.empty()  # Clear previous content
    #st.title("Akili Check")
    
    # Center-aligned title for both languages
    st.markdown("<h1 style='text-align: center;'>Akili Check</h1>", unsafe_allow_html=True)

    # Introduction based on the selected language
    if selected_language == "English":
        st.markdown(
            """
            <h2 style='text-align: center;'>Welcome to Akili Check</h2>
            
            **This tool is designed to help you gain insights into your mental well-being based on the symptoms you report.**

            **Please note:** The insights provided by this tool are based on general patterns and should not be considered definitive conclusions. Always consult with a medical professional for an accurate diagnosis and treatment.

            **We advise** you to begin with the **EARLY-CHECK IN**. After that, you will be directed to the respective assessments.

            **Please be informed:** This tool does not collect any personally identifiable information as it aims to maintain your anonymity.
            """,
            unsafe_allow_html=True,
        )

    else:  # Swahili
        st.markdown(
            """
            <h2 style='text-align: center;'>Karibu Akili Check</h2>
            
            **Zana hii imeundwa kukusaidia kuelewa afya yako ya akili kulingana na dalili unazopitia.**

            **Tafadhali kumbuka** kuwa ufahamu uliotolewa na zana hii unategemea mifumo ya jumla na haipaswi kuchukuliwa kama hitimisho thabiti. Daima washauriane na mtaalamu wa matibabu kwa utambuzi sahihi na matibabu.
            
            **Tafadhali** unashauriwa kuanza na tathmini ya awali kisha tathmini ya awali itakupeleka kwenye tathmini  zaidi kulingana na tathminiya awali.
            
            **Zingatia pia** kwamba hatukusanyi taarifa binafsi kama majina yako, sehemu unapoishi wala chochote kinachokutambua.
            """,
            unsafe_allow_html=True,
        )

    
        
        

    
    if "btn_clicked" not in st.session_state:
        st.session_state.btn_clicked = None

    col1, col2 = st.columns(2)
    
    

    # Display buttons based on the selected language
    if col1.button("Early Check-in" if selected_language == "English" else "Tathmini ya awali"):
        st.session_state.btn_clicked = "model_prediction"
    if col2.button("Assessment" if selected_language == "English" else "Tathmini zaidi"):
        st.session_state.btn_clicked = "assessments"

    if st.session_state.btn_clicked == "model_prediction":
        st.session_state.page = "model_prediction"
        st.experimental_rerun()
    elif st.session_state.btn_clicked == "assessments":
        st.session_state.page = "assessments"
        st.experimental_rerun()



def render_model_prediction_page(selected_language):
    st.empty()  # Clear previous content

    # Apply the styling
    set_age_input_style()

    # Display a title based on the selected language
    title = "Early Check-in" if selected_language == "English" else "Tathmini ya awali"
    st.subheader(title)

    # Collect user's age and gender
    age = st.number_input('Enter your age:', min_value=13, max_value=100, value=None, step=None)

    gender = st.selectbox('Select your gender:', ['', 'Male', 'Female'])

     # Retrieve the appropriate headers and symptoms based on the selected language
    headers = get_headers_by_language(selected_language)
    if selected_language == 'English':
        symptoms_list = {key: list(val.values()) for key, val in swahili_to_english_mapping.items()}
    else:
        symptoms_list = {key: list(val.keys()) for key, val in swahili_to_english_mapping.items()}

    selected_symptoms = []
    for condition in headers:
        st.write(f"**{condition}:**")
        
        # Determine the correct English header to access the symptoms list
        english_condition = condition if selected_language == "English" else swahili_to_english_headers[condition]

        for symptom in symptoms_list[english_condition]:
            if st.checkbox(symptom):
                selected_symptoms.append(symptom)

        col1, col2 = st.columns(2)
    # Determine button labels based on the selected language
    predict_label = "Check" if selected_language == "English" else "Check"
    assessment_label = "Go to Assessments" if selected_language == "English" else "Tathmini zaidi"

        # Predict button in the left column
    if col1.button(predict_label, key='UniqueKeyForModelPrediction'):
        if not age:
            age_warning = "Please enter your age." if selected_language == "English" else "Tafadhali ingiza umri wako."
            st.warning(age_warning)
        elif not gender:
            gender_warning = "Please select your gender." if selected_language == "English" else "Tafadhali chagua jinsi yako."
            st.warning(gender_warning)
        elif not selected_symptoms:
            symptoms_warning = "Please select at least one symptom." if selected_language == "English" else "Tafadhali chagua angalau dalili moja."
            st.warning(symptoms_warning)
        else:
            predicted_condition = get_predicted_condition(age, gender, selected_language, selected_symptoms)
            

                                    
                    
                    # Get the recommended assessments based on the predicted condition
            recommended_assessments = get_recommended_assessment(predicted_condition)
            if recommended_assessments:
                st.session_state.from_model_recommendation = True  # Set the flag here
                st.session_state.recommended_assessments = recommended_assessments

                # Check for the selected language and adjust the response accordingly
                if selected_language == "English":
                    recommendation_intro = "Based on your symptoms, we recommend taking the following assessment(s) for a more comprehensive evaluation:"
                else:  # Swahili
                    recommendation_intro = "Kulingana na dalili zako, tunapendekeza ufanye tathmini zifuatazo kwa tathmini kamili zaidi:"

                st.write(f"{recommendation_intro} {', '.join(recommended_assessments)}")
                # Set the prediction made flag to True
                st.session_state.prediction_made = True
                # Store the recommended assessments in the session state
                st.session_state.recommended_assessments = recommended_assessments


    # This "Go to Assessments" button will be available after the Predict button has been pressed
    if 'prediction_made' in st.session_state and st.session_state.prediction_made:
        if col2.button(assessment_label):
            # Reset the prediction made flag
            st.session_state.prediction_made = False
            st.session_state.page = "assessments"
            st.experimental_rerun()
    
if __name__ == "__main__":
    main()
