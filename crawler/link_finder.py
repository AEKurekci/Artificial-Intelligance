from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url):
        super().__init__()
        self.baseURL = base_url
        self.pageURL = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (attribute, value) in attrs:
                if attribute == "href":
                    url = parse.urljoin(self.baseURL, value)
                    self.links.add(url)

    def allLinks(self):
        return self.links

    def error(self, message):
        print(message)


