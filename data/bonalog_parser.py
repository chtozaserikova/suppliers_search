import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO
import time

class NalogParser:
    def __init__(self, inn_file: str):
        self.driver = webdriver.Chrome()
        self.ac = ActionChains(self.driver)
        self.parser = etree.HTMLParser()
        self.wait = WebDriverWait(self.driver, 10)
        self.list_of_df = []
        self.inns = self._load_inns(inn_file)

    def _load_inns(self, inn_file: str) -> list:
        df = pd.read_csv(inn_file)
        return df['ИНН'].astype('string').str[:-2].unique().tolist()

    def parse(self):
        for inn in self.inns:
            try:
                url = f'https://bo.nalog.ru/search?query={inn}&page=1'
                self.driver.get(url)
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search")))
                self.ac.click().perform()
                tree = etree.parse(StringIO(self.driver.page_source), self.parser)
                orgs = tree.xpath('//*[@id="root"]/main/div/div/div[2]/div[2]/a')
                if orgs:
                    id_link = orgs[0].attrib['href']
                    org_id = "".join(filter(str.isdigit, id_link))
                    self._parse_org_page(inn, org_id)
            except Exception as e:
                print(f"Error processing INN {inn}: {e}")
        self.driver.close()
        return pd.concat(self.list_of_df, ignore_index=True)

    def _parse_org_page(self, inn: str, org_id: str):
        self.driver.get(f'https://bo.nalog.ru/organizations-card/{org_id}')
        time.sleep(5)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        dfs = soup.find_all('div', class_='tabulator-table')

        list_cols = ['ИНН']
        list_values = [inn]

        for row in dfs[2].find_all('div', class_='tabulator-row'):
            list_cols.append(row.find_all('div', class_='tabulator-cell')[0].text.strip() + '2023')
            list_cols.append(row.find_all('div', class_='tabulator-cell')[0].text.strip() + '2022')
            list_values.append(row.find_all('div', class_='tabulator-cell')[2].text.strip())
            list_values.append(row.find_all('div', class_='tabulator-cell')[3].text.strip())

        list_cols.append('Баланс2023')
        list_cols.append('Баланс2022')
        list_values.append(dfs[0].find_all('div', class_='tabulator-row')[-1].find_all('div', class_='tabulator-cell')[2].text.strip())
        list_values.append(dfs[0].find_all('div', class_='tabulator-row')[-1].find_all('div', class_='tabulator-cell')[3].text.strip())

        data = {col: [val] for col, val in zip(list_cols, list_values)}
        self.list_of_df.append(pd.DataFrame(data))

if __name__ == "__main__":
    parser = NalogParser('na_ratings.csv')
    full_df = parser.parse()
    full_df.to_csv('parsed_nalog_data.csv', index=False)