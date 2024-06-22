import requests
from bs4 import BeautifulSoup
import json


# URL of the page to scrape
url = "https://api.scrapingdog.com/scrape?api_key=665eb0542739e1784a9213a2&url=https://www.glassdoor.com/Job/texas-us-data-engineer-jobs-SRCH_IL.0,8_IS1347_KO9,22.htm?includeNoSalaryJobs=true"


def fetch_page(url):
    """Fetch the content of the page."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None


def parse_job_listings(html_content):
    """Parse the job listings from the HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    job_listings = soup.select('li[data-test="jobListing"]')
    return job_listings


def extract_data(job):
    """Extract data from a single job listing."""

    def safe_extract(selector):
        element = job.select_one(selector)
        return element.get_text(strip=True) if element else None

    company = safe_extract(".EmployerProfile_compactEmployerName__LE242")
    rating = safe_extract(".EmployerProfile_ratingContainer__ul0Ef span")
    job_title = safe_extract(".JobCard_jobTitle___7I6y")
    location = safe_extract(".JobCard_location__rCz3x")
    salary = safe_extract(".JobCard_salaryEstimate__arV5J")
    description = safe_extract(
        ".JobCard_jobDescriptionSnippet__yWW8q > div:nth-child(1)"
    )
    skills_element = job.select_one(
        ".JobCard_jobDescriptionSnippet__yWW8q > div:nth-child(2)"
    )
    skills = (
        skills_element.get_text(strip=True).replace("Skills:", "").strip()
        if skills_element
        else None
    )

    data = {
        "company": company,
        "rating": rating,
        "job_title": job_title,
        "location": location,
        "salary": salary,
        "description": description,
        "skills": skills,
    }

    return data


def save_data_to_json(data, filename="data/glassdoor_jobs.json"):
    """Save scraped data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    """Main function to orchestrate the scraping process."""
    html_content = fetch_page(url)
    if not html_content:
        return
    job_listings = parse_job_listings(html_content)
    if not job_listings:
        print("No job listings found.")
        return
    all_jobs_data = []
    for job in job_listings:
        job_data = extract_data(job)
        all_jobs_data.append(job_data)
    save_data_to_json(all_jobs_data)


if __name__ == "__main__":
    main()