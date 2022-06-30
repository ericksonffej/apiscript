import requests
import shodan
import configparser
from file_util_shodan import write_dict_json_html_shodan

cfg = configparser.ConfigParser()
cfg.read('api_configuration/config.cfg')

KEY = cfg.get('Shodan', 'Shodan_KEY').replace("'", "")


def get_shodan_ip_url(url_or_ip: str, output_filename: str):

    # Check if ShodanIO Website is reachable
    try:
        get = requests.get("https://www.shodan.io/")
        if not get.status_code == 200:
            print("[+] ShodanIO website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] ShodanIO website is not reachable!")
        return e

    target = url_or_ip

    api = shodan.Shodan(KEY)

    try:
        host = api.host(url_or_ip)
    except shodan.APIError:
        print("[+] Checking in Shodan https://www.shodan.io/")
        print(f"[+] Shodan: {target} is NOT found in Shodan!")
        return

    print("[+] Checking in Shodan https://www.shodan.io/")
    print(f"[+] Shodan: Found in Shodan database!")

    write_dict_json_html_shodan(target=url_or_ip, dict_obj=host, filename=f'{output_filename}')



