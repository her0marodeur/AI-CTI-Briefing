# AI-CTI-Briefing

Create custom CTI News Briefings using OpenAI and LangChain.


This is all work in progress and at a very early stage but it is working and I hope for some community input.

### Quick Start

Clone the repo and do:

```
pip install -r requirements.txt
```

Create a .env file by copying and adding keys into the .env.example file.
- OpenAI API key: https://openai.com/blog/openai-api
- Create Telegram bot: https://core.telegram.org/bots/tutorial
- Get Telegram Chat ID: https://diyusthad.com/2022/03/how-to-get-your-telegram-chat-id.html

Set up a CRON job that runs the script daily.

You now get AI powered news. YEAH!

### NOTES:
- The script was build using an API key from a free OpenAI trial and therefore limits the context size a lot. If you are using better models you can achieve better results, by editing the prompts and this in the main.py:

```
llm = OpenAI(max_tokens=2048)
```

### How to make it better?

- Improve the prompts or give the model context about your requirements.
- Add more news sources in [parse_feeds.py](https://github.com/her0marodeur/AI-CTI-Briefing/blob/main/parse_feeds.py) AND [scrape_articles.py](https://github.com/her0marodeur/AI-CTI-Briefing/blob/main/scrape_articles.py).
- Add more channels in [notifiers.py](https://github.com/her0marodeur/AI-CTI-Briefing/blob/main/notifiers.py).

### How does it work?

The tool currently scrapes the following feeds:

- https://www.wired.com/feed/category/security/latest/rss
- https://www.bleepingcomputer.com/feed/
Done in [parse_feeds.py](https://github.com/her0marodeur/AI-CTI-Briefing/blob/main/parse_feeds.py)

And the CVE trends from:
- https://vulmon.com/searchpage?q=&sortby=byactivity
Done in: [cve_intel.py](https://github.com/her0marodeur/AI-CTI-Briefing/blob/main/cve_intel.py)

The tool then selects the most relevant headlines according to the following prompt:

```
Given the headlines: 
{headlines}

From various news sources.

Please select the 3 most interesting headlines for a daily news briefing intended for a Pentester/Red Teamer. 
Please ensure that the headlines are not covering the same topic.
List each headline you select on a new line, preceded by a hyphen and a space. For example:
- Headline 1
- Headline 2
- Headline 3
```
**Note:** If you adjust the number of headlines, append a or delete a '- Headline n' to or from the prompt. 

And summarizes them using the following prompt:

```
Please summarize the following article:

{full_article}

in 80 words.

Focus on the key messages and actionable takeaways for somebody working as a Pentester/Red Teamer.

Include the title in the summary.

Output format should be:

Title

Summary

```

It bundles all the stuff together and ships the final product:

```
Given the full text articles:

{full_articles}

And these CVEs with descriptions

{cve_report}

Please write a news briefing for someone working in Red Teaming and Pentesting. 
From the CVEs and their summaries mention the top 3 with the most critical impact by CVE ID and say which product is affected and how.
Also provide 2 ideas for an interesting tweet for a cybersecurity Twitter account. 
The tweets should not just cite news, but provide some comment or analysis based on the overall context of todays news.
```
