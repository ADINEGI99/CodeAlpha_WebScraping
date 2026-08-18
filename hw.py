import csv
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_all_books(base_url, file_name, total_pages=50):
    print("Thank you for sharing the URL and file name!\n Starting the scraper...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/151.0.0.0 Safari/537.36'
    }

   
    with open(file_name, 'w', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(['Title', 'Price', 'Stock', 'Rating', 'Link'])

        
        for page_num in range(1, total_pages + 1):
            
            
            page_url = f"{base_url}catalogue/page-{page_num}.html"
            print(f"Scraping Page {page_num} of {total_pages}...")
            
            response = requests.get(page_url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                book_containers = soup.find_all('article', class_='product_pod')

                
                for book in book_containers:
                    
                    title_tag = book.find('h3')
                    if title_tag and title_tag.find('a'):
                        book_name = title_tag.find('a').get('title', 'NA')
                        link = title_tag.find('a').get('href', 'NA')
                        full_link = f"{base_url}catalogue/{link}" if link != 'NA' else 'NA'
                    else:
                        book_name, full_link = 'NA', 'NA'

                    # Price
                    price_tag = book.find('p', class_='price_color')
                    price = price_tag.text.strip() if price_tag else 'NA'

                    # Stock Status
                    stock_tag = book.find('p', class_='instock availability')
                    stock = stock_tag.text.strip() if stock_tag else 'NA'

                    # Star Rating
                    rating_tag = book.find('p', class_='star-rating')
                    if rating_tag and len(rating_tag.get('class', [])) > 1:
                        rating = rating_tag['class'][1]
                    else:
                        rating = 'NA'

                    
                    writer.writerow([book_name, price, stock, rating, full_link])
                
                
                delay = random.randint(1, 3)
                time.sleep(delay)
                
            else:
                print(f"Failed to connect to page {page_num}. Status code: {response.status_code}")
                break
    print(f"\nScraping complete! All books saved to '{file_name}' successfully.")


if __name__ == '__main__':
    
    
    url_input = input("Please enter url! : ")
    file_input = input("Please give file name! (e.g. all_books.csv) : ")
    
    
    scrape_all_books(url_input, file_input, total_pages=50)