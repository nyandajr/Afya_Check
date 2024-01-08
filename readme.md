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



To use this app, you'll need an API key from OpenAI, as the application relies on the GPT-3 model to generate responses.

### Local Setup

1. **Using Environment Variables**:

    Set your OpenAI API key as an environment variable:

    - **Linux/macOS**:
      ```bash
      export OPENAI_API_KEY='your_openai_api_key_here'
      ```

    - **Windows (Command Prompt)**:
      ```cmd
      set OPENAI_API_KEY=your_openai_api_key_here
      ```

    - **Windows (PowerShell)**:
      ```powershell
      $env:OPENAI_API_KEY='your_openai_api_key_here'
      ```

2. **Accessing the API Key in Streamlit**:

    In your Streamlit application (`mental.py`), you can access this environment variable:
    ```python
    import os
    api_key = os.environ.get("OPENAI_API_KEY")
    ```

### Deployment (e.g., Streamlit Sharing)

1. **Using Streamlit Sharing**:

    If you're deploying with Streamlit sharing:

    - Deploy your app on Streamlit sharing.
    - Navigate to the app's settings and find the 'Secrets' section.
    - Add your OpenAI API key as a secret with the name `OPENAI_API_KEY`.

    You can access the secret in your app the same way as in the local setup:

    ```python
    import os
    api_key = os.environ.get("OPENAI_API_KEY")
    ```

## Running the App

Once you've set everything up, you can run the Streamlit app using the following command:

```bash
streamlit run mental.py

