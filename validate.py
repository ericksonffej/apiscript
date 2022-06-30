import re


def check_hash(hsh):
    if is_hash(hsh):
        return hsh
    else:
        print("[+] Error: The Hash input does not appear valid.")
        exit(1)


def check_vt_url(url):
    # TODO: validate url
    if is_url(url):
        return url
    else:
        print("[+]  Error: The URL input does not appear valid.")
        exit(1)


def check_vt_ip(ip):
    # TODO: validate ip
    if is_ip(ip):
        return ip
    else:
        print("[+] Error: The IP address input does not appear valid.")
        exit(1)


def is_hash(target):
    if len(target) == 32:
        if re.findall(r"([a-fA-F\d]{32})", target):
            return True
    elif len(target) == 40:
        if re.findall(r"([a-fA-F\d]{40})", target):
            return True
    elif len(target) == 64:
        if re.findall(r"([a-fA-F\d]{64})", target):
            return True
    else:
        return False


def is_url(target):
    # validate url
    if re.findall(
            r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s("
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
            target):
        return True
    elif re.findall(r"([\w\-\.]+)", target):
        return True
    else:
        return False


def is_ip(target):
    # validate ip address
    if re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", target):
        return True
    else:
        return False
