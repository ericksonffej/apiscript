import re
import pytz
from datetime import datetime
from pathlib import Path

now = datetime.now(pytz.timezone('Asia/Manila'))
dt_string = now.strftime("%d/%m/%Y %H:%M:%S %Z")


def write_dict_json_html_ibmxforce(target: str, dict_obj: dict, dict_obj1: dict, filename: str) -> None:
    output = f'{filename}_{target}.html'
    res = re.sub("[://|?]", "", output)
    path = Path(f'output/{res}')

    # IP Reputation Information
    ip_addr = dict_obj["ip"]
    cats_info = dict_obj.get("cats")
    category = f'{cats_info}'.strip("{}")
    country_info = dict_obj.get("geo")
    score = dict_obj["score"]

    # Additional Information
    country = country_info["country"]

    # WHOIS Information
    contact_info = dict_obj1["contact"]

    organization = contact_info[0]["organization"]
    contactEmail = 'contactEmail'
    registrarName = 'registrarName'
    registrantname = 'name'
    createdDate = 'createdDate'
    updatedDate = 'updatedDate'

    with open('template/template.html', "r") as f:
        content = f.read()

    if path.is_file():
        rows = ["<div id=\"IBM X-Force\" class=\"tabcontent\"><br>"
                "<table><tr><th colspan=2><b>X-Force IP Report</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>IP Address</b></td><td>", ip_addr, "</td></tr>"
                "<tr><td><b>Risk Score</b></td><td>", score, "</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>Details</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>Categorization</b></td><td>", category, "%</td></tr>"
                "<tr><td><b>Location</b></td><td>", country, "</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>WHOIS Record</b></th></tr>"]

        if createdDate in dict_obj1:
            created_date = dict_obj1["createdDate"]
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td>{created_date}</td></tr>")
        else:
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td></td></tr>")

        if updatedDate in dict_obj1:
            updated_date = dict_obj1["updatedDate"]
            rows.append(f"<tr><td><b>Updated</b></td><td>{updated_date}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Updated</b></td><td></td></tr>")

        rows.append(f"<tr><td><b>Registrant Organization</b></td><td>{organization}</td></tr>")

        if registrantname in dict_obj1:
            registrantname = dict_obj1[0]["name"]
            rows.append(f"<tr><td><b>Registrant Name</b></td><td>{registrantname}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")

        if registrarName in dict_obj1:
            registrar = dict_obj1["registrarName"]
            rows.append(f"<tr><td><b>Registrar Name</b></td><td>{registrar}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrar Name</b></td><td></td></tr>")

        if contactEmail in dict_obj1:
            contact = dict_obj1["contactEmail"]
            rows.append(f"<tr><td><b>Email</b></td><td>{contact}</td></tr></table></div><br>")
        else:
            rows.append(f"<tr><td><b>Email</b></td><td></td></tr></table></div><br>")

    else:
        rows = [content,
                "<div id=\"IBM X-Force\" class=\"tabcontent\">"
                "<br><table><tr><th colspan=2><b>X-Force IP Report</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>IP Address</b></td><td>", ip_addr, "</td></tr>"
                "<tr><td><b>Risk Score</b></td><td>", score, "</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>Details</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>Categorization</b></td><td>", category, "%</td></tr>"
                "<tr><td><b>Location</b></td><td>", country, "</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>WHOIS Record</b></th></tr>"]

        if createdDate in dict_obj1:
            created_date = dict_obj1["createdDate"]
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td>{created_date}</td></tr>")
        else:
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td></td></tr>")

        if updatedDate in dict_obj1:
            updated_date = dict_obj1["updatedDate"]
            rows.append(f"<tr><td><b>Updated</b></td><td>{updated_date}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Updated</b></td><td></td></tr>")

        rows.append(f"<tr><td><b>Registrant Organization</b></td><td>{organization}</td></tr>")

        if registrantname in dict_obj1:
            registrantname = dict_obj1[0]["name"]
            rows.append(f"<tr><td><b>Registrant Name</b></td><td>{registrantname}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")

        if registrarName in dict_obj1:
            registrar = dict_obj1["registrarName"]
            rows.append(f"<tr><td><b>Registrar Name</b></td><td>{registrar}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrar Name</b></td><td></td></tr>")

        if contactEmail in dict_obj1:
            contact = dict_obj1["contactEmail"]
            rows.append(f"<tr><td><b>Email</b></td><td>{contact}</td></tr></table></div><br>")
        else:
            rows.append(f"<tr><td><b>Email</b></td><td></td></tr></table></div><br>")

    write_to_file(filename=f'{filename}_{target}.html', rows=rows)

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.readlines()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        for line in lines:
            if score >= 6:
                f.write(re.sub(r'<td></td></tr><!--X-Force-->', f"<td>X-Force IP Report: <font color=red>Risk {score}</font></td></tr>", line))
            elif score >= 3:
                f.write(re.sub(r'<td></td></tr><!--X-Force-->', f"<td>X-Force IP Report: <font color=orange>Risk {score}</font></td></tr>", line))
            else:
                f.write(re.sub(r'<td></td></tr><!--X-Force-->', f"<td>X-Force IP Report: <font color=green>Risk {score}</font></td></tr>", line))

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


