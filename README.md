# WebScraping
 Web scraping, fetch data from mercadolibre
 
  1. Clone this project 
  2. Create a virtualenv
  3. Install dependencies with pip install -r requirements.txt
  
  Built with AWS API GATEWAY, LAMBDA FUNCTIONS, PYTHON

  Fetch data from mercadolibre.com, enter your mercadolibre url in URL parameter. Enter how many pages do you want to fetch in number_of_pages parameter

  ENDPOINTS AWS API Gateway: https://llb178ib7k.execute-api.us-east-2.amazonaws.com/dev/products
  METHOD: POST
  BODY REQUEST EXAMPLE: {
    "url" : "https://listado.mercadolibre.com.co/autos#D[A:autos]",
    "number_of_pages": 1
}