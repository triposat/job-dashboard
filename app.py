from flask import Flask, render_template
import json
import subprocess
import re

app = Flask(__name__)


def run_scrapers():
    try:
        subprocess.run(["python", "script/linkedin_scraper.py"])
        subprocess.run(["python", "script/indeed_scraper.py"])
        subprocess.run(["python", "script/glassdoor_scraper.py"])
    except Exception as e:
        print(f"Error running scrapers: {e}")


def combine_data():
    linkedin_file = 'data/linkedin_jobs.json'
    with open(linkedin_file, 'r', encoding='utf-8') as file:
        linkedin_data = json.load(file)
        for job in linkedin_data:
            job['company_profile'] = job.get('company_profile').replace(
                "?trk=public_jobs_jserp-result_job-search-card-subtitle", "")

    glassdoor_file = 'data/glassdoor_jobs.json'
    with open(glassdoor_file, 'r', encoding='utf-8') as file:
        glassdoor_data = json.load(file)
        for job in glassdoor_data:
            job['salary'] = job.get('salary') if job.get('salary') else "N/A"
            job['skills'] = job.get('skills') if job.get('skills') else "N/A"

    indeed_file = 'data/indeed_jobs.json'
    with open(indeed_file, 'r', encoding='utf-8') as file:
        indeed_data = json.load(file)
        for job in indeed_data:
            job_descriptions = job.get('jobDescription', [])
            if job_descriptions:
                job['Description'] = ' '.join(
                    [desc.strip() for desc in job_descriptions if desc.strip()])
            else:
                job['Description'] = "N/A"

    with open(indeed_file, 'w') as file:
        json.dump(indeed_data, file, indent=4)
    indeed_data.pop()

    return linkedin_data, glassdoor_data, indeed_data


@app.route('/')
def index():
    try:
        run_scrapers()
        linkedin_data, glassdoor_data, indeed_data = combine_data()
        return render_template('dashboard.html',
                               linkedin_jobs=linkedin_data,
                               glassdoor_jobs=glassdoor_data,
                               indeed_jobs=indeed_data)
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    app.run(debug=True)
