from urllib.parse import urlparse


#get domain name (example.com)
def getDomainName(url):
    try:
        results = getSubdomainName(url).split('.')
        print("result:", results)
        result = ""
        length = len(results)
        while length > 0:
            if length > 1:
                result += results[-length] + "."
            elif length == 1:
                result += results[-length]
            results.pop(0)
            length -= 1
        print(result)
        return result
    except:
        return ""


#get subdomain name (mail.example.com)
def getSubdomainName(url):
    try:
        return urlparse(url).netloc
    except:
        return ""
