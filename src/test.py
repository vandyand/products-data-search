import requests
from bs4 import BeautifulSoup
import unittest
import sys

# Function to scrape inventory
def scrape_inventory(url):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15' }
    print('Making request to:', url)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print('Request sent. Waiting for response...')
        if response.status_code != 200:
            print('Failed to retrieve the webpage', file=sys.stderr)
            return None
        print('Received response from the server')
    except requests.exceptions.RequestException as e:
        print('An error occurred:', e, file=sys.stderr)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    items = []
    
    for item in soup.find_all('div', class_='item-class'):
        product_name = item.find('a', class_='product-name-class').text.strip()
        price = item.find('span', class_='price-class').text.strip()
        item_url = item.find('a', class_='product-name-class')['href']
        condition = item.find('span', class_='condition-class').text.strip() 
        
        items.append({
            'name': product_name,
            'price': price,
            'url': item_url,
            'condition': condition
        })
    
    print('Total items scraped:', len(items))
    return items

# Define the logging mechanism to use a file in the tests directory
log_file_path = 'tests/test_log.txt'

class TestScraping(unittest.TestCase):
    def test_scrape_inventory(self):
        with open(log_file_path, 'a') as log_file:
            # Redirect stdout and stderr to the log file
            sys.stdout = log_file
            sys.stderr = log_file
            print('Running test for inventory scraping...')
            url = 'https://www.liquidation.com/'
            inventory = scrape_inventory(url)
            print('Inventory scraped:', inventory)
            self.assertIsNotNone(inventory, 'Scraping should return a list of items')

if __name__ == '__main__':
    # Open a file to write the test results
    with open(log_file_path, 'a') as f:
        # Redirect stdout to the file
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)