__author__ = 'wlarson'

import requests
import re
import math
import os
import csv
import sys

def scrapeSearch(ref, classNum, patentNum):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    #classNum = classNum.replace('/', '%2F')

    if ref == 'c':
        #urlSize = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&d=PTXT&S1=(' + str(classNum) + '%2F$.CCLS.+AND+%40PD%3E%3D19940101%3C%3D20061231)&Page=Next&OS=ccl/' + str(classNum) + '/$+and+isd/1/1/1994-%3E12/31/2006&RS=(CCL/' + str(classNum) + '/$+AND+ISD/19940101-%3E20061231)'
        urlSize = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=ccl%2F' + classNum + '&d=PTXT'
        directory1 = "class" + str(classNum)
        directory2 = 'class' + str(classNum) + 'classresults'
    if ref == 'p':
        urlSize = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&d=PTXT&S1=' + patentNum + '.UREF.&Page=Next&OS=ref/' + patentNum + '&RS=REF/' + patentNum
        directory1 = "class" + str(classNum)
        directory2 = 'class' + str(classNum) + 'refresults'

    while True:
        try:
            pageSize = requests.get(urlSize, timeout=60)
            break
        except requests.exceptions.RequestException as e:
            print('Try again')
            pass

    sizeHTML = pageSize.text
    sizeString = re.findall(r'out of \<strong.*$', sizeHTML, re.MULTILINE)
    singleString = re.findall(r'URL=.*$', sizeHTML, re.MULTILINE)
    urlSingle = ''
    if singleString:
        oneString = ''
        for b in singleString:
            oneString = oneString + b
        oneString = oneString.replace('URL=', '')
        oneString = oneString.replace('">', '')
        urlSingle = 'http://patft.uspto.gov' + oneString
    size = ''
    for x in sizeString:
        size = size + x
    size = size.replace('out of <strong>','')
    size = size.replace('</strong>','')
    if size:
        size = int(size)
    elif singleString:
        size = 1
    else:
        size = 0
    pages = math.ceil(size/50)
    if ref =='c':
        print(size)

    j = 1
    limit = pages
    while j<=limit:
        if ref == 'c':
            #url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=' + str(j) + '&f=S&l=50&d=PTXT&S1=(' + str(classNum) + '%2F$.CCLS.+AND+%40PD%3E%3D19940101%3C%3D20061231)&Page=Next&OS=ccl/' + str(classNum) + '/$+and+isd/1/1/1994-%3E12/31/2006&RS=(CCL/' + str(classNum) + '/$+AND+ISD/19940101-%3E20061231)'
            url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=ccl%2F' + classNum + '&RS=CCL%2F' + classNum + '&Query=ccl%2F' + classNum + '&TD=3825&Srch1=' + classNum + '.CCLS.&NextList' + str(j) + '=Next+50+Hits'
            filename = 'class' + str(classNum) + 'results' + str(j) +'.html'
            print(str(j),' saved')
        if ref == 'p':
            url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=' + str(j) + '&f=S&l=50&d=PTXT&S1=' + patentNum + '.UREF.&Page=Next&OS=ref/' + patentNum + '&RS=REF/' + patentNum
            if urlSingle:
                url = urlSingle
            filename = 'ref' + patentNum + 'results' + str(j) +'.html'

        while True:
            try:
                page = requests.get(url)
                break
            except requests.exceptions.RequestException as e:
                print('Try again')
                pass

        resultsHTML = page.text

        dest_dir = os.path.join(script_dir, directory1, directory2)
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass # already exists
        path = os.path.join(dest_dir, filename)
        html_file = open(path, 'w')
        html_file.write(resultsHTML)
        html_file.close()
        j += 1

    return size

