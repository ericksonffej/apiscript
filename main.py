import argparse
import re
from pathlib import Path
from convert2pdf import convert2pdf_url_or_ip, convert2pdf_hash
from osint_greynoise import get_greynoise_ip
from osint_ibmxforce import get_ibmxforce_ip, get_ibmxforce_url
from osint_shodan import get_shodan_ip_url
from file_util_virustotal import read_file
from osint_abuseipdb import get_abuseipdb_ip
from osint_urlscan import get_urlscan_ip_url
from validate import check_hash, check_vt_url, is_hash, is_ip, is_url
from osint_virustotal import get_vt_hash, get_vt_ip_url

def main():
    parser = argparse.ArgumentParser(description="API SCRIPT Help Check")
    parser.add_argument('-T', '--ticket', required=True,
                        help='Reference ticket, output file name')
    parser.add_argument('-H', '--hash', type=check_hash, required=False,
                        help='Single Hash example: 6a8401448a5bd2b540850f811b20a66d')
    parser.add_argument('-U', '--url', type=check_vt_url, required=False,
                        help='url or website example: www.17ebook.com')
    parser.add_argument('-IP', '--ip-address', type=check_vt_url, required=False,
                        help='IP Address example: 192.168.1.1')
    parser.add_argument('-F', '--file', required=False,
                        help='File input')
    args = parser.parse_args()

    # displayed in GUI
    # print(f'Reference Ticket: {args.ticket}')
    # print("===================================================================================")

    if args.hash:
        print(f'Input HASH: {args.hash}')
        get_vt_hash(hash_str=args.hash, output_filename=args.ticket)
        convert2pdf_hash(hash_str=args.hash, output_filename=args.ticket)
        exit(0)

    if args.url:
        print(f'Input URL: {args.url}')
        get_vt_ip_url(url_or_ip=args.url, output_filename=args.ticket)
        # get_abuseipdb_url(url_or_ip=args.url, output_filename=args.ticket)
        get_urlscan_ip_url(url_or_ip=args.url, output_filename=args.ticket)
        get_ibmxforce_url(url_or_ip=args.url, output_filename=args.ticket)
        convert2pdf_url_or_ip(url_or_ip=args.url, output_filename=args.ticket)
        exit(0)

    if args.ip_address:
        print(f'Input IP Address: {args.ip_address}')
        get_vt_ip_url(url_or_ip=args.ip_address, output_filename=args.ticket)
        get_abuseipdb_ip(url_or_ip=args.ip_address, output_filename=args.ticket)
        get_shodan_ip_url(url_or_ip=args.ip_address, output_filename=args.ticket)
        # get_urlscan_ip_url(url_or_ip=args.ip_address, output_filename=args.ticket)
        get_greynoise_ip(url_or_ip=args.ip_address, output_filename=args.ticket)
        get_ibmxforce_ip(url_or_ip=args.ip_address, output_filename=args.ticket)
        convert2pdf_url_or_ip(url_or_ip=args.ip_address, output_filename=args.ticket)
        exit(0)

    if args.file:
        # READ File input.txt
        input_list = read_file()

        for target in input_list:
            filename = args.ticket
            output = f'{filename}_{target}'
            res = re.sub("[://|?]", "", output)
            final_output = re.search(r"([\w\-\.]+\.\w\w)", res)
            if final_output is None:
                final_res = output
            else:
                final_res = final_output.group(0)

            path = Path(f'output/{final_res}.html')
            print("===================================================================================")
            print(f'Target: {target}')
            # Validation if file already exists
            if path.is_file():
                print('File already exists. Either delete the existing file or use different reference number.')
                return
            if is_hash(target):
                print('[+] Hash found')
                get_vt_hash(hash_str=target, output_filename=args.ticket)
                convert2pdf_hash(hash_str=target, output_filename=args.ticket)
            elif is_ip(target):
                print('[+] IP or URL found')
                get_vt_ip_url(url_or_ip=target, output_filename=args.ticket)
                get_abuseipdb_ip(url_or_ip=target, output_filename=args.ticket)
                get_shodan_ip_url(url_or_ip=target, output_filename=args.ticket)
                # get_urlscan_ip_url(url_or_ip=target, output_filename=args.ticket)
                get_greynoise_ip(url_or_ip=target, output_filename=args.ticket)
                get_ibmxforce_ip(url_or_ip=target, output_filename=args.ticket)
                convert2pdf_url_or_ip(url_or_ip=target, output_filename=args.ticket)
            elif is_url(target):
                print('[+] IP or URL found')
                get_vt_ip_url(url_or_ip=target, output_filename=args.ticket)
                # get_abuseipdb_url(url_or_ip=target, output_filename=args.ticket)
                get_urlscan_ip_url(url_or_ip=target, output_filename=args.ticket)
                get_ibmxforce_url(url_or_ip=target, output_filename=args.ticket)
                convert2pdf_url_or_ip(url_or_ip=target, output_filename=args.ticket)
            else:
                print(f'[+] Error: Skipping invalid format')
        exit(0)

    # No valid inputs like hash, url, ip or file input
    print('[+] Error: Please check arguments.')


if __name__ == "__main__":
    main()
