import os


#create directory if not exists
def createProjectDir(directory):
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.makedirs(directory)


#create queue and crawled files
def createDataFiles(project_name, base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt"
    if not os.path.isfile(queue):
        writeFile(queue, base_url)
    if not os.path.isfile(crawled):
        writeFile(crawled, "")


#create a new file
def writeFile(path, content):
    f = open(path, 'w')
    f.write(content)
    f.close()


#add data onto existing file
def appendToFile(path, data):
    with open(path, 'a') as file:
        file.write(data + "\n")


#delete file contents
def deleteFileContents(path):
    open(path, 'w').close()


#read a file and convert each line to set items
def fileToSet(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


#Iterate through a set, each item will be a new line in the file
def setToFile(links, file):
    deleteFileContents(file)
    for link in sorted(links):
        appendToFile(file, link)



