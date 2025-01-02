import requests,json,random,os,yaml,datetime,asyncio
from dotenv import load_dotenv
from bot import send_message

#load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config', '.env'))
proxy_list_url = os.getenv("PROXY_LIST_URL")

#load search config
def load_search_config():
    with open(os.path.join(os.path.dirname(__file__), 'config', 'search.yaml')) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

#proxy
def is_proxy_working(proxy):
    test_url = "https://ricardo.ch"
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return True
    except:
        return False
    return False

def get_random_proxy():
    done=False
    try:
        response = requests.get(proxy_list_url)
        lines = response.text.splitlines()
        proxys = [line.strip() for line in lines]
    except:
        return None
    while not done:
            if len(proxys)==0:
                return None
            proxy= random.choice(proxys)
            proxys.remove(proxy)
            print(f"Tesing: {proxy}")
            done = is_proxy_working(proxy)
    return proxy

#request data
def get_data(criteria):
    done = False
    while not done:
        p = get_random_proxy()
        proxies = {
            "http": p,
            "https": p,
        }
        print(f"Using proxy: {p}")
        try:
            base_url = "https://www.ricardo.ch/api/mfa/search/"
            query_string = "&".join([f"{key}={value}" for key, value in criteria.items()])
            url = f"{base_url}?{query_string}"
            response = requests.get(url, proxies=proxies)
            print(response.status_code)
            data = response.json()
            return data.get('articles', [])
        except:
            pass
        if p is None:
            done = True
    return None

def search_all_configs(previous_results):
    search_configs = load_search_config()
    new_results = {}
    for key, config in search_configs.items():
        print(f"Searching for {key} with config: {config}")
        data = get_data(config)
        if key in previous_results:
            new_data = [item for item in data if item['id'] not in previous_results[key]]
        else:
            new_data = data
        new_results[key] = new_data
    return new_results

#update previous results
def update_previous_results(previous_results):
    if previous_results is None:
        return previous_results 
    updated_results = {}
    current_time = datetime.utcnow()
    for key, items in previous_results.items():
        updated_items = [item for item in items if datetime.strptime(item['endDate'], '%Y-%m-%dT%H:%M:%SZ') > current_time]
        if updated_items:
            updated_results[key] = updated_items
    return updated_results

#send results
async def send_results(results):
    asyncio.run(send_message("Results:",silent=False))
    base_url = "https://www.ricardo.ch/de/a/"
    for key, data in results.items():
        await send_message(f"Results for {key}:")
        try:
            for item in data[:5]:
                message = f"<a href='{base_url}{item['id']}'>{item['title']}</a>"
                await send_message(message)
        except:
            await send_message("No new results")

if __name__ == '__main__':
    previous_results = {}
    all_results = search_all_configs(previous_results)
    asyncio.run(send_results(all_results))
    all_results = search_all_configs(previous_results)
    asyncio.run(send_results(all_results))