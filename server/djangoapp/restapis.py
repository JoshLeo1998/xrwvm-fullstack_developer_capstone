import requests
import os
from dotenv import load_dotenv


load_dotenv()

backend_url = os.getenv('backend_url', default="https://example.com/")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="https://sentianalyzer.example.com/",
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = f"{backend_url}{endpoint}?{params}"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None
