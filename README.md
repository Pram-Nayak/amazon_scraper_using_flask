# Amazon Laptop Scraper

This project is a web scraper designed to fetch laptop details from Amazon India and display them on a frontend using Flask. It allows users to search for specific laptops by entering keywords, then scrapes relevant data and displays it in an easy-to-view format.

## Project Structure
The project consists of two main parts:
1. **Scraper**: Python script using `requests` and `BeautifulSoup` to scrape product information from Amazon India.
2. **Frontend**: A Flask web application that accepts user input, performs the search, and displays results in a styled HTML format.

## Features
- **Web Scraper**: Collects laptop details such as:
  - Title, Brand, and Description
  - MRP, Selling Price, and Discount
  - Item Weight and ASIN
  - Category and Estimated Delivery
  - Image URL
- **Frontend**: Provides a search bar for users to enter specific laptop keywords. Displays the scraped results in a structured format.

## Getting Started

### Prerequisites
- **Python 3.x**
- **Flask**: Install via `pip install flask`
- **Requests** and **BeautifulSoup**: Install via `pip install requests beautifulsoup4`


