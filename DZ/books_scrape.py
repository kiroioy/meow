from http.client import responses
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

all_books_data = []
base_url = 'http://books.toscrape.com/catalogue/page-'
max_page = 5
for page_num in range(1, max_page+1):
    current_url = f"{base_url}{page_num}.html"
    print(f"\nобрабатываем страницу №{page_num} по адресу: {current_url}")
    try:
        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"ошибка при запросе страницы {page_num}. код: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        book_containers = soup.find_all('article', class_='product_pod')
        if not book_containers:
            print("не найдено ни одного блока книги на этой странице")
            break
        for book in book_containers:
        # название
            title = book.find('h3').find('a')['title']
        # цена
            price = book.find('p', class_='price_color').text
        # рейтинг
            rating_element = book.find('p', class_='star-rating')
            rating = rating_element['class'][1]
            all_books_data.append({
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Page_Scraped': page_num
        })

    except requests.exceptions.RequestException as e:(
        print(f"произошла ошибка подключения для страницы {page_num}: {e}"))
    time.sleep(1)

print("\nпарсинг завершен")
print(f"всего собрано записей: {len(all_books_data)}")

'''формирование датасета'''
books_df = pd.DataFrame(all_books_data)
print("\nпервые 5 строк сформированного датасета:")
print(books_df.head())
csv_filename = 'books_data.csv'
books_df.to_csv(csv_filename, index=False, encoding='utf-8')
print(f"\nдатасет успешно сохранен в файл: {csv_filename}")