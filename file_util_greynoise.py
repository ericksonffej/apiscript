import re
import pytz
from datetime import datetime
from pathlib import Path

now = datetime.now(pytz.timezone('Asia/Manila'))
dt_string = now.strftime("%d/%m/%Y %H:%M:%S %Z")


def write_dict_json_html_greynoise(target: str, dict_obj: dict, filename: str) -> None:
    output = f'{filename}_{target}.html'
    res = re.sub("[://|?]", "", output)
    path = Path(f'output/{res}')

    classification = dict_obj.get("classification")
    last_seen = dict_obj.get("last_seen")
    link = dict_obj.get("link")
    ip = dict_obj.get("ip")
    name = dict_obj.get("name")
    riot = dict_obj.get("riot")
    noise = dict_obj.get("noise")

    if classification == "malicious":
        verdict = f'Classification: <font color=#ff0000>{classification}</font>'
    else:
        verdict = f'Classification: <font color=#008000>{classification}</font>'

    with open('template/template.html', "r") as f:
        content = f.read()

    if path.is_file():
        rows = ["<div id=\"GreyNoise\" class=\"tabcontent\">\n"
                "<br>\n"
                "\n"
                "<table><tr><th colspan=2><font size=4>SUMMARY</font></th></tr>\n"
                "<tr><td width=20%; text-align=\"right\"><b>IP Address</b></td><td>", ip, "</td></tr>\n"
                "<tr><td><b>Classification</b></td><td>", verdict, "</td></tr>\n"
                "<tr><td><b>Last Seen</b></td><td>", last_seen, "</td></tr>\n"
                "<tr><td><b>Name</b></td><td>", name, "</td></tr>\n"
                "<tr><td><b>GreyNoise</b></td><td><a href=\"", link, "\" target=\"_blank\"> View Full Report</a></td></tr>\n"
                "<tr><td><b>Riot</b></td><td>", riot, "</td></tr>\n"
                "<tr><td><b>Noise</b></td><td>", noise, "</td></tr>\n"
                "</table></div>"]

    else:
        rows = [content,
                "<div id=\"GreyNoise\" class=\"tabcontent\">\n"
                "<br>\n"
                "\n"
                "<table><tr><th colspan=2><font size=4>SUMMARY</font></th></tr>\n"
                "<tr><td width=20%; text-align=\"right\"><b>IP Address</b></td><td>", ip, "</td></tr>\n"
                "<tr><td><b>Classification</b></td><td>", verdict, "</td></tr>\n"
                "<tr><td><b>Last Seen</b></td><td>", last_seen, "</td></tr>\n"
                "<tr><td><b>Name</b></td><td>", name, "</td></tr>\n"
                "<tr><td><b>GreyNoise</b></td><td><a href=\"", link, "\" target=\"_blank\"> View Full Report</a></td></tr>\n"
                "<tr><td><b>Riot</b></td><td>", riot, "</td></tr>\n"
                "<tr><td><b>Noise</b></td><td>", noise, "</td></tr>\n"
                "</table></div>"]

    write_to_file(filename=f'{filename}_{target}.html', rows=rows)

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.read()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        if classification == "malicious":
            f.write(re.sub(r'<td></td></tr><!--GreyNoise-->', f'<td>Classification: <font color=#ff0000>{classification}</font></td></tr>', lines))
        else:
            f.write(re.sub(r'<td></td></tr><!--GreyNoise-->', f'<td>Classification: {classification}</td></tr>', lines))

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.read()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        f.write(re.sub(r'<td></td></tr><!--Ticket-->', f'<td>{filename}</td></tr>', lines))

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.read()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        f.write(re.sub(r'<td></td></tr><!--Target-->', f'<td>{target}</td></tr>', lines))

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.read()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        f.write(re.sub(r'<td></td></tr><!--Date-->', f'<td>{dt_string}</td></tr>', lines))


def write_to_file(filename: str, rows: list) -> None:
    output = f'{filename}'
    res = re.sub("[://|?]", "", output)
    # print(f'[+] Writing to file {output}...')
    with open(f'output/{res}', 'a', encoding='utf-8') as f:
        for row in rows:
            f.write(f'{row}\n')
