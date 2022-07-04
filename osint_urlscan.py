import json
import requests
import time
import configparser
from colorama import Fore, init
from file_util_urlscan import write_dict_json_html_urlscan

init(convert=True)
cfg = configparser.ConfigParser()
cfg.read('api_configuration/config.cfg')

KEY = cfg.get('URLScanIO', 'URLScanIO_KEY').replace("'", "")


def get_urlscan_ip_url(url_or_ip: str, output_filename: str):

    # Check if URLScanIO Website is reachable
    try:
        get = requests.get("https://urlscan.io")
        if not get.status_code == 200:
            print("[+] URLScanIO website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] URLScanIO website is not reachable!")
        return e

    headers = {'API-Key': KEY, 'Content-Type': 'application/json', 'resource': url_or_ip}

    data = {"url": url_or_ip, "visibility": "public"}
    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))

    print("[+] Checking in URLScanIO https://urlscan.io/")
    if response.status_code == 429:
        print("[+] Exceeded quota. Skipping.")
        return

    # parse json result from API
    json_response = response.json()

    status_response = json_response.get('status')

    # not in URLSCANIO
    if status_response == 400:
        print(f'[+] URLScanIO: {url_or_ip} is not in URLScanIO')
        # get_urlscan_ip_url_search(url_or_ip, output_filename)
        return

    if status_response == 401:
        print(f'[+] URLScanIO: API key supplied but not found in database.')
        return

    x = str(json_response)
    x = x.replace("'", '"')

    parsed = json.loads(x)
    uuid = parsed.get('api')
    print(f'[+] URLScanIO: Please wait ...')
    time.sleep(13)

    api_site = requests.get(f'{uuid}', headers=headers)
    api_response = api_site.json()

    if api_response.get("status"):
        api_status = api_response['status']
        if api_status:
            if api_status == 404:
                print(f'[+] URLScanIO: We could not find this page.')
                return

    verdict_info = api_response.get("verdicts")
    malicious_code = verdict_info.get("overall").get("malicious")
    if malicious_code:
        print('[+] urlscan.' + Fore.GREEN + 'io ' + Fore.WHITE + 'Verdict ' + Fore.RED + 'Malicious!!!' + Fore.WHITE)

    write_dict_json_html_urlscan(target=url_or_ip, dict_obj=api_response, filename=f'{output_filename}')


def get_urlscan_ip_url_search(url_or_ip: str, output_filename: str):

    # Check if URLScanIO Website is reachable
    try:
        get = requests.get("https://urlscan.io")
        if not get.status_code == 200:
            print("[+] URLScanIO website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] URLScanIO website is not reachable!")
        return e

    headers = {'API-Key': KEY, 'Content-Type': 'application/json', 'resource': url_or_ip}

    print(f'[+] URLScanIO: Try using Search API reference')

    if '://' in url_or_ip:
        url = url_or_ip.split("://")[1]
        params = (
           ('q', "domain:%s" % url),
        )
    else:
        params = (
            ('q', "domain:%s" % url_or_ip),
        )

    response = requests.get('https://urlscan.io/api/v1/search/', params=params)
    r = response.content.decode("utf-8")

    if response.status_code == 400:
        print(f'[+] URLScanIO: DNS Error - Could not resolve domain.')
        return

    parsed = json.loads(r)

    results = parsed.get("total")

    if results == 0:
        print(f'[+] URLScanIO: {url_or_ip} is not in URLScanIO')
        return

    res = parsed.get("results")
    task = res[0].get('task')
    uuid = task['uuid']
    print(f'[+] URLScanIO: Please wait ...')
    time.sleep(13)

    api_site = requests.get(f'https://urlscan.io/api/v1/result/{uuid}', headers=headers)
    api_response = api_site.json()
    verdict_info = api_response.get("verdicts")
    malicious_code = verdict_info.get("overall").get("malicious")

    if malicious_code:
        print('[+] urlscanIO Verdict: ' + Fore.RED + 'Malicious!!!' + Fore.WHITE)

    write_dict_json_html_urlscan(target=url_or_ip, dict_obj=api_response, filename=f'{output_filename}')


