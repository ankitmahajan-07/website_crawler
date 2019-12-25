from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import cssutils
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
    url = 'https://www.codegaragetech.com'
    r = requests.get(url)
    content = BeautifulSoup(r.content, "html5lib")
    indexFile.write(str(content))
    findCss(content, path)
    findJs(content,path)
    downloadImages(content, path)
    findAllAnchors(content, path)

def writeIntoFiles(url,file):
    print('creating '+url+' file.')
    r = requests.get(url)
    content = BeautifulSoup(r.content, "html5lib")
    print(str(content))
    file.write(str(content))

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
        print('working on '+i)
        if i == '/' or i[0] == '#':
            continue
        if '/' not in i and i[0:4] != 'http' and i != 'index.html':
            if i[-4:] == 'html':
                newUrl = url +'/'+ i
                print('creating file',i)
                file = makeHtmlFile(i, path, newUrl)
                continue
            else:
                fileName = i[1:] + '.html'
                print('creating file',fileName)
                newUrl = url +'/'+ i
                file = makeHtmlFile(fileName, path, newUrl)
                continue
        if i[0:5] == 'https' or i[0:4] == 'http':
            continue
        count = countSlashes(i)
        if count == 1:
            fileName = i[1:] + '.html'
            newUrl = url + i
            print('creating file', fileName)
            file = makeHtmlFile(fileName, path,newUrl)
            continue

        if count == 2 and i[-1] == '/':
            fileName = i[1:-1] + '.html'
            newUrl = url + i[:-1]
            print('creating file', fileName)
            file = makeHtmlFile(fileName, path,newUrl)
            continue
        else :
            makeFoldersandFiles(i, path)

def countSlashes(i):
    count = 0
    for letter in i:
        if letter == '/':
            count = count + 1
    return count

def makeFoldersandFiles(i, path):
    global url
    if i[-1] == '/':
        i = i[0:-1]
    sortStr = i.split('/')
    if sortStr[-1][-4:] != 'html':
        sortStr[-1] = sortStr[-1] + '.html'
    for j in sortStr:
        if '.' not in j:
            path = path + '\\'+j
        if j == '':
            continue
        if j == sortStr[-1]:
            createSubDirectories(path)
            newUrl = url+ '/'+sortStr[-1]
            print('creating file',j)
            makeHtmlFile(j, path,newUrl)

def makeHtmlFile(fileName, path,url):
    try:
        file = open(f'{path}\\{fileName}', 'w+', encoding="utf-8")
        r = requests.get(url)
        content = BeautifulSoup(r.content, "html5lib")
        file.write(str(content))
        downloadImages(content, path)
        findCss(content,path)
        findJs(content,path)
        return file
    except OSError:
        print("Creation of the directory %s failed" % path)

def createSubDirectories(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the sub-directory %s failed" % path)

def downloadImages(content, path):
    print('Downloading images')
    global url
    imgs = content.find_all("img")
    srcs = []
    for img in imgs:
        raw_src = str(img).split('src="')
        src = raw_src[1].split('"')
        srcs.append(src[0])
    print(srcs)
    for src in srcs:
        if src[0:4] == 'http':
            continue
        else:
            try:
                if src[0] == '/':
                    src = src[1:]
                src = src.replace(' ', '%20')
                mySrc = url + '/' + src
                nameLength = len(src.split('/')[-1])
                newPath = path+'/'+src[0:len(src)-nameLength-1]
                createSubDirectories(newPath)
                fileName = path+'/'+src.replace('%20', ' ')
                print('Downloading ',fileName)
                urllib.request.urlretrieve(mySrc, fileName)
            except:
                # if src[-3:] != 'png' or src[-3:] != 'jpg' or src[-3:] != 'svg' or src[-3:] == 'peg':
                continue

    divs = content.find_all('div')
    for div in divs:
        if div.has_attr('style'):
            try:
                div_style = div['style']
                style = cssutils.parseStyle(div_style)
                src = style['background-image']
                mySrc = url + '/' + src
                nameLength = len(src.split('/')[-1])
                newPath = path + '/' + src[0:len(src) - nameLength - 1]
                createSubDirectories(newPath)
                fileName = path + '/' + src
                print('Downloading ', mySrc)
                urllib.request.urlretrieve(mySrc, fileName)
            except:
                pass

def findCss(content, path):
    global url
    links = content.find_all('link')
    for link in links:
        if link['href'][-4:] == '.css' and link['href'][:4]!='http':
            src = link['href']
            if src[0] == '/':
                src = src[1:]
            mySrc = url + '/' + src
            nameLength = len(src.split('/')[-1])
            newPath = path + '/' + src[0:len(src) - nameLength - 1]
            createSubDirectories(newPath)
            fileName = path + '/' + src
            file = open(f'{fileName}', 'w+', encoding="utf-8")
            r = requests.get(mySrc)
            content = BeautifulSoup(r.content, "html5lib")
            file.write(str(content)[25:-14])
        if link['href'][-4:] == '.png' or link['href'][-4:] == '.jpg':
            src = link['href']
            if src[0] == '/':
                src = src[1:]
            mySrc = url + '/' + src
            nameLength = len(src.split('/')[-1])
            newPath = path + '/' + src[0:len(src) - nameLength - 1]
            createSubDirectories(newPath)
            fileName = path + '/' + src
            urllib.request.urlretrieve(mySrc, fileName)

def findJs(content, path):
    global url
    links = content.find_all('script')
    for link in links:
        try:
            if link['src'][-3:] == '.js' and link['src'][:4]!='http':
                src = link['src']
                if src[0] == '/':
                    src = src[1:]
                mySrc = url + '/' + src
                nameLength = len(src.split('/')[-1])
                newPath = path + '/' + src[0:len(src) - nameLength - 1]
                createSubDirectories(newPath)
                fileName = path + '/' + src
                file = open(f'{fileName}', 'w+', encoding="utf-8")
                r = requests.get(mySrc)
                content = BeautifulSoup(r.content, "html5lib")
                file.write(str(content)[25:-14])
        except:
            continue

createProjectDirectory()
print("Web site has been scraped successfully.")
# getIndexHtml()