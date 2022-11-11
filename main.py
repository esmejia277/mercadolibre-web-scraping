from typing import List, AnyStr
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime


def replace_blank_spaces_in_search_word(search: str) -> str:
    return search.replace(" ", "-")

def generate_url(url: str, search: str, number_of_pages: int) -> List[str]:
    urls = []
    page_counter = 51
    url = url + search
    url_copy = url[::]
    for page_number in range(1, number_of_pages + 1):
        if page_number == 1:
            urls.append(url)
            continue
        url = url_copy + f"_Desde_{page_counter}_NoIndex_True"
        urls.append(url)
        page_counter += 50
    return urls


def fetch_data(url: str) -> list:
    http_response = []
    for url in urls:
        try:
            page = urlopen(url)
            http_response.append(page)
        except:
            pass
    return http_response


def save_file(parsed_products: List, search: str, file_extension: AnyStr):
    if file_extension == ".csv":
        pd.DataFrame(parsed_products).to_csv(f"./{search}-{datetime.today().strftime('%d-%m-%Y-%H-%M-%S')}.csv")
    if file_extension == ".xlsx":
        pd.DataFrame(parsed_products).to_excel(f"./{search}-{datetime.today().strftime('%d-%m-%Y-%H-%M-%S')}.xlsx")


def parse_products_page(pages):
    parsed_products = []
    product_item = {}

    for index, page in enumerate(pages, 1):
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        li_tag = soup.find_all("li", attrs={"class": "ui-search-layout__item"})
        for parsed_page in li_tag:
            img = parsed_page.img
            link = parsed_page.a
            if img:
                product_item["description"] = img["alt"]
                product_item["img_url"] = img["data-src"]
            if link:
                product_item["link"] = link["href"]
            
            prices = parsed_page.find_all("span", attrs={"class": "price-tag-fraction"})
            if len(prices) == 1 or len(prices) == 2:
                product_item["price_today"] = float(prices[0].text.replace(".", ""))
            elif len(prices) == 3:
                product_item["price_before"] = float(prices[0].text.replace(".", ""))
                product_item["price_today"] = float(prices[1].text.replace(".", ""))
            product_item["page_number"] = index
            parsed_products.append(product_item)
            product_item = {}
    return parsed_products


if __name__ == "__main__":
    URL = "https://listado.mercadolibre.com.co/"
    
    number_of_pages = 3
    search = "macbook pro"

    search = replace_blank_spaces_in_search_word(search=search)
    urls = generate_url(url=URL, search=search, number_of_pages=number_of_pages)
    pages = fetch_data(url=urls)
    parsed_products = parse_products_page(pages=pages)
    save_file(parsed_products=parsed_products, search=search, file_extension=".csv")