import requests,json,random,os,yaml,asyncio,logging
from dotenv import load_dotenv
from bot import send_message
from datetime import datetime
#logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

#load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
proxy_list_url = os.getenv("PROXY_LIST_URL")
logger.info("Loaded environment variables")

#load search config
def load_search_config():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'search.yaml')) as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except Exception as e:
        logger.error(f"Failed to load search config: {str(e)}")
        return {}

# Load previous results from file
def load_previous_results():
    if os.path.exists("previous_results.json"):
        try:
            with open("previous_results.json", 'r') as file:
                logger.info("Previous results loaded successfully")
                return json.load(file)
        except Exception as e:
            logger.error(f"Failed to load previous results: {str(e)}")
    return {}

# Save previous results to file
def save_previous_results(previous_results):
    try:
        with open("previous_results.json", 'w') as file:
            json.dump(previous_results, file)
        logger.info("Previous results saved successfully")
    except Exception as e:
        logger.error(f"Failed to save previous results: {str(e)}")

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
            with open('proxies.txt', 'a+') as file:
                file.seek(0)
                existing_proxies = file.read().splitlines()
                if proxy not in existing_proxies:
                    file.write(proxy + '\n')
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
        logger.info(f"Fetched {len(proxys)} proxies from source")
    except Exception as e:
        logger.error(f"Failed to fetch proxy list: {str(e)}")
        return None
    while not done:
            if len(proxys)==0:
                logger.warning("No working proxies found")
                return None
            proxy= random.choice(proxys)
            proxys.remove(proxy)
            logger.info(f"Testing proxy: {proxy}")
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
            logger.info(f"Received {len(data.get('articles', []))} results")
            return data.get('articles', [])
        except Exception as e:
            logger.error(f"Failed to get data: {str(e)}")
            pass
        if p is None:
            done = True
    logger.warning("Failed to get data")
    return None

def search_all_configs(previous_results):
    search_configs = load_search_config()
    new_results = {}
    for key, config in search_configs.items():
        logger.info(f"Searching for {key} with config: {config}")
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
    current_time = datetime.now()
    for key, items in previous_results.items():
        updated_items = [item for item in items if datetime.strptime(item['endDate'], '%Y-%m-%dT%H:%M:%SZ') > current_time]
        if updated_items:
            updated_results[key] = updated_items
    logger.info(f"Updated previous results to {len(updated_results)} items")
    return updated_results

#send results
async def send_results(results):
    logger.info(f"Sending results")
    await send_message("Results:",silent=False)
    base_url = "https://www.ricardo.ch/de/a/"
    for key, data in results.items():
        await send_message(f"Results for {key}:")
        try:
            for item in data[:5]:
                message = f"<a href='{base_url}{item['id']}'>{item['title']}</a>"
                await send_message(message)
                previous_results[key]=[]
                previous_results[key].append(item)
        except:
            await send_message("No new results")

if __name__ == '__main__':
    previous_results = load_previous_results()
    previous_results = update_previous_results(previous_results)
    asyncio.run(send_results(search_all_configs(previous_results)))
    save_previous_results(previous_results)