def classList(classNum, limit):

    outFileName = 'class' + str(classNum) + 'list.csv'
    classDir = 'class' + str(classNum)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, classDir)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass # already exists

    outFileName = os.path.join(dest_dir, outFileName)
    writer = open(outFileName, 'w', newline='')
    writerr = csv.writer(writer)

    j = 1
    i = 1
    while j <= limit:
        htmlfilename = 'class' + str(classNum) + 'results' + str(j) + ".html"

        html_dir = os.path.dirname(os.path.abspath(__file__))
        html_dir = os.path.join(html_dir, 'class' + str(classNum), 'class' + str(classNum) + 'classresults', htmlfilename)

        resultsFile = open(html_dir, 'r')
        resultsHTML = resultsFile.read()

        class1P = re.findall(r'\d\,\d\d\d\,\d\d\d', resultsHTML)
        class1RE = re.findall(r'RE\d\d\,\d\d\d', resultsHTML)
        class1D = re.findall(r'D\d\d\d\,\d\d\d', resultsHTML)
        class1H = re.findall(r'H\d\,\d\d\d', resultsHTML)

        for y in class1P:
            y = y.replace(',','')
            data = [i,y]
            writerr.writerow(data)
            i += 1
        for y in class1RE:
            y = y.replace(',','')
            data = [i,y]
            writerr.writerow(data)
            i += 1
        for y in class1D:
            y = y.replace(',','')
            data = [i,y]
            writerr.writerow(data)
            i += 1
        for y in class1H:
            y = y.replace(',','')
            data = [i,y]
            writerr.writerow(data)
            i += 1

        j += 1

    writer.close()

def classRefs(classNum, classSize):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    reader_filename = 'class' + str(classNum) + 'list.csv'
    reader_filename = os.path.join(script_dir, 'class' + str(classNum), reader_filename)

    writer_filename = 'class' + str(classNum) + 'listnums.csv'
    writer_filename = os.path.join(script_dir, 'class' + str(classNum), writer_filename)

    reader = open(reader_filename, 'r')
    reader = csv.reader(reader)
    reader = list(reader)

    writer = open(writer_filename, 'w')
    writer.close()

    j = 1 #3476 change this number if stopped - also change the filename!!!
    while j <= classSize:
        patentNum = reader[j-1][1]
        size = scrapeSearch('p', classNum, patentNum)
        data = [j, patentNum, int(size)]
        writer = open(writer_filename, 'a+')
        writerr = csv.writer(writer, delimiter=',', lineterminator='\n')
        writerr.writerow(data)
        writer.close()
        print(str(j)+ ' loaded')
        j += 1

def refNumbers(classNum, classSize):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reader_filename = 'class' + str(classNum) + 'listnums.csv'
    reader_filename = os.path.join(script_dir, 'class' + str(classNum), reader_filename)

    writer_filename = 'class' + str(classNum) + 'refs.csv'
    writer_filename = os.path.join(script_dir, 'class' + str(classNum), writer_filename)

    reader = open(reader_filename, 'r')
    reader = csv.reader(reader)
    reader = list(reader)

    writer = open(writer_filename, 'w')
    writer = csv.writer(writer)

    j = 1
    while j<= classSize:
        patentNum = reader[j-1][1]
        totRefs = reader[j-1][2]
        totRefs = int(totRefs)

        numRefs = math.ceil(totRefs/50)

        if numRefs == 0:
            data = [j, patentNum, 'NA']
            writer.writerow(data)

        i = 1
        while i <= numRefs:
            htmlfilename = 'ref' + patentNum + 'results' + str(i) + ".html"

            html_dir = os.path.dirname(os.path.abspath(__file__))
            html_dir = os.path.join(html_dir, 'class' + str(classNum), 'class' + str(classNum) + 'refresults', htmlfilename)

            resultsFile = open(html_dir, 'r')
            resultsHTML = resultsFile.read()

            if totRefs == 1:

                singleNum = re.findall(r'<TITLE>.*$', resultsHTML, re.MULTILINE)
                singleP = ''
                for d in singleNum:
                    singleP = singleP + d

                singleP = singleP.replace('<TITLE>United States Patent: ', '')
                singleP = singleP.replace('</TITLE></HEAD>', '')
                data = [j, patentNum, singleP]
                writer.writerow(data)
            else:
                classP = re.findall(r'\d\,\d\d\d\,\d\d\d', resultsHTML)
                classRE = re.findall(r'RE\d\d\,\d\d\d', resultsHTML)
                classD = re.findall(r'D\d\d\d\,\d\d\d', resultsHTML)
                classH = re.findall(r'H\d\,\d\d\d', resultsHTML)

                for y in classP:
                    y = y.replace(',','')
                    data = [j, patentNum,y]
                    writer.writerow(data)
                for y in classRE:
                    y = y.replace(',','')
                    data = [j, patentNum,y]
                    writer.writerow(data)
                for y in classD:
                    y = y.replace(',','')
                    data = [j, patentNum,y]
                    writer.writerow(data)
                for y in classH:
                    y = y.replace(',','')
                    data = [j, patentNum,y]
                    writer.writerow(data)

            i += 1
        j += 1

