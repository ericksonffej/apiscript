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
    output = f'{filename}_{target}.html'

    # remove special character
    res = re.sub("[://|?]", "", output)

    path = Path(f'output/{res}')

    if path.is_file():
        # convert html output to PDF format
        pdfkit.from_file(f'output/{res}', f'output/{res}.pdf', configuration=config)
    else:
        return


def convert2pdf_hash(hash_str: str, output_filename: str) -> None:
    # configuration for wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # source hash
    target = hash_str

    # output file name
    filename = f'{output_filename}'
    output = f'{filename}_{target}.html'

    # remove special character
    res = re.sub("[://|?]", "", output)

    path = Path(f'output/{res}')

    if path.is_file():
        # convert html output to PDF format
        pdfkit.from_file(f'output/{res}', f'output/{res}.pdf', configuration=config)
    else:
        return
