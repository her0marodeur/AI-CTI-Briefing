from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import time


from parse_feeds import parse_feeds
from scrape_articles import scrape_article

import dotenv



dotenv.load_dotenv()

def get_links_for_selected_headlines(articles, selected_headlines):
    links = []
    for headline in selected_headlines:
        for article in articles:
            if article['title'] == headline:
                links.append(article['link'])
                break  # Once the matching article is found, no need to continue the inner loop
    return links


def parse_llm_output_to_list(llm_output):
    """
    Parses the LLM output to extract headlines into a list.
    
    :param llm_output: String output from the LLM.
    :return: List of headlines or an empty list if parsing fails.
    """
    headlines_list = []
    for line in llm_output.split('\n'):
        if line.startswith('- '):
            headline = line[2:]  # Remove the "- " at the beginning
            headlines_list.append(headline)
    return headlines_list

headlines = []

articles = parse_feeds()

#print(articles)

for article in articles:
    headlines.append(article["title"])

llm = OpenAI(max_tokens=1024)

summary_template = """
Given the headlines: 
{headlines}

From various news sources.

Please select the 4 most interesting headlines for a daily news briefing intended for a Pentester/Red Teamer. List each headline you select on a new line, preceded by a hyphen and a space. For example:
- Headline 1
- Headline 2
"""

summary_prompt_template = PromptTemplate(
    input_variables=["headlines"], template=summary_template
)

chain = LLMChain(llm=llm, prompt=summary_prompt_template)

llm_output = chain.run(headlines=headlines)

#print(llm_output)

selected_headlines = parse_llm_output_to_list(llm_output)

#print(selected_headlines)

briefing_template = """
Given the headlines: 
{headlines_with_links}

From various news sources.

And the full text articles selected from these headlines:

{full_articles}

Please write a news briefing. 
Also use the headlines provided for your briefing.
If any CVEs are mentioned mention them in a list of CVEs.

"""

briefing_prompt_template = PromptTemplate(
    input_variables=["headlines_with_links", "full_articles"], template=briefing_template
)

chain = LLMChain(llm=llm, prompt=briefing_prompt_template)

full_full_text_articles = []

links = get_links_for_selected_headlines(articles, selected_headlines)

for link in links:
    full_full_text_articles.append(scrape_article(link))


summary_article_template = """
Please summarize the following article:

{full_article}

in 80 words.

Focus on the key messages and actionable takeaways for somebody working as a Pentester/Red Teamer.

Include the title in the summary.

Output format should be:

Title

Summary

"""

summary_article_template = PromptTemplate(
    input_variables=["full_article"], template=summary_article_template
)

summary_chain = LLMChain(llm=llm, prompt=summary_article_template)

full_text_articles= []

for article in full_full_text_articles:
    full_text_articles.append(summary_chain.run(full_article=article))
    time.sleep(20)



llm_output = chain.run(headlines_with_links=articles, full_articles=full_text_articles)

print(llm_output)
for article in full_text_articles:
    print(article)
    print()
    print()