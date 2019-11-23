from bs4 import BeautifulSoup
import requests
import os
url = ''
def createProjectDirectory():
    path = input('Enter Project Name : ')
    try:
        os.mkdir(path)
        indexFile = open(f'{path}\\index.html', 'w+', encoding="utf-8")
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the project directory %s " % path)
    getIndexHtml(indexFile, path)

def getIndexHtml(indexFile, path):          
    global url
    url = 'https://shawinc.com/'
    r = requests.get(url)
    content = BeautifulSoup(r.content, "html5lib")
    indexFile.write(str(content))
    findAllAnchors(content, path)

def findAllAnchors(content, path):
    allAnchors = content.find_all('a')
    storeHrefs(allAnchors, path)

def storeHrefs(allAnchors, path):
    hrefs = []
    for i in allAnchors:
        if i.has_attr('href'):
            hrefs.append(i['href'])
    print('Hrefs are collected.')
    hrefs = list(dict.fromkeys(hrefs))
    print(hrefs)
    makingFilesFromHrefs(hrefs, path)

def makingFilesFromHrefs(hrefs, path):
    for i in hrefs:
        if i == '/' or '/' not in i:
            continue
        if i[0:5] == 'https' or i[0:4] == 'http':
            continue
        count = countSlashes(i)
        if count == 1:
            fileName = i[1:] + '.html'
            file = makeHtmlFile(fileName, path)
            newUrl = url + i
        if count == 2 and i[-1] == '/':
            fileName = i[1:-1] + '.html'
            file = makeHtmlFile(fileName, path)
        else :
            makeFoldersandFiles(i, path)

def countSlashes(i):
    count = 0
    for letter in i:
        if letter == '/':
            count = count + 1
    return count

def makeFoldersandFiles(i, path):
    if i[-1] == '/':
        i = i[0:-1]
    sortStr = i.split('/')
    sortStr[-1] = sortStr[-1] + '.html'
    for j in sortStr:
        if '.' not in j:
            path = path + '\\'+j
        if j == '':
            continue
        if j == sortStr[-1]:
            createSubDirectories(path)
            makeHtmlFile(j, path)

def makeHtmlFile(fileName, path):
    try:
        file = open(f'{path}\\{fileName}', 'w+')
        return file
    except OSError:
        print("Creation of the directory %s failed" % path)

def createSubDirectories(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the sub-directory %s failed" % path)


createProjectDirectory()
# getIndexHtml()