import requests

from scraper import Scraper
from typing import List


class VacScraper(Scraper):

    def __init__(self, language, dest_country, country):
        super().__init__('countryLocation', language, dest_country, country)

    def get_items(self) -> List[dict]:
        payload = {
            'content_type': self._content_type,
            'fields.title[match]':
            f'{self._dest_country} > {self._country} > {self._language}',
            'order': 'fields.vacName',
            'limit': '200'
        }

        r = requests.get(self.url, params=payload, headers=self.headers)
        return r.json()['items']

    def get_data(self) -> List[dict]:
        items = self.get_items()
        fields = [i['fields'] for i in items]
        cities = [f['vacName'] for f in fields]
        opening_hours = [f['openingHoursObject'] for f in fields]
        vacaddresses = [
            f['address']['content'][0]['content'][0]['value'].strip('{ }')
            for f in fields
        ]
        addresses = self.get_addresses(vacaddresses)

        centers_data = [{
            "city": c,
            "opening_hours": oh,
            'address': a
        } for c, oh, a in zip(cities, opening_hours, addresses)]

        return centers_data

    def get_addresses(self, vacaddresses: List[str]) -> List[str]:
        payload = {
            'content_type':
            'resourceGroup',
            'fields.locale':
            (f'vfs&{self._language}&{self._dest_country}&{self._dest_country} '
             f'> {self._language}&{self._dest_country} > {self._country}'
             f'&{self._dest_country} > {self._country} > {self._language}'),
            'limit':
            500
        }

        r = requests.get(self.url, params=payload, headers=self.headers)
        resources = r.json()['items'][4]['fields']['resources']
        addresses = [resources[v] for v in vacaddresses]
        return addresses
