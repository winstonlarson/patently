__author__ = 'wlarson'

import scraper
import math

patentClasses = ['707%2F999.101', '707%2F999.202', '707%2FE17.006', '707%2F602', '707%2F791', '707%2F804', '707%2F809']
sizes = [3825, 4507, 0, 0, 0, 0, 0]
lengths = []
for row in sizes:
    lengths.append(math.ceil(row/50))

#size101 = 3825
#length101 = math.ceil(size101/50)
#s = scraper.scrapeSearch('c', patentClasses[1], 1)
#length200 = math.ceil(size200/50)

#scraper.classList(patentClasses[1], lengths[1]) # outputs class361list.csv - list of patents in a class
#scraper.classRefs(patentClasses[1], sizes[1]) # downloads the html files for forward reference search results (class361refresults)
#scraper.refNumbers(patentClasses[1], sizes[1]) # outputs class361refs.csv - list of patents matched to forward references
#scraper.getPatents(patentClasses[1]) # downloads the html files for class patents
#scraper.getRefs(patentClasses[0]) # downloads the html files for the forward reference patents
#scraper.patentList(patentClasses[0]) # outputs class361patents.csv - list of patents with information
scraper.refList(patentClasses[0])
