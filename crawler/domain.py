from urllib.parse import urlparse


#get domain name (example.com)
def getDomainName(url):
    try:
        results = getSubdomainName(url).split('.')
        return results[-2] + "." + results[-1]
    except:
        return ""


#get subdomain name (mail.example.com)
def getSubdomainName(url):
    try:
        return urlparse(url).netloc
    except:
        return ""