def getPatents(classNum):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    readerP_filename = 'class' + str(classNum) + 'listnums.csv'
    readerP_filename = os.path.join(script_dir, 'class' + str(classNum), readerP_filename)

    readerP = open(readerP_filename, 'r')
    readerP = csv.reader(readerP)
    readerP = list(readerP)

    classSize = len(readerP)
    print(classSize)

    j = 1 #change this number if it breaks
    while j <= classSize:
        patentNum = readerP[j-1][1]

        if re.findall(r'H',patentNum):
            patentNum = patentNum.replace('H','H00')

        urlP = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=1&p=1&f=G&l=50&d=PTXT&S1=' + str(patentNum) + '.PN.&OS=pn/' + str(patentNum) + '&RS=PN/' + str(patentNum)

        while True:
            try:
                pageP = requests.get(urlP, timeout=60)
                break
            except requests.exceptions.RequestException as e:
                print('Try again')
                pass

        htmlP = pageP.text

        dirP = os.path.join(script_dir, 'class' + str(classNum), 'class' + str(classNum) + 'patents')
        fileP = 'patent' + str(patentNum) + '.html'

        try:
            os.makedirs(dirP)
        except OSError:
            pass # already exists

        pathP = os.path.join(dirP, fileP)
        html_fileP = open(pathP, 'w')
        html_fileP.write(htmlP)
        html_fileP.close()
        print(str(j), " saved")
        j += 1

def getRefs(classNum):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    readerR_filename = 'class' + str(classNum) + 'refs.csv'
    readerR_filename = os.path.join(script_dir, 'class' + str(classNum), readerR_filename)

    readerR = open(readerR_filename, 'r')
    readerR = csv.reader(readerR)
    readerR = list(readerR)
    totalRefs = len(readerR)
    print('Patents to download: ', totalRefs)

    i = 1
    while i <= totalRefs:
        refNum = readerR[i-1][2]
        if refNum == 'NA':
            print(str(i), ' NA')
            i += 1
            continue

        urlR = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=1&p=1&f=G&l=50&d=PTXT&S1=' + str(refNum) + '.PN.&OS=pn/' + str(refNum) + '&RS=PN/' + str(refNum)

        while True:
            try:
                pageR = requests.get(urlR, timeout=60)
                break
            except requests.exceptions.RequestException as e:
                print('Try again')
                pass

        htmlR = pageR.text

        dirR = os.path.join(script_dir, 'class' + str(classNum), 'class' + str(classNum) + 'refs')
        fileR = 'ref' + str(refNum) + '.html'
        try:
            os.makedirs(dirR)
        except OSError:
            pass
        pathR = os.path.join(dirR, fileR)
        html_fileR = open(pathR, 'w')
        html_fileR.write(htmlR)
        html_fileR.close()
        print(str(i), " saved: ", refNum)

        i += 1

