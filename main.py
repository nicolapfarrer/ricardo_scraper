import requests,json,random,os,yaml,time
from dotenv import load_dotenv
from bot import send_message

#load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config', '.env'))
proxy_list_url = os.getenv("PROXY_LIST_URL")


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
    return None

def search_all_configs():
    search_configs = load_search_config()
    results = {}
    for key, config in search_configs.items():
        print(f"Searching for {key} with config: {config}")
        data = get_data(config)
        results[key] = data
    return results

#send results
def send_results(results):
    base_url = "https://www.ricardo.ch/de/a/"
    for key, data in results.items():
        send_message(f"Results for {key}:")
        for item in data[:5]:
            message = f"<a href='{base_url}{item['id']}'>{item['title']}</a>"
            send_message(message)

if __name__ == '__main__':
    all_results = search_all_configs()
    print(all_results)