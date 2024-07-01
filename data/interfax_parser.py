import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

class SparkParser:
    def __init__(self, inn_file: str):
        self.dct = {}
        self.inns = self._load_inns(inn_file)

    def _load_inns(self, inn_file: str) -> list:
        df = pd.read_csv(inn_file)
        return df['ИНН'].astype('string').str[:-2].unique().tolist()

    def parse(self):
        for inn in self.inns:
            try:
                if 'ИНН' not in self.dct:
                    self.dct['ИНН'] = []
                self.dct['ИНН'].append(int(inn))
                self._parse_inn(inn)
            except Exception as e:
                print(f"Error processing INN {inn}: {e}")
        return pd.DataFrame(self.dct)

    def _parse_inn(self, inn: str):
        url = f'https://spark-interfax.ru/search?Query={inn}'
        page = requests.get(url)
        html = BeautifulSoup(page.text, "html.parser")
        company_link = 'https://spark-interfax.ru' + html.find('li', class_="search-result-list__item").find('a')['href']
        page = requests.get(company_link)
        html = BeautifulSoup(page.text, "html.parser")
        tables = html.find_all('div', class_='company-sidebar-section')

        labels = [
            ['судебные дела', 'в качестве истца', 'в качестве ответчика'],
            ['текущие производства', 'завершенные производства'],
            ['совладельцы']
        ]

        for table, label in zip(tables, labels):
            cells = table.find_all('a', class_="js-popup-open")
            cells = [cell for cell in cells if not cell.find(class_="js-replace-ruble")]
            for cell, name in zip(cells, label):
                num = cell.text
                if name not in self.dct:
                    self.dct[name] = []
                self.dct[name].append(int(num))

        div_element = html.find('div', class_='company-description__text').text.strip()
        match = re.search(r'(\d+)\s+тендер', div_element)
        number = int(match.group(1)) if match else 0

        if 'число тендеров' not in self.dct:
            self.dct['число тендеров'] = []
        self.dct['число тендеров'].append(number)

if __name__ == "__main__":
    parser = SparkParser('na_ratings.csv')
    df = parser.parse()
    df.to_csv('parsed_spark_data.csv', index=False)
