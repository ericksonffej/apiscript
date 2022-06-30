# API SCRIPT FOR OSINT ANALYSIS
This project allows getting HTML and PDF reports using API-OSINT Automater. Using this tool we can check the reputation of IPAddress, Domains, Urls, and Hashes from the famous and well known Threat Intelligence websites.


## Supported OSINT Tools:
* Virus Total
* AbuseIPDB
* URLScanIO
* ShodanIO
* IBM X-Force
* GreyNoise


## Script Execution 

$ python main.py -h <br/>
usage: main.py &nbsp;[-h] &nbsp; -T TICKET &nbsp;[-H HASH]&nbsp; [-U URL]&nbsp; [-IP IP_ADDRESS] &nbsp;[-F FILE]

| ARGS | ARGS         | HELP                                                  |
|------|--------------|-------------------------------------------------------|
| -h   | --help       | show this help message and exit                       |
| -T   | --ticket     | Reference ticket, output file name                    |
| -H   | --hash       | Single Hash example: 6a8401448a5bd2b540850f811b20a66d |
| -U   | --url        | URL or website example: www.17ebook.com               |
| -IP  | --ip-address | IP Address example: 192.168.1.1                       |
| -F   | --file       | File input example "input.txt"                        |


## Output: 
- PDF
- HTML