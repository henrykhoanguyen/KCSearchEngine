''' Group 3 '''
import json
import re, time
import math
from collections import defaultdict
from lxml import html

freq = {}
index = defaultdict(list)


def parse_for_content( ):
    f = open("WEBPAGES_RAW/bookkeeping.json")
    #reads data from file
    data = json.load(f)
    f.close()
    i = 0
    for file_path in data:
        #if i < 20:
            #print(file_path)
        folder = (file_path.split('/', 1)[0])
        file_name = (file_path.split('/', 1)[1])
        f = open("WEBPAGES_RAW/%s/%s" % (folder, file_name))
        html_content = f.read()
        try:
            #parses doc, creating html doc, returns text content
            parsed = html.fromstring(html_content).text_content().lower()
            #tokenize each word in parsed html content
            tokenize(parsed, file_path)
            freq.clear()
        except html.etree.ParserError:
            pass
        f.close()
            #i += 1
    #writing index to file
    '''with open('inverted_index_mine.txt', 'w') as the_file:
        for i, o in index.iteritems():
            the_file.write(str(i) + " - ")
            for x in o:
                the_file.write(str(x) + " ")
            the_file.write("\n")

    the_file.close()'''
    return data


''' Tokenize Function tokenizes words and find TF'''
def tokenize(f, file_path):
    ''' use regex to get token '''
    regex = re.compile("([a-zA-Z]+)")
    words = re.findall(regex, f.lower())

    ''' Count term frequency '''
    for i in words:
        if i not in freq:
            freq[i] = 0
        freq[i] += 1

    ''' Insert word into dictionary with docId and weighted TF '''
    for term in freq:
        docId = {file_path: (1 + math.log10(freq[term]))}
        index[term].append(docId)


def sortSecond(posting_list):
    #posting_list contains doc ids & corresponding weight
    for docId in posting_list:
        #the weight
        return posting_list[docId]


def weighting(data):
    #number of documents in the corpus
    doc_len = len(data)
    for term in index:
        #index[term]: doc id & frequency 
        for document in index[term]:
            ''' Calculate idf '''
            #number of docs/number of docs containing specified term
            idf = math.log10(doc_len / len(index[term]))
            ''' Calculate tf_idf weight scheme '''
            for docId in document:
                tf_idf = document[docId] * idf
                document[docId] = tf_idf
        #sort by descending weight
        index[term].sort(key=sortSecond, reverse=True)

    '''with open('weighted_index.txt', 'w') as the_file:
        for i, o in index.iteritems():
            the_file.write(str(i) + " - ")
            for x in o:
                the_file.write(str(x) + " ")
            the_file.write("\n")

    the_file.close()'''


def search():
    token = raw_input("Enter term to search for: ").lower()

    while token != "!!!":
        startTime = time.time()
        ''' use regex to get token '''
        regex = re.compile("([a-zA-Z]+)")
        words = re.findall(regex, token)
        #holds doc id, weight
        posting_list = []
        url = []

        ''' Get Documents from Query '''
        #breaks token up into seperate words
        for tkn in words:
            if index.get(tkn) is not None:
                posting_list.extend(index.get(tkn))
        ''' Get Links from Document '''
        if len(posting_list) > 0:
            #sort by descending weight
            posting_list.sort(key=sortSecond, reverse=True)
            counter = 1
            results = []
            for doc in posting_list:
                #gets doc id out from list
                doc_id = doc.keys().pop()

                if url.count(data.get(doc_id)) < 1:
                    url.append(data.get(doc_id))
                    print counter, " - ", str(data.get(doc_id))
                    counter += 1
                if counter > 10:
                    break
        else:
            print("No Result!")

        elapsedTime = time.time() - startTime
        print("Search Time: %f seconds" % elapsedTime)
        token = raw_input("Enter term to search for: ").lower()


if __name__ == '__main__':
    print("Building the index (this may take a few minutes...)")
    data = parse_for_content()
    print("Finish building index...")
    print("Calculating weight scheme tf-idf...")
    weighting(data)
    search()









