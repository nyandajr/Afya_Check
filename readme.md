# Afya Check

This is AI powered solution mental health solution that helps people to check their mental health status and get help if needed.


# Getting Started

- Fork the repo

    Fork the repo into your account and then 

- Clone the repo by running

    ```bash
    git clone https://github.com/nyandajr/Afya_Check.git
    ```

- Creating virtual environment

    This is a python project and I would like to make a virtual environment for this project so that we don't mess up with our system packages. This is optional but I would recommend you to do so.

    - Create a virtual environment by running in Linux/MacOS

        ```bash
        python3 -m venv AfyaCheck
        ```

        Activate the virtual environment

        ```bash
        source AfyaCheck/bin/activate
        ```

    - Create a virtual environment by running in Windows

        ```bash
        pip install virtualenv
        python -m venv AfyaCheck
        ```
        Activate the virtual environment

        ```bash
        AfyaCheck\Scripts\activate
        ```

- Install the Dependencies

    ```bash
    cd Afya_Check || cd Afya-Check
    pip install -r requirements.txt
    ```


You'll need OpenAI's API Key as we are going to use Langauge model(GPT-3), to curate responses. 

#Setting up OpenAI API Key:
To use this app, you'll need an API key from OpenAI as the app utilizes the GPT-3 model to generate responses.

Locally:
Using Environment Variables:

Set your OpenAI API key as an environment variable:

Linux/macOS:

´´´bash
Copy code
export OPENAI_API_KEY='your_openai_api_key_here'
´´´

Windows (Command Prompt):

cmd
Copy code
set OPENAI_API_KEY=your_openai_api_key_here
Windows (PowerShell):

powershell
Copy code
´´´$env:OPENAI_API_KEY='your_openai_api_key_here' ´´´

In your Streamlit application (mental.py), you can access this environment variable:


python
Copy code
import os
api_key = os.environ.get("OPENAI_API_KEY")
Online (e.g., deploying with Streamlit sharing):
Using Streamlit Sharing:

Deploy your app on Streamlit sharing.

Under the app's settings, find the 'Secrets' section.

Add your OpenAI API key as a secret with the name OPENAI_API_KEY.

In your app, you can access this secret as you would locally:

python
Copy code
import os
api_key = os.environ.get("OPENAI_API_KEY")

#Run the App:
Now, with everything set up, you can run your Streamlit app:
    ```bash
    streamlit run mental.py
    ```
