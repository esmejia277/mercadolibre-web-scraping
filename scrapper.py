from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def fetch_data(url: str, number_of_pages: int) -> list:

    products = []
    product_item = {}
    page_counter = 51
    url_copy = url[::]
    for page_number in range(1, number_of_pages + 1):
        try:
            if page_number != 1:
                url = url_copy + f"_Desde_{page_counter}"
                page_counter += 50

            page = urlopen(url)

        except Exception as error:
            print("Error: ", str(error), "URL: ", url, "\n" )

        if page.status != 200:
            break

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")

        li_tag = soup.find_all("li", attrs={"class": "ui-search-layout__item"})

        for product in li_tag:
            img = product.img
            link = product.a
            if img:
                product_item["description"] = img["alt"]
                product_item["img_url"] = img["data-src"]
            if link:
                product_item["link"] = link["href"]
            

            prices = product.find_all("span", attrs={"class": "price-tag-fraction"})

            if len(prices) == 1 or len(prices) == 2:
                product_item["price_today"] = float(prices[0].text.replace(".", ""))
            elif len(prices) == 3:
                product_item["price_before"] = float(prices[0].text.replace(".", ""))
                product_item["price_today"] = float(prices[1].text.replace(".", ""))
            product_item["page_number"] = page_number
            products.append(product_item)
            product_item = {}
        
    return products


if __name__ == "__main__":
    
    products = fetch_data(
        url = "https://computacion.mercadolibre.com.co/monitores/monitor-144hz",
        number_of_pages = 10
    )
    df_data = pd.DataFrame(data = products)
    df_data.to_excel("./products-monitors.xlsx")
    print(df_data)

            