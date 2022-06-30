import json
import requests
import configparser
from colorama import Fore, init
from file_util_virustotal import write_dict_json_csv_file, write_dict_json_html

init(convert=True)
cfg = configparser.ConfigParser()
cfg.read('api_configuration/config.cfg')

KEY = cfg.get('VirusTotal', 'VirusTotal_KEY').replace("'", "")


def get_vt_hash(hash_str: str, output_filename: str) -> None:

    # Check if VirusTotal Website is reachable
    try:
        get = requests.get("https://www.virustotal.com/")
        if not get.status_code == 200:
            print("[+] VirusTotal website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] VirusTotal website is not reachable!")
        return e

    # prepare API parameters
    params = {'apikey': KEY, 'resource': hash_str}
    # call API
    resp = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)

    print("[+] Checking in VT https://www.virustotal.com")

    if resp.status_code == 204:
        print("[+] Exceeded quota. Skipping.")
        return

    # parse json result from API
    json_response = resp.json()
    x = str(json_response)
    x = x.replace("'", '"')
    x = x.replace("False", '"False"')
    x = x.replace("True", '"True"')
    x = x.replace("None", '"None"')

    parsed = json.loads(x)
    response_code = parsed.get('response_code')

    # not in virus total
    if response_code == 0:
        print(f'[+] {hash_str} is NOT in Virus Total!')
        return

    scans = parsed.get('scans')
    for r in scans.values():
        #   if r.get('detected') == "TRUE":
        # print('[+] VT: Found as ' + Fore.RED + 'MALICIOUS!!!' + Fore.WHITE)
        # break
        detected = r.get('detected')
        if not detected:
            continue
        if detected.lower() == 'true':
            print('[+] VT: Security vendor found this as ' + Fore.RED + 'MALICIOUS!!!' + Fore.WHITE)
            break

    # Create CSV
    # write_dict_json_csv_file(target=hash_str, dict_obj=scans, filename=f'{output_filename}')

    # Create HTML
    write_dict_json_html(target=hash_str, dict_obj=parsed, filename=f'{output_filename}')


def get_vt_ip_url(url_or_ip: str, output_filename: str):

    # Check if VirusTotal Website is reachable
    try:
        get = requests.get("https://www.virustotal.com/")
        if not get.status_code == 200:
            print("[+] VirusTotal website is not reachable!")
            return
    except requests.ConnectionError as e:
        print("[+] VirusTotal website is not reachable!")
        return e

    # prepare API parameters
    params = {'apikey': KEY, 'resource': url_or_ip}
    # call API
    resp = requests.get('https://www.virustotal.com/vtapi/v2/url/report', params=params)

    print("[+] Checking in VT https://www.virustotal.com")

    if resp.status_code == 204:
        print("[+] Exceeded quota. Skipping.")
        return

    # parse json result from API
    json_response = resp.json()

    x = str(json_response)
    x = x.replace("'", '"')
    x = x.replace("False", '"False"')
    x = x.replace("True", '"True"')
    x = x.replace("None", '"None"')

    parsed = json.loads(x)
    response_code = parsed.get('response_code')

    # not in virus total
    if response_code == 0:
        print(f'[+] {url_or_ip} is NOT in Virus Total!')
        return

    scans = parsed.get('scans')
    for r in scans.values():
        detected = r.get('detected')
        if not detected:
            continue
        if detected.lower() == 'true':
            print('[+] VT: Security vendor found this as ' + Fore.RED + 'MALICIOUS!!!' + Fore.WHITE)
            break

    # Create CSV
    # write_dict_json_csv_file(target=url_or_ip, dict_obj=scans, filename=f'{output_filename}')

    # Create HTML
    write_dict_json_html(target=url_or_ip, dict_obj=parsed, filename=f'{output_filename}')
