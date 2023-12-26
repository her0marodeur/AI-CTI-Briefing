import requests
from bs4 import BeautifulSoup
import re

def get_unique_cve_ids_vulnmon():
    url = 'https://vulmon.com/searchpage?q=&sortby=byactivity'
    # Fetch the content of the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the web page")
        return []

    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Regular expression to match CVE IDs
    cve_regex = re.compile(r'CVE-\d{4}-\d{4,7}')

    # Find all CVE IDs in the webpage
    cve_ids = set()
    for text in soup.stripped_strings:
        matches = cve_regex.findall(text)
        for match in matches:
            cve_ids.add(match)

    return list(cve_ids)


def get_cve_summary(cve_id):
    # API endpoint
    url = f"https://cve.circl.lu/api/cve/{cve_id}"

    # Send a GET request to the API
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return None

    try:
        data = response.json()

        # Extract the summary
        summary = data.get('summary', 'No summary available')
    except:
        return("No summary for CVE")
    return summary


def get_cve_report():
    
    interesting_cves = []

    cve_list = get_unique_cve_ids_vulnmon()

    for cve in cve_list:
        cve_summary = get_cve_summary(cve)
        interesting_cves.append(f"{cve}:  {cve_summary}")
    
    return interesting_cves

