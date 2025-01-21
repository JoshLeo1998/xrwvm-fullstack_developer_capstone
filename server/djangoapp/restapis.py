# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the backend URL provided
backend_url = os.getenv(
    'backend_url',
    default="https://joshleonardi-3030.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="https://sentianalyzer.1qy62yzpmy2y.us-south.codeengine.appdomain.cloud/"
)

# Function for GET requests to the backend
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")
    try:
        # Call GET method from the requests library
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle network exceptions
        print(f"Network exception occurred: {e}")
        return None

# Function to analyze review sentiments
def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print(f"GET from {request_url}")
    try:
        # Call GET method from the requests library
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle network exceptions
        print(f"Network exception occurred: {e}")
        return None

# Function to POST review data
def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    print(f"POST to {request_url} with data {data_dict}")
    try:
        # Call POST method from the requests library
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle network exceptions
        print(f"Network exception occurred: {e}")
        return None

