import requests
import json

url = "https://api.scrapingdog.com/linkedinjobs/"
params = {
    "api_key": "665eb0542739e1784a9213a2",
    "field": "data%20engineer",
    "geoid": "102748797",
    "page": "1"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    with open('data/linkedin_jobs.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
else:
    print("Request failed with status code:", response.status_code)