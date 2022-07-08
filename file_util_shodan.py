import re
import pytz
from datetime import datetime
from pathlib import Path


def write_dict_json_html_shodan(target: str, dict_obj: dict, filename: str) -> None:
    now = datetime.now(pytz.timezone('Asia/Manila'))
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S %Z")
    output = f'{filename}_{target}'
    res = re.sub("[://|?]", "", output)
    final_output = re.search(r"([\w\-\.]+\.\w\w)", res)
    final_res = final_output.group(0)
    path = Path(f'output/{final_res}.html')

    city = dict_obj.get('city')
    ip_str = dict_obj.get('ip_str')
    isp = dict_obj.get('isp')
    hostnames = dict_obj.get('hostnames')
    hostname = f'{hostnames}'.strip("[]")
    country_code = dict_obj.get('country_code')
    country_name = dict_obj.get('country_name')
    domains = dict_obj.get('domains')
    domain = f'{domains}'.strip("[]")
    org = dict_obj.get('org')
    asn = dict_obj.get('asn')
    ports = dict_obj.get('ports')

    with open('template/template.html', "r") as f:
        content = f.read()

    if path.is_file():
        rows = ["<div id=\"Shodan\" class=\"tabcontent\">"
                "<h2>", ip_str, "</h2>"
                "<table><tr><th colspan=2>General Information</th></tr>"
                "<tr><td>Hostnames</td><td>", hostname, "</td></tr>"
                "<tr><td>Domains</td><td>", domain, "</td></tr>"
                "<tr><td>Country</td><td>", country_name, "</td></tr>"
                "<tr><td>Country Code</td><td>", country_code, "</td></tr>"
                "<tr><td>City</td><td>", city, "</td></tr>"
                "<tr><td>Organization</td><td>", org, "</td></tr>"
                "<tr><td>ISP</td><td>", isp, "</td></tr>"
                "<tr><td>ASN</td><td>", asn, "</td></tr>"
                "<tr><td>Open Ports</td><td>", ports, "</td></tr>"
                "</table><br></div>"]

        write_to_file(filename=f'{filename}_{target}', rows=rows)

    else:
        rows = [content,
                "<div id=\"Shodan\" class=\"tabcontent\">"
                "<h2>", ip_str, "</h2>"
                "<table><tr><th colspan=2>General Information</th></tr>"
                "<tr><td>Hostnames</td><td>", hostname, "</td></tr>"
                "<tr><td>Domains</td><td>", domains, "</td></tr>"
                "<tr><td>Country</td><td>", country_name, "</td></tr>"
                "<tr><td>Country Code</td><td>", country_code, "</td></tr>"
                "<tr><td>City</td><td>", city, "</td></tr>"
                "<tr><td>Organization</td><td>", org, "</td></tr>"
                "<tr><td>ISP</td><td>", isp, "</td></tr>"
                "<tr><td>ASN</td><td>", asn, "</td></tr>"
                "<tr><td>Open Ports</td><td>", ports, "</td></tr>"
                "</table></div>"]

        write_to_file(filename=f'{filename}_{target}', rows=rows)

    with open(f'output/{final_res}.html', "r", encoding='utf-8') as f:
        lines = f.readlines()
    with open(f'output/{final_res}.html', "w", encoding='utf-8') as f:
        for line in lines:
            f.write(re.sub(r'<td></td></tr><!--Shodan-->', f'<td>Found in our database.</td></tr>', line))

    with open(f'output/{final_res}.html', "r", encoding='utf-8') as f:
        lines = f.read()
    with open(f'output/{final_res}.html', "w", encoding='utf-8') as f:
        f.write(re.sub(r'<td></td></tr><!--Ticket-->', f'<td>{filename}</td></tr>', lines))

    with open(f'output/{final_res}.html', "r", encoding='utf-8') as f:
        lines = f.read()
    with open(f'output/{final_res}.html', "w", encoding='utf-8') as f:
        f.write(re.sub(r'<td></td></tr><!--Target-->', f'<td>{target}</td></tr>', lines))

    with open(f'output/{final_res}.html', "r", encoding='utf-8') as f:
        lines = f.read()
    with open(f'output/{final_res}.html', "w", encoding='utf-8') as f:
        f.write(re.sub(r'<td></td></tr><!--Date-->', f'<td>{dt_string}</td></tr>', lines))


def write_to_file(filename: str, rows: list) -> None:
    output = f'{filename}'
    res = re.sub("[://|?]", "", output)
    final_output = re.search(r"([\w\-\.]+\.\w\w)", res)
    final_res = final_output.group(0)
    # print(f'[+] Writing to file {output}...')
    with open(f'output/{final_res}.html', 'a', encoding='utf-8') as f:
        for row in rows:
            f.write(f'{row}\n')