import pdfkit
import re
from pathlib import Path


def convert2pdf_url_or_ip(url_or_ip: str, output_filename: str) -> None:
    # configuration for wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # source URL or IP address
    target = url_or_ip

    # output file name
    filename = f'{output_filename}'
    output = f'{filename}_{target}'

    # remove special character
    res = re.sub("[://|?]", "", output)

    final_output = re.search(r"([\w\-\.]+\.\w\w)", res)
    final_res = final_output.group(0)

    path = Path(f'output/{final_res}.html')

    if path.is_file():
        # convert html output to PDF format
        pdfkit.from_file(f'output/{final_res}.html', f'output/{final_res}.pdf', configuration=config)
    else:
        return


def convert2pdf_hash(hash_str: str, output_filename: str) -> None:
    # configuration for wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # source hash
    target = hash_str

    # output file name
    filename = f'{output_filename}'
    output = f'{filename}_{target}'

    # remove special character
    res = re.sub("[://|?]", "", output)

    final_res = output

    path = Path(f'output/{final_res}.html')

    if path.is_file():
        # convert html output to PDF format
        pdfkit.from_file(f'output/{final_res}.html', f'output/{final_res}.pdf', configuration=config)
    else:
        return
