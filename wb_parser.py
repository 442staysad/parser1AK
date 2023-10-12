import json
from datetime import date
from os import path
import time
import requests
from cards_extender import Cards_Extender
from excelService import ExcelService

class WildBerriesParser:

    def __init__(self, category):
        self.category = category
        self.headers = {'Accept': "*/*",
                        'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"}
        self.product_cards = []

    def download_current_catalogue(self) -> str:
        # Функция для загрузки текущего каталога товаров
        local_catalogue_path = path.join(self.directory, 'wb_catalogue.json')
        if (not path.exists(local_catalogue_path)
                or date.fromtimestamp(int(path.getmtime(local_catalogue_path)))
                > self.run_date):
            url = ('https://static-basket-01.wb.ru/vol0/data/'
                   'main-menu-ru-ru-v2.json')
            response = requests.get(url, headers=self.headers).json()
            with open(local_catalogue_path, 'w', encoding='UTF-8') as my_file:
                json.dump(response, my_file, indent=2, ensure_ascii=False)
        return local_catalogue_path

    def traverse_json(self, parent_category: list, flattened_catalogue: list):
        # Функция для обхода JSON-структуры каталога
        for category in parent_category:
            try:
                flattened_catalogue.append({
                    'name': category['name'],
                    'url': category['url'],
                    'shard': category['shard'],
                    'query': category['query']
                })
            except KeyError:
                continue
            if 'childs' in category:
                self.traverse_json(category['childs'], flattened_catalogue)

    def process_catalogue(self, local_catalogue_path: str) -> list:
        # Функция для обработки сохраненного каталога товаров
        catalogue = []
        with open(local_catalogue_path, 'r', encoding='utf-8') as my_file:
            self.traverse_json(json.load(my_file), catalogue)
        return catalogue

    def extract_category_data(self, catalogue: list, user_input: str) -> tuple:
        # Функция для извлечения данных о категории из каталога
        for category in catalogue:
            if (user_input.split("https://www.wildberries.ru")[-1]
                    == category['url'] or user_input == category['name']):
                return category['name'], category['shard'], category['query']

    def get_products_on_page(self,page_data: dict) -> list:
        # Функция для извлечения данных о товарах с одной страницы
        products_on_page = []
        for item in page_data['data']['products']:
            url=f"https://www.wildberries.ru/catalog/"f"{item['id']}/detail.aspx",
            products_on_page.append({
                'Ссылка': url,
                'Артикул': item['id'],
                'Наименование': item['name'],
                'Бренд': item['brand'],
                'Цена': int(item['priceU'] / 100),
                'Цена со скидкой': int(item['salePriceU'] / 100),
                })
        return products_on_page

    def add_data_from_page(self, url: str):
        # Функция для добавления данных о товарах с одной страницы
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            try:
                response_json = response.json()
                if isinstance(response_json, dict) and 'data' in response_json:
                    page_data = self.get_products_on_page(response_json)
                    if len(page_data) > 0:
                        self.product_cards.extend(page_data)
                        return True
                else:
                    print(f"Invalid response format: {response_json}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON response: {e}")
        elif response.status_code == 429:
            time.sleep(2)  # Подождать 2 секунды перед повторной попыткой
            return self.add_data_from_page(url)
        else:
            print(f"Request to {url} failed with status code {response.status_code}")
        return False

    def get_all_products_in_category(self, category_data: tuple):
        # Функция для загрузки всех товаров в указанной категории
        for page in range(1, 101):
            url = (f"https://catalog.wb.ru/catalog/{category_data[1]}/"
                    f"catalog?appType=1&curr=rub"
                   f"&dest=-1075831,-77677,-398551,12358499&page={page}"
                   f"&reg=0&sort=popular&spp=0&{category_data[2]}")
            if category_data[2] == "cat=128636":
                url += "&xsubject=5819"
                if page == 16:
                    break
            elif category_data[2] == "cat=128697":
                url += "&xsubject=4129"
                if page == 10:
                    break
            elif category_data[2] == "cat=128306":
                url += "&xsubject=2196"
                if page == 26:
                    break
            elif category_data[2] == "subject=3906":
                if page == 33:
                    break
            elif category_data[2] == "cat=59132":
                url += "&xsubject=792"
                if page == 59:
                    break
            try:
                self.add_data_from_page(url)
            except:
                break

    def run_parser(self):
        # Функция для запуска парсера
        local_catalogue_path = self.download_current_catalogue()
        processed_catalogue = self.process_catalogue(local_catalogue_path)
        category_data = self.extract_category_data(processed_catalogue,
                                                    self.category)
        
        self.get_all_products_in_category(category_data)
        cards_ext=Cards_Extender(self.product_cards)
        excelserv=ExcelService(self.category[0],self.category[2],cards_ext.extract_cards())
        excelserv.save_data_to_excel()

"""
if __name__ == '__main__':
    app = WildBerriesParser()
    app.run_parser()
"""