def patentList(classNum):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reader_filename = 'class' + str(classNum) + 'listnums.csv'
    reader_filename = os.path.join(script_dir, 'class' + str(classNum), reader_filename)

    writer_filename = 'class' + str(classNum) + 'patents.csv'
    writer_filename = os.path.join(script_dir, 'class' + str(classNum), writer_filename)

    reader = open(reader_filename, 'r')
    reader = csv.reader(reader)
    reader = list(reader)
    classSize = len(reader)

    writer = open(writer_filename, 'w')
    writercsv = csv.writer(writer)
    data = ['j', 'Patent num', 'Title', 'Assignee(s)', 'Publication date', 'File date', 'Abstract']
    writercsv.writerow(data)

    j = 1
    while j<= classSize: #classSize
        patentNum = reader[j-1][1]
        #patentNum = str(8653917)
        print(j)
        #print(patentNum)

        htmlfilename = 'patent' + patentNum + ".html"
        html_dir = os.path.dirname(os.path.abspath(__file__))
        html_dir = os.path.join(html_dir, 'class' + str(classNum), 'class' + str(classNum) + 'patents', htmlfilename)

        resultsFile = open(html_dir, 'r')
        resultsHTML = resultsFile.read()

        ti = re.findall(r'<FONT size=\"\+1\".*?</FONT>', resultsHTML, re.DOTALL)
        title = ''
        for i in ti:
            title = title + i
        title = title.replace('<FONT size="+1">', '')
        title = title.replace('</FONT>', '')
        title = title.replace('\n', '')
        title = title.replace('    ','')
        #print(title)

        assig = re.findall(r'Assignee.*?</TD>', resultsHTML, re.DOTALL)
        if assig:
            assig = assig[0]
        assignee = ''
        for i in assig:
            assignee = assignee + i
        assignee = assignee.replace('Assignee:</TH>', '')
        assignee = assignee.replace('\n','')
        assignee = assignee.replace('<TD align="left" width="90%">', '')
        assignee = assignee.replace('<B>','')
        assignee = assignee.replace('</B>', '')
        assignee = assignee.replace('<BR>', '; ')
        assignee = assignee.replace('</TD>', '')
        if not assignee:
            assignee = 'NA'
        #print(assignee)

        pdate = re.findall(r'United States Patent </b>.*?</TABLE>', resultsHTML, re.DOTALL)
        pubdate = ''
        for i in pdate:
            pubdate = pubdate + i
        pubdate = re.findall(r'^.*\d\,\s\d\d\d\d', pubdate, re.MULTILINE)
        pubdate = pubdate[0]
        pubdate = pubdate.lstrip()
        #print(pubdate)

        fdate = re.findall(r'Filed:.*?</TD>', resultsHTML, re.DOTALL)
        fdate = fdate[0]
        filedate = ''
        for i in fdate:
            filedate = filedate + i
        filedate = re.findall(r'^.*\d\,\s\d\d\d\d', filedate, re.MULTILINE)
        filedate = filedate[0]
        filedate = filedate.lstrip()
        filedate = filedate.replace('<b>', '')
        #print(filedate)

        ab = re.findall(r'Abstract.*?</p>', resultsHTML, re.DOTALL)
        abstract = ''
        for i in ab:
            abstract = abstract + i
        abstract = re.findall(r'<p>.*</p>', abstract, re.DOTALL)
        if abstract:
            abstract = abstract[0]
            abstract = abstract.replace('<p>', '')
            abstract = abstract.replace('</p>', '')
            abstract = abstract.replace('\n',' ')
            abstract = abstract.replace('      ',' ')
            abstract = abstract.lstrip()
        else:
            abstract = 'NA'
        #print(abstract)

        data = [j, patentNum, title, assignee, pubdate, filedate]
        writercsv.writerow(data)

        j += 1

    writer.close()

