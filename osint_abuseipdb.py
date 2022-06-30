import requests
import dns.resolver
import re
import configparser

from file_util_abuseip import write_dict_json_html_abuseipdb

cfg = configparser.ConfigParser()
cfg.read('api_configuration/config.cfg')

KEY = cfg.get('AbuseIPDB', 'AbuseIPDB_KEY').replace("'", "")


def get_abuseipdb_url(url_or_ip: str, output_filename: str):
    target = url_or_ip
    filename = f'{output_filename}'
    out = f'output/{filename}_{target}.html'

    try:
        ans = dns.resolver.resolve(target, 'A')
        for data in ans:
            new_target = f'{data}'
    except dns.resolver.NXDOMAIN:
        print("[+] Checking in AbuseIPDB https://www.abuseipdb.com/")
        print("[+] Target was not found in AbuseIPDB!")
        with open(out, "r") as f:
            lines = f.readlines()
        with open(out, "w") as f:
            for line in lines:
                f.write(re.sub(r'REPLACE ME', f'{target} was NOT found in our database!', line))
        # print(f'[+] Writing to file {out}...')
        return

    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': new_target,
        # 'ipAddress': target,
        'maxAgeInDays': '365',
    }

    headers = {
        'Accept': 'application/json',
        'Key': KEY
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    print("[+] Checking in AbuseIPDB https://www.abuseipdb.com/")

    r = response.json()

    if response.status_code == 422:
        print(f'[+] AbuseIPDB: {url_or_ip} is NOT in AbuseIPDB!')
        return
    elif r['data']['totalReports'] == 0:
        print(f'[+] AbuseIPDB: {url_or_ip} was NOT found in AbuseIPDB database!')
    elif r['data']['totalReports'] > 0:
        print(f'[+] AbuseIPDB: {url_or_ip} was found in AbuseIPDB database!')

    write_dict_json_html_abuseipdb(target=url_or_ip, dict_obj=r, filename=f'{output_filename}')


def get_abuseipdb_ip(url_or_ip: str, output_filename: str):

    # Check if AbuseIPDB Website is reachable
    try:
        get = requests.get("https://api.abuseipdb.com")
        if not get.status_code == 200:
            print("[+] AbuseIPDB website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] AbuseIPDB website is not reachable!")
        return e

    target = url_or_ip

    # API for AbuseIPDB Search
    url = 'https://api.abuseipdb.com/api/v2/check'
    # API for AbuseIPDB Reports
    url_report = 'https://api.abuseipdb.com/api/v2/reports'

    querystring = {
       'ipAddress': target,
       'maxAgeInDays': '365',
    }

    headers = {
         'Accept': 'application/json',
         'Key': KEY
    }

    response_report = requests.request(method='GET', url=url_report, headers=headers, params=querystring)
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    print("[+] Checking in AbuseIPDB https://www.abuseipdb.com/")

    if response.status_code == 429:
        print("[+] Exceeded quota. Skipping.")
        return

    if response.status_code == 401:
        print("[+] API Key is either missing, incorrect, or revoked.")
        return

    r = response.json()
    r_report = response_report.json()

    if response.status_code == 422:
        print(f'[+] AbusedIPDB: {url_or_ip} is NOT in AbuseIPDB!')
        return
    elif r['data']['totalReports'] == 0:
        print(f'[+] AbuseIPDB: {url_or_ip} was NOT found in AbuseIPDB database!')
    elif r['data']['totalReports'] > 0:
        print(f'[+] AbuseIPDB: {url_or_ip} was found in AbuseIPDB database!')

    write_dict_json_html_abuseipdb(target=url_or_ip, dict_obj=r, dict_obj1=r_report, filename=f'{output_filename}')
