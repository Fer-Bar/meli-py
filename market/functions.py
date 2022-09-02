import requests
from typing import Any


def get_product_id(nickname: str, BASE_URL: str ='https://api.mercadolibre.com', 
                   site_id: str = 'MLA', offset: int = 0, limit: int = 50)-> list[str]:
    """Get the product ID from the vendor nickname
    
    Parameters:
    nickname (str): The vendor nickname
    site_id (str): The site ID name
    BASE_URL (str): The base URL
    offset (int): The offset to retrieve the results, by default is 0 
                  FYC the limit value by default is 50   
    Returns:
    list: Returns fifty product ID's
    """
    
    vendor = requests.get(f'{BASE_URL}/sites/{site_id}/search?nickname={nickname}&offset={offset}&limit={limit}').json()
    return [result['id'] for result in vendor['results']]

def product_details(product_id: str, BASE_URL: str ='https://api.mercadolibre.com') -> list[dict[str, Any]]:
    """Get the product details from product ID
    
    Parameters:
    product_id (str): The product_id to search
    BASE_URL (str): The base URL
    
    Returns:
    dict: Returns a dict with the details of the product
    """
    item_list = []
    percent = lambda part, whole: 100 * float(part) / float(whole)
    item = requests.get(f'{BASE_URL}/items/{product_id}')
    if item.status_code == 200:
        item = item.json()
        original_price = item.get('original_price') if item.get('original_price') is not None else item.get('base_price')
        discount_ammount = abs(original_price - item.get('base_price')) if original_price != 0 else 0
        discount_percent = percent(discount_ammount, original_price)
        item_list.append({
                'seller_id': item.get('seller_id'),
                'title': item.get('title'),
                'brand': item['attributes'][2]['values'][0]['name'],
                'base_price': item.get('base_price'), #precio con descuento, menos precio
                'original_price': original_price, # precio original sin descuento. aveces en null
                'discount_ammount': discount_ammount,
                'discount_percent': round(discount_percent, 2),
                'brand_discount_allow': 0 # 0 by default for every product
            })
        return item_list
    return None

def update_product_data(obj, item_details):
    obj.base_price = item_details[0]['base_price']
    obj.discount_ammount = item_details[0]['discount_ammount']
    obj.discount_percent = item_details[0]['discount_percent']
    if not obj.raise_alert(): 
        obj.fault_date = None
    obj.save()
    print('Data Updated Success')