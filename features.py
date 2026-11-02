import re
from urllib.parse import urlparse

WORDS = ["login", "verify", "update", "secure", "bank", "account", "free"]

def features(url):
    try:
        p = urlparse(url if "://" in url else "http://" + url)
        host, scheme = p.netloc, p.scheme
    except ValueError:
        host, scheme = "", ""
    return {
        "length": len(url),
        "host_length": len(host),
        "dots": url.count("."),
        "hyphens": url.count("-"),
        "at": int("@" in url),
        "digits": sum(c.isdigit() for c in url),
        "slashes": url.count("/"),
        "has_ip": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host.split(":")[0]))),
        "https": int(scheme == "https"),
        "subdomains": max(host.count(".") - 1, 0),
        "bad_words": sum(w in url.lower() for w in WORDS),
    }