# mercadolibre.com scraping

Web scraping, fetch data from mercadolibre

1. Clone this project

    `git clone git@github.com:esmejia277/WebScraping.git`

3. Create a virtualenv

   `python3 -m venv env`

4. Activate your virtual environment

   `source env/bin/activate`

5. Install dependencies

   `pip install -r requirements.txt`

6. Modify `number_of_pages` & `search` parameters in `main.py` depending on what you want to get from mercadolibre.com
   
   `example:`
   `number_of_pages = 3`
   `search = "teclado mecanico logitech"`

7. Execute the script
   
   `python main.py`

8. Check the output file with data