def write_dict_json_html_ibmxforce_url_whois(target: str, dict_obj1: dict, filename: str) -> None:
    output = f'{filename}_{target}.html'
    res = re.sub("[://|?]", "", output)
    path = Path(f'output/{res}')

    # WHOIS Information
    # contact_info = dict_obj1["contact"]
    # created_date = dict_obj1["createdDate"]
    # updated_date = dict_obj1["updatedDate"]
    # contact = dict_obj1["contactEmail"]
    # registrant = dict_obj1.get("contact")[0]["name"]
    # organization = contact_info[0]["organization"]
    # region = contact_info[0]["country"]

    contact = 'contact'
    contactEmail = 'contactEmail'
    registrarName = 'registrarName'
    registrantname = 'name'
    createdDate = 'createdDate'
    updatedDate = 'updatedDate'

    with open('template/template.html', "r") as f:
        content = f.read()

    if path.is_file():
        rows = ["<div id=\"IBM X-Force\" class=\"tabcontent\"><br>"
                "<table><tr><th colspan=2><b>X-Force URL Report</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>URL</b></td><td>", target, "</td></tr>"
                "<tr><td><b>Risk Score</b></td><td>Risk Unknown</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>Details</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>Categorization</b></td><td>Unknown</td></tr>"
                "</table><br>"
                ""
                "<table><tr><th colspan=2><b>WHOIS Record</b></th></tr>"]

        if createdDate in dict_obj1:
            created_date = dict_obj1["createdDate"]
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td>{created_date}</td></tr>")
        else:
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td></td></tr>")

        if updatedDate in dict_obj1:
            updated_date = dict_obj1["updatedDate"]
            rows.append(f"<tr><td><b>Updated</b></td><td>{updated_date}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Updated</b></td><td></td></tr>")

        if contact in dict_obj1:
            contact = dict_obj1.get("contact")[0]
            if registrantname in contact:
                registrant_name = contact["name"]
                rows.append(f"<tr><td><b>Registrant Name</b></td><td>{registrant_name}</td></tr>")
            else:
                rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")

        if registrarName in dict_obj1:
            registrar = dict_obj1["registrarName"]
            rows.append(f"<tr><td><b>Registrar Name</b></td><td>{registrar}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrar Name</b></td><td></td></tr>")

        if contactEmail in dict_obj1:
            contact = dict_obj1["contactEmail"]
            rows.append(f"<tr><td><b>Email</b></td><td>{contact}</td></tr></table></div><br>")
        else:
            rows.append(f"<tr><td><b>Email</b></td><td></td></tr></table></div><br>")

    else:
        rows = [content,
                "<div id=\"IBM X-Force\" class=\"tabcontent\">"
                "<br><table><tr><th colspan=2><b>X-Force URL Report</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>URL</b></td><td>", target, "</td></tr>"
                "<tr><td><b>Risk Score</b></td><td>Risk Unknown</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>Details</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>Categorization</b></td><td>Unknown</td></tr>"
                "</table><br>"
                ""
                "<table><tr><th colspan=2><b>WHOIS Record</b></th></tr>"]

        if createdDate in dict_obj1:
            created_date = dict_obj1["createdDate"]
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td>{created_date}</td></tr>")
        else:
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td></td></tr>")

        if updatedDate in dict_obj1:
            updated_date = dict_obj1["updatedDate"]
            rows.append(f"<tr><td><b>Updated</b></td><td>{updated_date}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Updated</b></td><td></td></tr>")

        if contact in dict_obj1:
            contact = dict_obj1.get("contact")[0]
            if registrantname in contact:
                registrant_name = contact["name"]
                rows.append(f"<tr><td><b>Registrant Name</b></td><td>{registrant_name}</td></tr>")
            else:
                rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")

        if registrarName in dict_obj1:
            registrar = dict_obj1["registrarName"]
            rows.append(f"<tr><td><b>Registrar Name</b></td><td>{registrar}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrar Name</b></td><td></td></tr>")

        if contactEmail in dict_obj1:
            contact = dict_obj1["contactEmail"]
            rows.append(f"<tr><td><b>Email</b></td><td>{contact}</td></tr></table></div><br>")
        else:
            rows.append(f"<tr><td><b>Email</b></td><td></td></tr></table></div><br>")

    write_to_file(filename=f'{filename}_{target}.html', rows=rows)

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.readlines()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        for line in lines:
            f.write(re.sub(r'<td></td></tr><!--X-Force-->', f"<td>X-Force URL Report: Risk Unknown</td></tr>", line))

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


