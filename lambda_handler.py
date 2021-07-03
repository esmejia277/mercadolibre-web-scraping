import json
from urllib.request import urlopen
from bs4 import BeautifulSoup


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


def lambda_handler(event, context):
    
    # check http method here. POST or GET

    url = event.get('url')
    number_of_pages = event.get('number_of_pages')
    
    if not url or not number_of_pages:
        return {
            'statusCode': 400,
            'body': json.dumps({
                    'msg': {
                        'url': 'Please enter an mercadolibre url. (Search the product in the webpage and copy and paste the url). Example: https://listado.mercadolibre.com.co/mouse#D[A:mouse]',
                        'number_of_pages': 'Please enter how many pages do you want to fetch'
                    }
                })
        }
    


    try:
        # fetch data from mercadolibre
        print('Fetching ...')        
        products = fetch_data(
            url = url,
            number_of_pages = 1
        )
    except Exception as error:
        print('Error: ', error)
        return json.dumps({
            'msg': 'An error occurred, please verify your URL'
        })

    

    if not products:
        return {
            'statusCode': 404,
            'body': json.dumps({
                    'msg': 'No data'
                })
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "response": products
        })
    }


        