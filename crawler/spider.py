from urllib.request import urlopen
from link_finder import LinkFinder
from general import *

class Spider:

    projectName = ""
    baseURL = ""
    domainName = ""
    queueFile = ""
    crawledFile = ""
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.projectName = project_name
        Spider.baseURL = base_url
        Spider.domainName = domain_name
        Spider.queueFile = Spider.projectName + '/queue.txt'
        Spider.crawledFile = Spider.projectName + '/crawled.txt'
        self.boot()
        self.crawlPage('First spider', Spider.baseURL)

    @staticmethod
    def boot():
        createProjectDir(Spider.projectName)
        createDataFiles(Spider.projectName, Spider.baseURL)
        Spider.queue = fileToSet(Spider.queueFile)
        Spider.crawled = fileToSet(Spider.crawledFile)

    @staticmethod
    def crawlPage(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + " now crawling " + page_url + "\n")
            print("Queue " + str(len(Spider.queue)) + " | Crawled " + str(len(Spider.crawled)))
            Spider.addLinksToQueue(Spider.gatherLink(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.updateFiles()

    @staticmethod
    def gatherLink(page_url):
        htmlString = ""
        try:
            response = urlopen(page_url)
            if response.getheader("Content-Type") == "text/html":
                htmlBytes = response.read()
                htmlString = htmlBytes.decode("utf-8")
            finder = LinkFinder(Spider.baseURL, page_url)
            finder.feed(htmlString)
        except:
            print("The page can not crawl")
            return set()
        return finder.allLinks()

    @staticmethod
    def addLinksToQueue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domainName not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def updateFiles():
        setToFile(Spider.queue, Spider.queueFile)
        setToFile(Spider.crawled, Spider.crawledFile)



