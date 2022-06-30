import re
import pytz
from datetime import datetime
from pathlib import Path


def write_dict_json_html_urlscan(target: str, dict_obj: dict, filename: str) -> None:
    now = datetime.now(pytz.timezone('Asia/Manila'))
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S %Z")
    output = f'{filename}_{target}.html'
    res = re.sub("[://|?]", "", output)
    path = Path(f'output/{res}')

    # relevant aggregate data
    verdict_info = dict_obj.get("verdicts")
    list_info = dict_obj.get("lists")
    stats_info = dict_obj.get("stats")
    page_info = dict_obj.get("page")
    sshot = dict_obj.get("task")

    # more data
    ip_count = list_info.get("ips")
    domain_count = list_info.get("domains")
    url_count = list_info.get("urls")
    links = list_info.get("linkDomains")

    # data for summary
    page_domain = page_info.get("domain")
    page_url = page_info.get("url")
    page_ip = page_info.get("ip")
    page_country = page_info.get("country")
    page_city = page_info.get("city")
    page_asnname = page_info.get("asnname")
    country_count = stats_info.get("uniqCountries")
    secureRequests = stats_info.get("secureRequests")
    malicious_code = verdict_info.get("overall").get("malicious")
    brands = verdict_info.get("overall").get("brands")
    sshot_link = sshot.get("screenshotURL")

    with open('template/template.html', "r") as f:
        content = f.read()

    # IP Count
    ip_list = []
    for ip in ip_count:
        ip_list.append(ip)

    ips = len(ip_list)

    # Domain Count
    domain_list = []
    for domain in domain_count:
        domain_list.append(domain)

    domains = len(domain_list)

    # URL count
    url_list = []
    for url in url_count:
        url_list.append(url)

    urls_http = len(url_list)

    # Result for Malicious or Clean
    if not malicious_code:
        verdict = f'<font color=#008000>No Classification</font>'
    else:
        verdict = f'<font color=#ff0000>Malicious!</font>'

    if path.is_file():
        rows = ["<div id=\"URLScanIO\" class=\"tabcontent\">"
                "<h2>", page_domain, "</h2>"
                "<b>IP Address:</b>", page_ip, "<br>"
                "<b>Effective URL:</b><font color=#008000><i>", page_url, "</i></font>"
                "<h2>Summary</h2>"
                "This website contacted <b>", ips, "IPs</b> in <b>", country_count, "countries </b> across <b>", domains, "domains</b> to perform <b>", urls_http, "HTTP transactions</b>."
                "This main IP is <font color=#008000><b>", page_ip, "</b></font>located in <b>", page_city, "</b><b>", page_country, "</b> and belongs to <font color=#008000><b>", page_asnname, "</b></font>.<br>" 
                "The main domain is <font color=#008000><b>", page_domain, "</b></font>."
                ""
                "<br><br><font size=5> urlscan.<font color=#008000>io</font> Verdict:", verdict, "</font><br><br>"
                "Targeting these brands:", brands, "<br>"
                ""
                "<h2>Screenshot</h2>"
                "<img src=\"", sshot_link, "\" alt=\"URLScan Screenhot\" width=\"600\" height=\"444\" border=\"1px\">"
                "<br>"
                "<h2>Domain & IP Information</h2>"
                "<button type=\"button\" class=\"collapsible\">IP ADDRESS</button>"
                "<div class=\"content\">"
                "<br><table><tr><th>IP Address</th></tr>"]

        for ip in ip_count:
            rows.append(f"<tr><td>{ip}</td></tr>")

        rows.append(f"</table></div><br><br><button type=\"button\" class=\"collapsible\">DOMAINS</button>")
        rows.append(f"<div class=\"content\">")
        rows.append(f"<br><table><tr><th>APEX Domains</th></tr>")

        for domain in domain_count:
            rows.append(f"<tr><td>{domain}</td></tr>")

        rows.append(f"</table></div><br><br><button type=\"button\" class=\"collapsible\">LINKS</button>")
        rows.append(f"<div class=\"content\">")
        rows.append(f"<br><table><tr><th>Domains</th></tr>")

        for link in links:
            rows.append(f"<tr><td>{link}</td></tr>")

        rows.append(f"</table></div>")
        rows.append(f"<h2>HTTP</h2>")
        rows.append(f"<table><tr><th>{urls_http} HTTP Transactions</th></tr>")

        for http in url_count:
            rows.append(f"<tr><td>{http}</td></tr>")

        rows.append(f"</table></div>")
        rows.append(f"<script>")
        rows.append(f"var coll = document.getElementsByClassName(\"collapsible\");")
        rows.append(f"var i;")
        rows.append(f"for (i = 0; i < coll.length; i++) {{")
        rows.append(f"coll[i].addEventListener(\"click\", function() {{")
        rows.append(f"this.classList.toggle(\"active\");")
        rows.append(f"var content = this.nextElementSibling;")
        rows.append(f"if (content.style.display === \"block\") {{")
        rows.append(f"content.style.display = \"none\";")
        rows.append(f"}} else {{")
        rows.append(f"content.style.display = \"block\";")
        rows.append(f"}}")
        rows.append(f"}});")
        rows.append(f"}}")
        rows.append(f"</script><br>")

    else:
        rows = [content,
                "<div id=\"URLScanIO\" class=\"tabcontent\">"
                "<h2>", page_domain, "</h2>"
                "<b>IP Address:</b>", page_ip, "<br>"
                "<b>Effective URL:</b><font color=#008000><i>", page_url, "</i></font>"
                "<h2>Summary</h2>"
                "This website contacted <b>", ips, "IPs</b> in <b>", country_count, "countries </b> across <b>", domains, "domains</b> to perform <b>", urls_http, "HTTP transactions</b>."
                "This main IP is <font color=#008000><b>", page_ip, "</b></font>located in <b>", page_city, "</b><b>", page_country, "</b> and belongs to <font color=#008000><b>", page_asnname, "</b></font>.<br>" 
                "The main domain is <font color=#008000><b>", page_domain, "</b></font>."
                ""
                "<br><br><font size=5> urlscan.<font color=#008000>io</font> Verdict:", verdict, "</font><br><br>"
                "Targeting these brands:", brands, "<br>"
                ""
                "<h2>Screenshot</h2>"
                "<img src=\"", sshot_link, "\" alt=\"URLScan Screenhot\" width=\"600\" height=\"444\" border=\"1px\">"
                "<br>"
                "<h2>Domain & IP Information</h2>"
                "<button type=\"button\" class=\"collapsible\">IP ADDRESS</button>"
                "<div class=\"content\">"
                "<br><table><tr><th>IP Address</th></tr>"]

        for ip in ip_count:
            rows.append(f"<tr><td>{ip}</td></tr>")

        rows.append(f"</table></div><br><br><button type=\"button\" class=\"collapsible\">DOMAINS</button>")
        rows.append(f"<div class=\"content\">")
        rows.append(f"<br><table><tr><th>APEX Domains</th></tr>")

        for domain in domain_count:
            rows.append(f"<tr><td>{domain}</td></tr>")

        rows.append(f"</table></div><br><br><button type=\"button\" class=\"collapsible\">LINKS</button>")
        rows.append(f"<div class=\"content\">")
        rows.append(f"<br><table><tr><th>Domains</th></tr>")

        for link in links:
            rows.append(f"<tr><td>{link}</td></tr>")

        rows.append(f"</table></div>")
        rows.append(f"<h2>HTTP Transactions</h2>")
        rows.append(f"<table><tr><th>{secureRequests} HTTP Transactions</th></tr>")

        for http in url_count:
            rows.append(f"<tr><td>{http}</td></tr>")

        rows.append(f"</table></div>")
        rows.append(f"<script>")
        rows.append(f"var coll = document.getElementsByClassName(\"collapsible\");")
        rows.append(f"var i;")
        rows.append(f"for (i = 0; i < coll.length; i++) {{")
        rows.append(f"coll[i].addEventListener(\"click\", function() {{")
        rows.append(f"this.classList.toggle(\"active\");")
        rows.append(f"var content = this.nextElementSibling;")
        rows.append(f"if (content.style.display === \"block\") {{")
        rows.append(f"content.style.display = \"none\";")
        rows.append(f"}} else {{")
        rows.append(f"content.style.display = \"block\";")
        rows.append(f"}}")
        rows.append(f"}});")
        rows.append(f"}}")
        rows.append(f"</script>")

    write_to_file(filename=f'{filename}_{target}.html', rows=rows)

    with open(f'output/{res}', "r", encoding='utf-8') as f:
        lines = f.readlines()
        with open(f'output/{res}', "w", encoding='utf-8') as f:
            for line in lines:
                f.write(re.sub(r'<td></td></tr><!--URLScanIO-->', f"<td>urlscan.<font color=#008000>io</font> Verdict: {verdict}</td></tr>", line))

    with open(f'output/{res}', "r") as f:
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