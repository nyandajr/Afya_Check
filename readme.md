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

- Run the app

    You'll need OpenAI's API Key as we are going to use Langauge model(GPT-3), to curate responses. 


    ```bash
    streamlit run mental.py
    ```
