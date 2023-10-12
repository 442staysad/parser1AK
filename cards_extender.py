from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class Cards_Extender:

    def __init__(self,data):
        self.headers = {'Accept': "*/*",
                'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"}
        self.driver_path = 'chromedriver.exe'
        self.data=data
    
    
    def get_url_for_data(self, page_url):

        # Опция для работы в режиме headless
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)

        driver.get(page_url)
        
        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'photo-zoom__preview'))
        )
        src_attribute = img_element.get_attribute('src')
        
        parts = src_attribute.split("image")
        desired_url = parts[0]
        driver.quit()
        return desired_url    

    def get_card_data(self, card_url):
        # Функция для получения характеристик и продавца товара
        return requests.get(f'{card_url}/info/ru/card.json',headers=self.headers).json()["grouped_options"],requests.get(f'{card_url}/info/sellers.json',headers=self.headers).json()

    def extract_cards(self):
        # Функция для извлечения данных о товарах с одной страницы
        products = []
        
        for item in self.data:
            url=f"https://www.wildberries.ru/catalog/"f"{item['id']}/detail.aspx",
            
            page_url=self.get_url_for_data(url)

            item_data,item_seller=self.get_card_data(page_url)

            if self.category_name=="cat=128636":
                products.append({
                    'Ссылка': item['Ссылка'],
                    'Артикул': item['Артикул'],
                    'Наименование': item['Наименование'],
                    'Бренд': item['Бренд'],
                    'Цена': item['Цена'],
                    'Цена со скидкой': item['Цена со скидкой'],
                    'Продавец':item_seller['trademark'],
                    'Емкость':next((option["value"] for item in item_data for option in item["options"] if "Емкость"in option["name"]), None),
                    'Пусковой ток':next((option["value"] for item in item_data for option in item["options"] if "Пусковой"in option["name"]), None),
                    'Полярность':next((option["value"] for item in item_data for option in item["options"] if "Полярность"in option["name"]), None),
                    'Габариты':next((option["value"] for item in item_data for option in item["options"] if "Габариты"in option["name"]), None),
                    'Технология':next((option["value"] for item in item_data for option in item["options"] if "Технология"in option["name"]), None)
                })
            elif self.category_name=="cat=128306":
                products.append({
                    'Ссылка': item['Ссылка'],
                    'Артикул': item['Артикул'],
                    'Наименование': item['Наименование'],
                    'Бренд': item['Бренд'],
                    'Цена': item['Цена'],
                    'Цена со скидкой': item['Цена со скидкой'],
                    'Продавец':item.item_seller['trademark'],
                    'Емкость':next((option["value"] for item in item_data for option in item["options"] if "Емкость"in option["name"]), None),
                    'Напряжение':next((option["value"] for item in item_data for option in item["options"] if "Напряжение"in option["name"]), None),
                    'Полярность':next((option["value"] for item in item_data for option in item["options"] if "Полярность"in option["name"]), None),
                    'Клемм':next((option["value"] for item in item_data for option in item["options"] if "клемм"in option["name"]), None),
                })
            elif self.category_name=="cat=59132":
                products.append({
                    'Ссылка': item['Ссылка'],
                    'Артикул': item['Артикул'],
                    'Наименование': item['Наименование'],
                    'Бренд': item['Бренд'],
                    'Цена': item['Цена'],
                    'Цена со скидкой': item['Цена со скидкой'],
                    'Продавец':item.item_seller['trademark'],
                    'Артикул производителя':next((option["value"] for item in item_data for option in item["options"] if "Артикул"in option["name"]), None),
                    'Тип химии':next((option["value"] for item in item_data for option in item["options"] if "клемм"in option["name"]), None),
                    'Типоразмер':next((option["value"] for item in item_data for option in item["options"] if "клемм"in option["name"]), None),
                    'Ток':next((option["value"] for item in item_data for option in item["options"] if "ток"in option["name"]), None),
                })
            elif self.category_name=="cat=128697":
                products.append({
                    'Ссылка': item['Ссылка'],
                    'Артикул': item['Артикул'],
                    'Наименование': item['Наименование'],
                    'Бренд': item['Бренд'],
                    'Цена': item['Цена'],
                    'Цена со скидкой': item['Цена со скидкой'],
                    'Продавец':item.item_seller['trademark'],
                    'Емкость':next((option["value"] for item in item_data for option in item["options"] if "Емкость"in option["name"]), None),
                    'Напряжение':next((option["value"] for item in item_data for option in item["options"] if "Напряжение"in option["name"]), None),
                    'Технология':next((option["value"] for item in item_data for option in item["options"] if "Технология"in option["name"]), None),
                    'Ток':next((option["value"] for item in item_data for option in item["options"] if "ток"in option["name"]), None),
                })
            elif self.category_name=="subject=3906":
                products.append({
                    'Ссылка': item['Ссылка'],
                    'Артикул': item['Артикул'],
                    'Наименование': item['Наименование'],
                    'Бренд': item['Бренд'],
                    'Цена': item['Цена'],
                    'Цена со скидкой': item['Цена со скидкой'],
                    'Продавец':item.item_seller['trademark'],
                    'Артикул производителя':next((option["value"] for item in item_data for option in item["options"] if "Артикул"in option["name"]), None),
                    'Литраж':next((option["value"] for item in item_data for option in item["options"] if "Литр"in option["name"]), None),
                    'Вязкость':next((option["value"] for item in item_data for option in item["options"] if "Вязкость"in option["name"]), None),
                    'Тип':next((option["value"] for item in item_data for option in item["options"] if "Тип"in option["name"]), None),
                })
        
        return products