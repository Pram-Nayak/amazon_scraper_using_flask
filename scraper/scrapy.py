import requests
from bs4 import BeautifulSoup
import json

class AmazonScraper:
    def __init__(self, url, headers):
        # Initialize the AmazonScraper with a given URL and headers
        self.url = url
        self.headers = headers

    def get_webpage_content(self):
        try:
            # Send an HTTP GET request to the specified URL with headers
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            # Return the content of the webpage
            return response.content
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

    def extract_product_links(self, content):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        # Find all links with a specific class attribute
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        # Extract product links from the anchor tags
        product_links = ["https://amazon.in" + link.get('href') for link in links]
        return product_links

    def get_product_details(self, product_url):
        try:
            # Send an HTTP GET request to the product URL with headers
            new_webpage = requests.get(product_url, headers=self.headers)
            new_webpage.raise_for_status()
            # Parse the HTML content of the product page using BeautifulSoup
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            
            # Extract product details such as title, features, image URL, brand, etc.
            title = new_soup.find("span", attrs={"id": 'productTitle'}).text.strip()
            features = new_soup.find("div", attrs={"id": 'feature-bullets'}).text.strip()
            image_url = new_soup.find("div", attrs={"class": "imgTagWrapper"}).img['src']
            brand = new_soup.select_one("tr.po-brand span.a-size-base.po-break-word")
            mrp = new_soup.select_one('span.a-price-whole')
            discount = new_soup.find('span', class_='a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage')
            sell_price = new_soup.select_one('.a-offscreen')

            # Extract weight from technical specifications table
            tech_spec_table = new_soup.find("table", {"id": "productDetails_techSpec_section_1"})
            item_weight = None
            if tech_spec_table:
                for row in tech_spec_table.find_all("tr"):
                    if "Item Weight" in row.text:
                        item_weight_element = row.find("td", class_="a-size-base")
                        item_weight = item_weight_element.text.strip() if item_weight_element else None
                        break

            # Extract ASIN from product details table
            product_details_table = new_soup.find("table", {"id": "productDetails_detailBullets_sections1"})
            asin_value = None
            if product_details_table:
                for row in product_details_table.find_all("tr"):
                    if "ASIN" in row.text:
                        asin_element = row.find("td", class_="a-size-base prodDetAttrValue")
                        asin_value = asin_element.text.strip() if asin_element else None
                        break

            # Extract the requested category
            category = new_soup.find("span", attrs={"class": 'a-list-item'}).text.strip()

            # Extract Estimated delivery information
            estimated_delivery = new_soup.find("div", attrs={"id": 'deliveryBlockContainer'}).text.strip()

            # Construct a dictionary containing product data
            product_data = {
                "name":  title,
                "title": title,
                "description": features,
                "image_url": image_url,
                "brand": brand.text.strip() if brand else None,
                "mrp": mrp.text.strip() if mrp else None,
                "discount": discount.text.strip() if discount else None,
                "selling_price": sell_price.text.strip() if sell_price else None,
                "item_weight": item_weight,
                "asin": asin_value,
                "Laptop Specification": features,
                "category": category,  # Add the category information to the product data
                "estimated_delivery": estimated_delivery  # Add Estimated delivery information
            }
            
            return product_data
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")
        except AttributeError as ae:
            print(f"Attribute Error: {ae}")

def main():
    # Define the URL and headers for the Amazon scraper
    URL = "https://www.amazon.in/s?k=laptop&crid=IIW1U6MQZY7X&sprefix=laptop%2Caps%2C209&ref=nb_sb_noss_1"
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

    # Create an instance of the AmazonScraper
    scraper = AmazonScraper(URL, HEADERS)

    # Get the content of the webpage
    content = scraper.get_webpage_content()
    # Extract product links from the webpage content
    product_urls = scraper.extract_product_links(content)

    # Store product data for all products in a list
    all_product_data = []

    # Iterate through each product URL and retrieve its details
    for product_url in product_urls:
        product_data = scraper.get_product_details(product_url)
        all_product_data.append(product_data)

    # # Save all product data to a JSON file
    # with open("amazon_product_data.json", "w") as json_file:
    #     json.dump(all_product_data, json_file, indent=2)
    #     print("Data saved to amazon_product_data.json")

if __name__ == "__main__":
    main()