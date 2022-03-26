import time
import json

from news_scraper import NewsScraper
from vac_scraper import VacScraper

news_scraper = NewsScraper('ru', 'pol', 'blr')
news_data = news_scraper.get_data()
vac_scraper = VacScraper('ru', 'pol', 'blr')
vac_data = vac_scraper.get_data()

with open('news.json', 'w', encoding='utf8') as wf:
    json.dump(news_data, wf, indent=4, ensure_ascii=False)

with open('vac.json', 'w', encoding='utf8') as wf:
    json.dump(vac_data, wf, indent=4, ensure_ascii=False)

all_data = {'centers': vac_data, 'news': news_data}

with open('all.json', 'w', encoding='utf8') as wf:
    json.dump(all_data, wf, indent=4, ensure_ascii=False)
