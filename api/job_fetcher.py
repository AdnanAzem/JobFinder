import requests
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_jobs(query, location):
    api_key = os.getenv("JSEARCH_API_KEY")
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {"query": f"{query} in {location}", "page": "1", "num_pages": "1"}
    response = requests.get(url, headers=headers, params=params)

    return response.json().get("data", [])