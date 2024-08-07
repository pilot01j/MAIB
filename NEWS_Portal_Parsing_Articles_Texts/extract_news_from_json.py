import json
import re
import os
import csv
from change_date_format import change_date
from titp_articol import extrage_text


json_file = "articles_list.json"
database_name = 'database.csv'


# Save de extracted info from json file to a table in format csv
def save_to_database(publication_date, web_page_name, source, title, text,link,
                     filename=database_name):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([publication_date, web_page_name, source, title, text, link])


# Extract from articles_list.json file relevant info about articles and check the article_type
def extract_form_json_Google_NEWS(web_page_name):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        for entry in data:
            article_html = entry['article_html']
            try:

                initial_date = ''.join(re.findall(r'<div class=\"OSrXXb rbYSKb LfVVr\" '
                                                                  r'style=\"bottom:0px\"><span>(.*?)</span></div>',
                                                                  article_html))
                publication_date = change_date(initial_date.strip())

                source = re.search(r'<span>(.*?)<\/span>', article_html).group(1)
                title_match = re.search(r'class="n0jPhd ynAwRc MBeuO nDgy9d".*?role="heading".*?>([^<]+)</div>',
                                        article_html, re.DOTALL)
                title = title_match.group(1).replace('\n', '').strip() if title_match else "Title not found"

                link = re.search(r'href="(.*?)"', article_html).group(1)

                text = extrage_text(link)

                print("Date:", publication_date)
                print("Source:", source)
                print("Title:", title)
                print("URL:", link, "\n")
                save_to_database(publication_date, web_page_name, source, title, text, link)

            except AttributeError:
                print("Failed to extract inf. from article.\n")
        # Delete de articles_list.json that contain all information about company articles
        os.remove(json_file)
    except FileNotFoundError:
        print("File not found. Skipping extraction.")
        pass

# Test
# extract_form_json_Google_NEWS('Unimedia.info')
