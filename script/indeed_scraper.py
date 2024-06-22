import requests
import json

url = "https://api.scrapingdog.com/indeed"
api_key = "665eb0542739e1784a9213a2"
job_search_url = "https://indeed.com/jobs?q=data+engineer&l=Texas"

params = {"api_key": api_key, "url": job_search_url}

response = requests.get(url, params=params)

if response.status_code == 200:
    json_response = response.json()
    with open('data/indeed_jobs.json', 'w') as json_file:
        json.dump(json_response, json_file, indent=4)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
