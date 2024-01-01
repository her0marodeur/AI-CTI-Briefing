### Needed Imports

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import time
import dotenv


### Project Imports

from parse_feeds import parse_feeds
from scrape_articles import scrape_article
from cve_intel import get_cve_report
from notifiers import send_telegram_message
from helpers import parse_selected_articles_to_list, get_links_for_selected_headlines



dotenv.load_dotenv()
llm = OpenAI(max_tokens=2048)


##### Prepare Articles and CVEs
headlines = []

articles = parse_feeds()


for article in articles:
    headlines.append(article["title"])

cve_report = get_cve_report()



summary_template = """
Given the headlines: 
{headlines}

From various news sources.

Please select the 3 most interesting headlines for a daily news briefing intended for a Pentester/Red Teamer. 
Please ensure that the headlines are not covering the same topic.
List each headline you select on a new line, preceded by a hyphen and a space. For example:
- Headline 1
- Headline 2
- Headline 3
"""

summary_prompt_template = PromptTemplate(
    input_variables=["headlines"], template=summary_template
)

chain = LLMChain(llm=llm, prompt=summary_prompt_template)

llm_output = chain.run(headlines=headlines)


selected_headlines = parse_selected_articles_to_list(llm_output)


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


#### Create Briefing

briefing_template = """

Given the full text articles:

{full_articles}

And these CVEs with descriptions

{cve_report}

Please write a news briefing for someone working in Red Teaming and Pentesting. 
From the CVEs and their summaries mention the top 3 with the most critical impact by CVE ID and say which product is affected and how.
Also provide 2 ideas for an interesting tweet for a cybersecurity Twitter account. 
The tweets should not just cite news, but provide some comment or analysis based on the overall context of todays news. 
"""

briefing_prompt_template = PromptTemplate(
    input_variables=["full_articles", "cve_report"], template=briefing_template
)

chain = LLMChain(llm=llm, prompt=briefing_prompt_template)


llm_output = chain.run(full_articles=full_text_articles, cve_report=cve_report)

print(llm_output)

#### Send Briefing

send_telegram_message(llm_output)
