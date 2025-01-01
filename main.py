import requests,json,random,yaml

#load config
def load_config():


def is_proxy_working(proxy):
    test_url = "https://www.google.com"
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except:
        return False
    return False


def get_random_proxy():
    gh_list= "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/https.txt"
    done=False
    try:
        response = requests.get(gh_list)
        lines = response.text.splitlines()
        proxys = [line.strip() for line in lines]
    except:
        return None
    while not done:
            proxy= random.choice(proxys)
            print(f"Tesing: {proxy}")
            done = is_proxy_working(proxy)
    return proxy

def get_data(criteria):
    done=False
    while not done:
        p= get_random_proxy()
        proxies = {
            "http": p,
            "https": p,
        }
        print(f"Using proxy: {p}")
        try:
            response = requests.get(f"https://www.ricardo.ch/api/mfa/search/?sort=newest&categorySeoSlug=grafikkarte-39204", proxies=proxies)#temporary url
            print(response.status_code)
            data = response.json()
            return data
        except:
            pass

print(get_data('grafikkarte-39204'))
