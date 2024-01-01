import requests
from bs4 import BeautifulSoup
import json



def scrape_article(url):
    if "wired.com" in url:
        article_text = scrape_wired(url)
    elif "bleepingcomputer.com" in url:
        article_text = scrape_bleeping_computer(url)
    
    if len(article_text) > 10240:
        return article_text[:10240]
    else:
        return article_text



def scrape_wired(url):
    # Send a request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the article"

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the <script> tag with the required type attribute
    script_tag = soup.find('script', {'type': 'application/ld+json'})

    if not script_tag:
        return "Script tag with the article data not found"

    # Parse the JSON data inside the script tag
    article_data = json.loads(script_tag.string)

    # Access the article body text
    article_text = article_data.get('articleBody', "Article body not found")
    
    return article_text


def scrape_bleeping_computer(url):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    try:
        # Send a request to the URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code != 200:
            return f"Failed to retrieve the webpage: Status code {response.status_code}"

        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <p> tags
        p_tags = soup.find_all('p')

        # Concatenate text from each <p> tag into one large string
        p_text_combined = ' '.join(tag.get_text().strip() for tag in p_tags)

        return p_text_combined

    except Exception as e:
        return f"An error occurred: {e}"
