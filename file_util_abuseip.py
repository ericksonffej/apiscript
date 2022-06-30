import re
import pytz
from datetime import datetime
from pathlib import Path


def write_dict_json_html_abuseipdb(target: str, dict_obj: dict, dict_obj1: dict, filename: str) -> None:
    now = datetime.now(pytz.timezone('Asia/Manila'))
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S %Z")
    output = f'{filename}_{target}.html'
    res = re.sub("[://|?]", "", output)
    path = Path(f'output/{res}')

    report = dict_obj1.get("data").get("results")

    reportingCategories = {
        1: 'DNS_Comprompise',
        2: 'DNS_Poisoning',
        3: 'Fraud_Orders',
        4: 'DDoS_Attack',
        5: 'FTP_Brute-Force',
        6: 'Ping_of_Death',
        7: 'Phishing',
        8: 'Fraud_VoIP',
        9: 'Open_Proxy',
        10: 'Web_Spam',
        11: 'Email_Spam',
        12: 'Blog_Spam',
        13: 'VPN_IP',
        14: 'Port_Scan',
        15: 'Hacking',
        16: 'SQL_Injection',
        17: 'Spoofing',
        18: 'Brute-Force',
        19: 'Bad_Web_Bot',
        20: 'Exploited_Host',
        21: 'Web_App_Attack',
        22: 'SSH',
        23: 'IoT_Targeted'
    }

    with open('template/template.html', "r") as f:
        content = f.read()

    if path.is_file():
        rows = ["<div id=\"AbuseIPDB\" class=\"tabcontent\">"
                "<h2>AbuseIPDB >>", target, "</h2>"]
        for r in dict_obj.values():
            ipAddress = r['ipAddress']
            isp = r['isp']
            countryCode = r['countryCode']
            domain = r['domain']
            domains = f'{domain}'.strip("[]")
            hostnames = r['hostnames']
            hostname = f'{hostnames}'.strip("[]")
            abuseConfidenceScore = r['abuseConfidenceScore']
            lastReportedAt = r['lastReportedAt']
            numDistinctUsers = r['numDistinctUsers']
            totalReports = r['totalReports']
            usageType = r['usageType']

            if r['totalReports'] == 0:
                rows.append(f"<table><tr><th colspan=2>{ipAddress} was NOT found in our database!</th></tr>")
                rows.append(f"<tr><td>ISP</td><td>{isp}</td></tr>")
                rows.append(f"<tr><td>Usage Type</td><td>{usageType}</td></tr>")
                rows.append(f"<tr><td>Hostname(s)</td><td>{hostname}</td></tr>")
                rows.append(f"<tr><td>Domain</td><td>{domains}</td></tr>")
                rows.append(f"<tr><td>Country</td><td>{countryCode}</td></tr>")
                rows.append(f"</table><br>")
                rows.append(f"<h2>IP Abuse Reports for {ipAddress}</h2>")
                rows.append(f"<p><i>The IP address has not been reported.</i></p><br></table>")

                with open(f'output/{res}', "r", encoding='utf-8') as f:
                    lines = f.readlines()
                with open(f'output/{res}', "w", encoding='utf-8') as f:
                    for line in lines:
                        f.write(re.sub(r'<td></td></tr><!--AbuseIPDB-->',
                                       f'<td>Target has not been reported.</td></tr>', line))

            elif r['totalReports'] > 0:
                rows.append(f"<table><tr><th colspan=2>{ipAddress} was found in our database!</th></tr>")
                rows.append(
                    f"<tr><th colspan=2>{ipAddress} was reported <font color=#ff0000>{totalReports}</font> times. Confidence of Abuse is <font color=#ff0000>{abuseConfidenceScore}%</font></th></tr>")
                rows.append(f"<tr><td>ISP</td><td>{isp}</td></tr>")
                rows.append(f"<tr><td>Usage Type</td><td>{usageType}</td></tr>")
                rows.append(f"<tr><td>Hostname(s)</td><td>{hostname}</td></tr>")
                rows.append(f"<tr><td>Domain</td><td>{domains}</td></tr>")
                rows.append(f"<tr><td>Country</td><td>{countryCode}</td></tr>")
                rows.append(f"</table><br>")
                rows.append(f"<h2>IP Abuse Reports for {ipAddress}</h2>")
                rows.append(
                    f"<p>The IP address has been reported a total of <b>{totalReports}</b> times from <b>{numDistinctUsers}</b> distinct sources. The most recent report was <b>{lastReportedAt}</b>.</p>")

                with open(f'output/{res}', "r", encoding='utf-8') as f:
                    lines = f.readlines()
                with open(f'output/{res}', "w", encoding='utf-8') as f:
                    for line in lines:
                        f.write(re.sub(r'<td></td></tr><!--AbuseIPDB-->',
                                       f'<td>Reported <font color=#ff0000>{totalReports}</font> times. Confidence of Abuse: <font color=#ff0000>{abuseConfidenceScore}%</font></td></tr>',
                                       line))

        rows.append(f'<br><table><tr><th>Reporter</th><th>Date</th><th>Comment</th><th>Categories</th></tr>')

        for rep in report:
            reportedAt = rep.get('reportedAt')
            comment = rep.get('comment')
            reportId = rep.get('reporterId')
            categories = rep.get('categories')

            rows.append(f'<tr><td>{reportId}</td><td>{reportedAt}</td><td>{comment}</td>')

            cat = list(map(int, categories))

            matches = []
            for i in cat:
                for match in reportingCategories.items():
                    if i in match:
                        matches.append(match[1])

            separator = ", \n"
            category_str = separator.join(matches)
            rows.append(f'<td>{category_str}</td>')

        rows.append(f'</table></div>')

        write_to_file(filename=f'{filename}_{target}.html', rows=rows)
    else:
        rows = [content,
                "<div id=\"AbuseIPDB\" class=\"tabcontent\">"
                "<h2>AbuseIPDB >>", target, "</h2>"]

        for r in dict_obj.values():
            ipAddress = r['ipAddress']
            isp = r['isp']
            countryCode = r['countryCode']
            domain = r['domain']
            domains = f'{domain}'.strip("[]")
            hostnames = r['hostnames']
            hostname = f'{hostnames}'.strip("[]")
            abuseConfidenceScore = r['abuseConfidenceScore']
            lastReportedAt = r['lastReportedAt']
            numDistinctUsers = r['numDistinctUsers']
            totalReports = r['totalReports']
            usageType = r['usageType']

            if r['totalReports'] == 0:
                rows.append(f"<table><tr><th colspan=2>{ipAddress} was NOT found in our database!</th></tr>")
                rows.append(f"<tr><td>ISP</td><td>{isp}</td></tr>")
                rows.append(f"<tr><td>Usage Type</td><td>{usageType}</td></tr>")
                rows.append(f"<tr><td>Hostname(s)</td><td>{hostname}</td></tr>")
                rows.append(f"<tr><td>Domain</td><td>{domains}</td></tr>")
                rows.append(f"<tr><td>Country</td><td>{countryCode}</td></tr>")
                rows.append(f"</table><br>")
                rows.append(f"<h2>IP Abuse Reports for {ipAddress}</h2>")
                rows.append(f"<p><i>The IP address has not been reported.</i></p><br></div>")
            elif r['totalReports'] > 0:
                rows.append(f"<table><tr><th colspan=2>{ipAddress} was found in our database!</th></tr>")
                rows.append(
                    f"<tr><th colspan=2>{ipAddress} was reported <font color=#ff0000>{totalReports}</font> times. Confidence of Abuse is <font color=#ff0000>{abuseConfidenceScore}%</font></th></tr>")
                rows.append(f"<tr><td>ISP</td><td>{isp}</td></tr>")
                rows.append(f"<tr><td>Usage Type</td><td>{usageType}</td></tr>")
                rows.append(f"<tr><td>Hostname(s)</td><td>{hostname}</td></tr>")
                rows.append(f"<tr><td>Domain</td><td>{domains}</td></tr>")
                rows.append(f"<tr><td>Country</td><td>{countryCode}</td></tr>")
                rows.append(f"</table><br>")
                rows.append(f"<h2>IP Abuse Reports for {ipAddress}</h2>")
                rows.append(
                    f"<p>The IP address has been reported a total of <b>{totalReports}</b> times from <b>{numDistinctUsers}</b> distinct sources. The most recent report was <b>{lastReportedAt}</b>.</p>")

        rows.append(f'<br><table><tr><th>Reporter</th><th>Date</th><th>Comment</th><th>Categories</th></tr>')

        for rep in report:
            reportedAt = rep.get('reportedAt')
            comment = rep.get('comment')
            reportId = rep.get('reporterId')
            categories = rep.get('categories')

            rows.append(f'<tr><td>{reportId}</td><td>{reportedAt}</td><td>{comment}</td>')

            cat = list(map(int, categories))

            matches = []
            for i in cat:
                for match in reportingCategories.items():
                    if i in match:
                        matches.append(match[1])

            separator = ", \n"
            category_str = separator.join(matches)
            rows.append(f'<td>{category_str}</td>')

        rows.append(f'</table></div>')

        write_to_file(filename=f'{filename}_{target}.html', rows=rows)

        if r['totalReports'] == 0:
            with open(f'output/{res}', "r", encoding='utf-8') as f:
                lines = f.readlines()
            with open(f'output/{res}', "w", encoding='utf-8') as f:
                for line in lines:
                    f.write(
                        re.sub(r'<td></td></tr><!--AbuseIPDB-->', f'<td>Target has not been reported.</td></tr>', line))
        elif r['totalReports'] > 0:
            with open(f'output/{res}', "r", encoding='utf-8') as f:
                lines = f.readlines()
            with open(f'output/{res}', "w", encoding='utf-8') as f:
                for line in lines:
                    f.write(
                        re.sub(r'<td></td></tr><!--AbuseIPDB-->',
                               f'<td>Reported <font color=red>{totalReports}</font> times. Confidence of Abuse: <font color=#ff0000>{abuseConfidenceScore}%</font></td></tr>',
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


def write_to_file(filename: str, rows: list) -> None:
    output = f'{filename}'
    res = re.sub("[://|?]", "", output)
    # print(f'[+] Writing to file {output}...')
    with open(f'output/{res}', 'a', encoding='utf-8') as f:
        for row in rows:
            f.write(f'{row}\n')