def refList(classNum):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reader_filename = 'class' + str(classNum) + 'refs.csv'
    reader_filename = os.path.join(script_dir, 'class' + str(classNum), reader_filename)

    writer_filename = 'class' + str(classNum) + 'refspatents.csv'
    writer_filename = os.path.join(script_dir, 'class' + str(classNum), writer_filename)

    reader = open(reader_filename, 'r')
    reader = csv.reader(reader)
    reader = list(reader)
    classSize = len(reader)

    writer = open(writer_filename, 'w')
    writercsv = csv.writer(writer)
    data = ['j', 'Patent num', 'Citing patent', 'Title', 'Assignee(s)', 'Publication date', 'File date', 'Abstract']
    writercsv.writerow(data)

    j = 1
    while j<= classSize: #classSize
        patentNum = reader[j-1][2]
        citingNum = reader[j-1][1]
        #patentNum = str(8653917)
        k = j % 1000
        if k == 0:
            print(j)

        if patentNum == 'NA':
            data = [j, 'No forward cites', citingNum]
            writercsv.writerow(data)
            j += 1
            continue

        htmlfilename = 'ref' + patentNum + ".html"
        html_dir = os.path.dirname(os.path.abspath(__file__))
        html_dir = os.path.join(html_dir, 'class' + str(classNum), 'class' + str(classNum) + 'refs', htmlfilename)

        resultsFile = open(html_dir, 'r')
        resultsHTML = resultsFile.read()

        ti = re.findall(r'<FONT size=\"\+1\".*?</FONT>', resultsHTML, re.DOTALL)
        title = ''
        for i in ti:
            title = title + i
        title = title.replace('<FONT size="+1">', '')
        title = title.replace('</FONT>', '')
        title = title.replace('\n', '')
        title = title.replace('    ','')
        #print(title)

        assig = re.findall(r'Assignee.*?</TD>', resultsHTML, re.DOTALL)
        if assig:
            assig = assig[0]
        assignee = ''
        for i in assig:
            assignee = assignee + i
        assignee = assignee.replace('Assignee:</TH>', '')
        assignee = assignee.replace('\n','')
        assignee = assignee.replace('<TD align="left" width="90%">', '')
        assignee = assignee.replace('<B>','')
        assignee = assignee.replace('</B>', '')
        assignee = assignee.replace('<BR>', '; ')
        assignee = assignee.replace('</TD>', '')
        if not assignee:
            assignee = 'NA'
        #print(assignee)

        pdate = re.findall(r'United States Patent </b>.*?</TABLE>', resultsHTML, re.DOTALL)
        pubdate = ''
        for i in pdate:
            pubdate = pubdate + i
        pubdate = re.findall(r'^.*\d\,\s\d\d\d\d', pubdate, re.MULTILINE)
        pubdate = pubdate[0]
        pubdate = pubdate.lstrip()
        #print(pubdate)

        fdate = re.findall(r'Filed:.*?</TD>', resultsHTML, re.DOTALL)
        fdate = fdate[0]
        filedate = ''
        for i in fdate:
            filedate = filedate + i
        filedate = re.findall(r'^.*\d\,\s\d\d\d\d', filedate, re.MULTILINE)
        filedate = filedate[0]
        filedate = filedate.lstrip()
        filedate = filedate.replace('<b>', '')
        #print(filedate)

        ab = re.findall(r'Abstract.*?</p>', resultsHTML, re.DOTALL)
        abstract = ''
        for i in ab:
            abstract = abstract + i
        abstract = re.findall(r'<p>.*</p>', abstract, re.DOTALL)
        if abstract:
            abstract = abstract[0]
            abstract = abstract.replace('<p>', '')
            abstract = abstract.replace('</p>', '')
            abstract = abstract.replace('\n',' ')
            abstract = abstract.replace('      ',' ')
            abstract = abstract.lstrip()
        else:
            abstract = 'NA'
        #print(abstract)

        data = [j, patentNum, citingNum, title, assignee, pubdate, filedate]
        writercsv.writerow(data)

        j += 1

    writer.close()
