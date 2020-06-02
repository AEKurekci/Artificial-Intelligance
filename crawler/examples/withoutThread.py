from urllib.request import urlopen
from time import time
siteler = ("http://www.python.org",
           "http://yasararabaci.tumblr.com",
           "http://metehan.us",
           "http://bilgisayarkavramlari.sadievrenseker.com/",
           "https://www.google.com/search/howsearchworks/crawling-indexing/")

start = time()
for site in siteler:
    f = urlopen(site)
    _ = f.read()
    f.close()
    print(site)

print("%f saniye surdu" % (time() - start))