def parse_selected_articles_to_list(llm_output):
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

def get_links_for_selected_headlines(articles, selected_headlines):
    links = []
    for headline in selected_headlines:
        for article in articles:
            if article['title'] == headline:
                links.append(article['link'])
                break  # Once the matching article is found, no need to continue the inner loop
    return links