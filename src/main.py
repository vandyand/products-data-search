import requests
from bs4 import BeautifulSoup

# Function to scrape inventory
def scrape_inventory(url):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15' }
    print('Making request to:', url)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print('Request sent. Waiting for response...')
        if response.status_code != 200:
            print('Failed to retrieve the webpage')
            return None
        print('Received response from the server')
    except requests.exceptions.RequestException as e:
        print('An error occurred:', e)
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
