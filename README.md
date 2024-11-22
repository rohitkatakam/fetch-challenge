# Setup Instructions
1. Ensure you have Python 3.7+ installed before setup.
2. Clone this repository into your local terminal and go into the folder (see below commands):
    % git clone {HTTPS link}
    % cd fetch-challenge
3. Create a Python virtual environment and activate with the following commands:
    % python -m venv env
    % source env/bin/activate
4. Install the required packages:
    - pip install -r requirements.txt
5. Start the API:
    % python app.py
6. There will be an HTTP URL ending in '8000' printed near the bottom of your terminal. The API endpoints will be available at {url}/add, {url}/spend, and {url}/balance. 
NOTE: Ensure that in POST requests are in JSON format. This means explicitly setting "Content-Type" to "application/json" whenever you call these POST methods. If testing in Postman, this is usually the default, but can be changed by adding a row to the "Headers" section with key "Content-Type" and value "application/json". 
If you are testing in the terminal, use the following command for GET (only balance endpoint):
    % curl {url}/balance
and use the following for POST (add and spend endpoints):
    % curl -X POST -H "Content-Type: application/json" -d '{data}' {url}/{endpoint}