def write_dict_json_html_ibmxforce_url(target: str, dict_obj: dict, dict_obj1: dict, filename: str) -> None:
    output = f'{filename}_{target}.html'
    res = re.sub("[://|?]", "", output)
    path = Path(f'output/{res}')

    # URL information
    category_info = dict_obj.get("result")
    category_url = category_info["url"]
    cats_info = dict_obj.get("cats")
    category = f'{cats_info}'.strip("{}")
    separator = ", \n"
    category_conv = separator.join(category)
    # country_info = dict_obj.get("geo")
    score = category_info["score"]

    # Additional Information
    # country = country_info["country"]

    # WHOIS Information
    # contact_info = dict_obj1["contact"]
    # created_date = dict_obj1["createdDate"]
    # updated_date = dict_obj1["updatedDate"]
    # contact = dict_obj1["contactEmail"]
    # registrant = dict_obj1.get("contact")[0]
    # organization = contact_info[0]["organization"]
    # region = contact_info[0]["country"]

    organization = 'organization'
    contact = 'contact'
    contact_info = 'contact'
    contactEmail = 'contactEmail'
    registrarName = 'registrarName'
    registrantname = 'name'
    createdDate = 'createdDate'
    updatedDate = 'updatedDate'

    with open('template/template.html', "r") as f:
        content = f.read()

    if path.is_file():
        rows = ["<div id=\"IBM X-Force\" class=\"tabcontent\"><br>"
                "<table><tr><th colspan=2><b>X-Force URL Report</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>URL</b></td><td>", category_url, "</td></tr>"
                "<tr><td><b>Risk Score</b></td><td>", score, "</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>Details</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>Categorization</b></td><td>", category_conv, "</td></tr>"
                "</table><br>"
                ""
                "<table><tr><th colspan=2><b>WHOIS Record</b></th></tr>"]

        if createdDate in dict_obj1:
            created_date = dict_obj1["createdDate"]
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td>{created_date}</td></tr>")
        else:
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td></td></tr>")

        if updatedDate in dict_obj1:
            updated_date = dict_obj1["updatedDate"]
            rows.append(f"<tr><td><b>Updated</b></td><td>{updated_date}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Updated</b></td><td></td></tr>")

        rows.append(f"<tr><td><b>Registrant Organization</b></td><td>{organization}</td></tr>")

        if contact_info in dict_obj1:
            contact_info = dict_obj1.get("contact")[0]
            if organization in contact_info:
                org = contact_info["organization"]
                rows.append(f"<tr><td><b>Registrant Organization</b></td><td>{org}</td></tr>")
            else:
                rows.append(f"<tr><td><b>Registrant Organization</b></td><td></td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Organization</b></td><td></td></tr>")

        if contact in dict_obj1:
            contact = dict_obj1.get("contact")[0]
            if registrantname in contact:
                registrant_name = contact["name"]
                rows.append(f"<tr><td><b>Registrant Name</b></td><td>{registrant_name}</td></tr>")
            else:
                rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")

        # if registrantname in registrant:
        #     registrant_name = registrant["name"]
        #     rows.append(f"<tr><td><b>Registrant Name</b></td><td>{registrant_name}</td></tr>")
        # else:
        #     rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")

        if registrarName in dict_obj1:
            registrar = dict_obj1["registrarName"]
            rows.append(f"<tr><td><b>Registrar Name</b></td><td>{registrar}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrar Name</b></td><td></td></tr>")

        if contactEmail in dict_obj1:
            contact = dict_obj1["contactEmail"]
            rows.append(f"<tr><td><b>Email</b></td><td>{contact}</td></tr></table></div><br>")
        else:
            rows.append(f"<tr><td><b>Email</b></td><td></td></tr></table></div><br>")

    else:
        rows = [content,
                "<div id=\"IBM X-Force\" class=\"tabcontent\">"
                "<br><table><tr><th colspan=2><b>X-Force URL Report</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>URL</b></td><td>", category_url, "</td></tr>"
                "<tr><td><b>Risk Score</b></td><td>", score, "</td></tr></table><br>"
                ""
                "<table><tr><th colspan=2><b>Details</b></th></tr>"
                "<tr><td width=20%; text-align=\"right\"><b>Categorization</b></td><td>", category_conv, "</td></tr>"
                "</table><br>"
                ""
                "<table><tr><th colspan=2><b>WHOIS Record</b></th></tr>"]

        if createdDate in dict_obj1:
            created_date = dict_obj1["createdDate"]
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td>{created_date}</td></tr>")
        else:
            rows.append(f"<tr><td width=20%; text-align=\"right\"><b>Created</b></td><td></td></tr>")

        if updatedDate in dict_obj1:
            updated_date = dict_obj1["updatedDate"]
            rows.append(f"<tr><td><b>Updated</b></td><td>{updated_date}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Updated</b></td><td></td></tr>")

        if contact_info in dict_obj1:
            contact_info = dict_obj1.get("contact")[0]
            if organization in contact_info:
                org = contact_info["organization"]
                rows.append(f"<tr><td><b>Registrant Organization</b></td><td>{org}</td></tr>")
            else:
                rows.append(f"<tr><td><b>Registrant Organization</b></td><td></td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Organization</b></td><td></td></tr>")

        if contact in dict_obj1:
            contact = dict_obj1.get("contact")[0]
            if registrantname in contact:
                registrant_name = contact["name"]
                rows.append(f"<tr><td><b>Registrant Name</b></td><td>{registrant_name}</td></tr>")
            else:
                rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrant Name</b></td><td></td></tr>")

        if registrarName in dict_obj1:
            registrar = dict_obj1["registrarName"]
            rows.append(f"<tr><td><b>Registrar Name</b></td><td>{registrar}</td></tr>")
        else:
            rows.append(f"<tr><td><b>Registrar Name</b></td><td></td></tr>")

        if contactEmail in dict_obj1:
            contact = dict_obj1["contactEmail"]
            rows.append(f"<tr><td><b>Email</b></td><td>{contact}</td></tr></table></div><br>")
        else:
            rows.append(f"<tr><td><b>Email</b></td><td></td></tr></table></div>")

    write_to_file(filename=f'{filename}_{target}.html', rows=rows)

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.readlines()
    with open(f'output/{res}', "w", encoding='utf-8') as f:
        for line in lines:
            if score >= 6:
                f.write(re.sub(r'<td></td></tr><!--X-Force-->', f"<td>X-Force URL Report: <font color=#ff0000>Risk {score}</font></td></tr>", line))
            elif score >= 3:
                f.write(re.sub(r'<td></td></tr><!--X-Force-->', f"<td>X-Force URL Report: <font color=#FFA500>Risk {score}</font></td></tr>", line))
            else:
                f.write(re.sub(r'<td></td></tr><!--X-Force-->', f"<td>X-Force URL Report: <font color=#008000>Risk {score}</font></td></tr>", line))

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
    print(f'[+] Writing to file {output}...')
    with open(f'output/{res}', 'a', encoding='utf-8') as f:
        for row in rows:
            f.write(f'{row}\n')
