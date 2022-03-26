import requests

from scraper import Scraper
from typing import List


class NewsScraper(Scraper):

    def __init__(self, language, dest_country, country):
        super().__init__('countryNews', language, dest_country, country)

    def get_items(self) -> List[dict]:
        payload = {
            'content_type':
            self._content_type,
            'fields.locale':
            (f'{self._dest_country} > {self._country} > {self._language}'
             f'&{self._dest_country} > {self._language}'),
            'fields.permanent':
            'true'
        }

        r = requests.get(self.url, params=payload, headers=self.headers)
        return r.json()['items']

    def get_data(self) -> List[dict]:
        items = self.get_items()
        fields = [i['fields'] for i in items]
        intros = [
            f['intro']['content'][0]['content'][0]['value'] for f in fields
        ]
        dates = [f['date'] for f in fields]
        urls = [
            'https://visa.vfsglobal.com/blr/ru/pol/news/' + f['slug']
            for f in fields
        ]

        contents_list = [f['body']['content'] for f in fields]
        paragraphs = self.extract_paragraphs(contents_list)

        news_data = [{
            "date": d,
            "intro": i,
            "paragraph": p
        } for d, i, p, u in zip(dates, intros, paragraphs, urls)]

        return news_data

    @staticmethod
    def extract_paragraphs(contents_list: List[dict]) -> List[str]:
        paragraphs = []
        for contents in contents_list:
            paragraph = ''
            for content in contents:
                for c in content['content']:
                    if 'value' in c.keys():
                        paragraph += (c['value']).strip() + '\n'
                        paragraph += '\n'
                        paragraphs.append(paragraph)
        return paragraphs
