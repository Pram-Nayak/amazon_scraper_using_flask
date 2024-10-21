from flask import Flask, render_template, request
from scraper.scrapy import AmazonScraper

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['query']
        URL = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}"
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

        scraper = AmazonScraper(URL, HEADERS)
        content = scraper.get_webpage_content()
        product_urls = scraper.extract_product_links(content)

        all_product_data = []
        for product_url in product_urls:
            product_data = scraper.get_product_details(product_url)
            if product_data:
                all_product_data.append(product_data)

        return render_template('results.html', products=all_product_data)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
