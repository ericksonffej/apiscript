import base64
import requests
import configparser
from file_util_ibmxforce import write_dict_json_html_ibmxforce, write_dict_json_html_ibmxforce_url, \
    write_dict_json_html_ibmxforce_url_whois

cfg = configparser.ConfigParser()
cfg.read('api_configuration/config.cfg')

KEY = cfg.get('IBM_X-Force', 'X-Force_KEY').replace("'", "")
PASS = cfg.get('IBM_X-Force', 'X-Force_PASS').replace("'", "")

x_cred = f'{KEY}:{PASS}'
data = base64.b64encode(x_cred.encode())
auth_string = str(data.decode('utf-8'))


def get_ibmxforce_ip(url_or_ip: str, output_filename: str):

    # Check if IBM X-Force Website is reachable
    try:
        get = requests.get("https://api.xforce.ibmcloud.com/")
        if not get.status_code == 200:
            print("[+] IBM X-Force website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] IBM X-Force website is not reachable!")
        return e

    header = {"Authorization": "Basic %s " % auth_string, "Accept": "application/json"}

    url_ipaddr = "https://api.xforce.ibmcloud.com/" + "ipr/%s" % url_or_ip
    url_whois = "https://api.xforce.ibmcloud.com/" + "whois/%s" % url_or_ip

    print("[+] Checking in IBM X-Force https://exchange.xforce.ibmcloud.com/")
    if get.status_code == 402:
        print("[+] Exceeded quota. Skipping.")
        return

    resp_ipaddr = requests.get(url_ipaddr, headers=header)
    resp_whois = requests.get(url_whois, headers=header)

    parsed_ipaddr = resp_ipaddr.json()
    parsed_whois = resp_whois.json()

    write_dict_json_html_ibmxforce(target=url_or_ip, dict_obj=parsed_ipaddr, dict_obj1=parsed_whois, filename=f'{output_filename}')


def get_ibmxforce_url(url_or_ip: str, output_filename: str):

    # Check if IBM X-Force Website is reachable
    try:
        get = requests.get("https://api.xforce.ibmcloud.com/")
        if not get.status_code == 200:
            print("[+] IBM X-Force website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] IBM X-Force website is not reachable!")
        return e

    header = {"Authorization": "Basic %s " % auth_string, "Accept": "application/json"}

    url = "https://api.xforce.ibmcloud.com/" + "url/%s" % url_or_ip
    url_whois = "https://api.xforce.ibmcloud.com/" + "whois/%s" % url_or_ip

    print("[+] Checking in IBM X-Force https://exchange.xforce.ibmcloud.com/")
    if get.status_code == 402:
        print("[+] Exceeded quota. Skipping.")
        return

    resp_url = requests.get(url, headers=header)
    resp_whois = requests.get(url_whois, headers=header)

    parsed_whois = resp_whois.json()

    if resp_url.status_code == 404:
        print("[+] IBM X-Force: Risk Unknown")

        write_dict_json_html_ibmxforce_url_whois(target=url_or_ip, dict_obj1=parsed_whois, filename=f'{output_filename}')
    else:
        parsed_url = resp_url.json()

        write_dict_json_html_ibmxforce_url(target=url_or_ip, dict_obj=parsed_url, dict_obj1=parsed_whois, filename=f'{output_filename}')