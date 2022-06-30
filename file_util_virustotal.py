import re
from datetime import datetime
import pytz


def write_dict_json_html(target: str, dict_obj: dict, filename: str) -> None:
    # build html contents
    now = datetime.now(pytz.timezone('Asia/Manila'))
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S %Z")
    scan_date = dict_obj["scan_date"]
    total = dict_obj["total"]
    positives = dict_obj["positives"]
    permalink = dict_obj["permalink"]
    output = f'{filename}_{target}.html'
    res = re.sub("[://|?]", "", output)

    with open('template/template.html', "r") as f:
        content = f.read()

    rows = [content,
            "<div id=\"VirusTotal\" class=\"tabcontent\" style=\"display:block\">\n"
            "<br>\n"
            "\n"
            "<table><tr><th colspan=2><b>SUMMARY</b></th></tr>\n"
            "<tr><td width=20%; text-align=\"right\"><b>Score</b></td><td>", positives, "/", total, "</td></tr>\n"
                                                                                                    "<tr><td><b>Last Analysis Date</b></td><td>",
            scan_date, "</td></tr>\n"
                       "<tr><td><b>Virus Total</b></td><td><a href=\"", permalink,
            "\" target=\"_blank\"> View Full Report</a></td></tr>"
            "<table><br>\n"
            "<table><tr><th colspan=5><b>SCAN</b></th></tr>\n"
            "<tr><td><b>Scanner</b></td><td><b>Detected</b></td><td><b>Version</b></td><td><b>Result</b></td><td><b>Update</b></td></tr>\n"]

    for vendor, r in dict_obj.get("scans").items():
        detected = r.get('detected')
        version = r.get('version')
        update = r.get('update')
        result = r.get('result')

        if r.get('result') == "malicious site":
            rows.append(
                f"<tr><td>{vendor}</td><td>{detected}</td><td>{version}</td><td><font color=#ff0000><b>{result}</b></font></td><td>{update}</td></tr>\n")
        elif r.get('result') == "clean site":
            continue
        elif r.get('result') == "unrated site":
            continue
        elif r.get('result') == "None":
            continue
        else:
            rows.append(
                f"<tr><td>{vendor}</td><td>{detected}</td><td>{version}</td><td><font color=#ff0000><b>{result}</b></font></td><td>{update}</td></tr>\n")
            # rows.append(f"<td>{update}</td></tr>\n")

    rows.append(f"</table></div>")

    write_to_file(filename=f'{filename}_{target}.html', rows=rows)

    with open(f'output/{res}', "r") as f:
        lines = f.readlines()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        for line in lines:
            if positives == 0:
                f.write(re.sub(r'<td></td></tr><!--VirusTotal-->',
                               f'<td>Security vendors found it as <font color=#008000>Clean</font></td></tr>', line))
            else:
                f.write(re.sub(r'<td></td></tr><!--VirusTotal-->',
                               f'<td>Security vendors found it as <font color=#ff0000>Malicious</font></td></tr>',
                               line))

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


def write_dict_json_csv_file(target: str, dict_obj: dict, filename: str) -> None:
    # build csv contents
    rows = [
        "==================================================================",
        target,
        "Vendor,Detected,Version,Result,Update"
    ]

    for vendor, r in dict_obj.get("scans").items():
        detected = r.get('detected')
        version = r.get('version', '---')
        result = r.get('result')
        update = r.get('update', '---')
        rows.append(f"{vendor},{detected},{version},{result},{update}")

    write_to_file(filename=f'{filename}.csv', rows=rows)


def write_to_file(filename: str, rows: list) -> None:
    output = f'{filename}'
    res = re.sub("[://|?]", "", output)
    # print(f'[+] Writing to file {output}...')
    with open(f'output/{res}', 'a', encoding='utf-8') as f:
        for row in rows:
            f.write(f'{row}\n')


def read_file() -> str:
    # TODO: read file
    # content = ['45.154.98.173', 'www.17ebook.com', '192.168.1.1', '6a8401448a5bd2b540850f811b20a66d']
    # return content
    with open('input/input.txt', "r", encoding='utf-8') as f:
        content = f.read().split()
    # print(content)
    # exit(1)
    return content
