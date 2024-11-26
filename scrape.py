import requests
from bs4 import BeautifulSoup

def fetch_msn_data(stock):
    url = f"https://www.msn.com/en-gb/money/stockdetails/{stock}-us-stock/fi-a1plh7?id=a1plh7"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        fetched_dev = soup.find_all('div', class_='factsRow-DS-EntryPoint1-1')

        keys = ["previous_close","avg_volume","market_cap","shares_outstanding","eps","pe","fwd_divident","ex_divident_date"]
        # Dictionary to store the key-value pairs
        result_dict = {}
        result_dict["current_price"] = soup.find('div', class_='mainPrice color_green-DS-EntryPoint1-1').text.strip()

        for i, container in enumerate(fetched_dev):
            # Extract review details and remove any unwanted characters
            value = container.find('div', class_='factsRowValue-DS-EntryPoint1-1').text.strip().replace("\u200e", "")
            
            # Map each cleaned value to a corresponding key
            if i < len(keys):
                result_dict[keys[i]] = value
            else:
                print("Warning: More values than keys provided!")

        return result_dict
    except Exception as e:
        print(f"Exception occurred: {e}")    

def fetch_zack_data(stock):
    url = f"https://www.zacks.com/stock/quote/{stock}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        fetched_dev = soup.find('div', class_='zr_rankbox composite_group')
        head_data = fetched_dev.find("p",class_="rank_view")
        main_data = head_data.find_all("span",class_="composite_val")

        keys = ["value","growth","momentum","vgm"]
        # Dictionary to store the key-value pairs
        result_dict = {}
        result_dict['insdustry'] = soup.find("a",class_="sector").text.replace("Industry:","").strip()

        for i, container in enumerate(main_data):
            # Extract review details and remove any unwanted characters
            value = container.text.strip()
            
            # Map each cleaned value to a corresponding key
            if i < len(keys):
                result_dict[keys[i]] = value
            else:
                print("Warning: More values than keys provided!")

        return result_dict
    except Exception as e:
        print(f"Exception occurred: {e}")    

def fetch_zack_data2(stock):
    url = f"https://www.zacks.com/stock/research/{stock}/price-target-stock-forecast"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        avg_price_target = soup.find_all('th', class_='align_center')[-1]
        lst_data = soup.find_all('td', class_='align_center')
        lst_data.append(avg_price_target)

        keys = ["highest_price_target","lowest_price_target","upside_to_avg_price_target","avg_price_target"]
        # Dictionary to store the key-value pairs
        result_dict = {}

        for i, container in enumerate(lst_data):
            # Extract review details and remove any unwanted characters
            value = container.text.replace("\n11.25%","").strip()
            
            # Map each cleaned value to a corresponding key
            if i < len(keys):
                result_dict[keys[i]] = value
            else:
                print("Warning: More values than keys provided!")

        return result_dict
    except Exception as e:
        print(f"Exception occurred: {e}")    

# Usage
def main(stock_name):
    if stock_name:
        result  = fetch_msn_data(stock_name)
        result2 = fetch_zack_data(stock_name)
        result3 = fetch_zack_data2(stock_name)
        result.update(result2)
        result.update(result3)
        return result
    return None    