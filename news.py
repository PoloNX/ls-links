import requests
from bs4 import BeautifulSoup
import json
import re
import html

rss_url = "http://www.logic-sunrise.com/forums/rss/forums/1-news-fr/"

response = requests.get(rss_url)

soup = BeautifulSoup(response.content, features="xml")

news_dict = {}

for index, item in enumerate(soup.select('item')):
    news = {}
    news['title'] = item.title.text
    # Supprime toutes les balises HTML et les caractères spéciaux avec une expression régulière
    content = re.sub(r'<[^>]*>', '', item.description.text)
    news['content'] = html.unescape(content)
    images = {}
    soup_item = BeautifulSoup(item.description.text, features="html.parser")
    img_tags = soup_item.find_all('img')
    for img_index, img_tag in enumerate(img_tags):
        images[f"image_{img_index+1}"] = img_tag['src']
        img_tag.extract()
    news['images'] = images
    news_dict[f"news_{index+1}"] = news

json_data = json.dumps(news_dict, indent=4)

with open('news.json', 'w') as f:
    f.write(json_data)