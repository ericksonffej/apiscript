import requests
import configparser
from colorama import Fore, init
from file_util_greynoise import write_dict_json_html_greynoise

init(convert=True)
cfg = configparser.ConfigParser()
cfg.read('api_configuration/config.cfg')

KEY = cfg.get('GreyNoise', 'GreyNoise_KEY').replace("'", "")


def get_greynoise_ip(url_or_ip: str, output_filename: str):

    # Check if GreyNoise Website is reachable
    try:
        get = requests.get("https://www.greynoise.io/")
        if not get.status_code == 200:
            print("[+] GreyNoise website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] GreyNoise website is not reachable!")
        return e

    headers = {
        "Accept": "application/json",
        "key": KEY
    }

    url = "https://api.greynoise.io/v3/community/" + f"{url_or_ip}"

    print("[+] Checking in GreyNoise https://viz.greynoise.io/")

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        print("[+] IP address not found in GreyNoise!")
        return
    if response.status_code == 400:
        print("[+] IP address is not a valid routable IPv4 address.")
        return
    if response.status_code == 429:
        print("[+] Exceeded Quota. Skipping.")
        return
    if response.status_code == 500:
        print("[+] Internal server error occurred while processing IP query.")
        return

    parsed = response.json()

    if parsed['classification'] == 'malicious':
        print('[+] GreyNoise: Classification: ' + Fore.RED + 'MALICIOUS!!!' + Fore.WHITE)

    write_dict_json_html_greynoise(target=url_or_ip, dict_obj=parsed, filename=f'{output_filename}')
