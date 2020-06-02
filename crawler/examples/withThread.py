from urllib.request import urlopen
from time import time
from threading import Thread
from queue import Queue

sira = Queue()

siteler = ("http://www.python.org",
           "http://yasararabaci.tumblr.com",
           "http://metehan.us",
           "http://bilgisayarkavramlari.sadievrenseker.com/",
           "https://www.google.com/search/howsearchworks/crawling-indexing/")

def site_okuyan(que):
    while True:
        site = que.get()
        print(site)
        source = urlopen(site)
        _ = source.read()
        source.close()
        que.task_done()


if __name__ == "__main__":
    basla = time()
    for i in range(5):
        t = Thread(target=site_okuyan, args=(sira,))
        t.daemon = True
        t.start()

    for site in siteler:
        sira.put(site)

    sira.join()
    print("%s saniye sürdü " % (time() - basla))
