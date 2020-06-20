import xml.etree.ElementTree as ET
import json
dic = {}
def pubmed_preprocess (file_name):
    root = ET.parse(file_name).getroot()

    res = []

    for child in root:
        medlinecitation = child.find('MedlineCitation')
        PMID = medlinecitation.find('PMID').text
    
        article = medlinecitation.find('Article')
        if article:
            temp = article.find('ArticleTitle').itertext()
            articletitle = ''
            for i in temp:
                articletitle += i
        else:
            articletitle = ''
    
        abstract = article.find('Abstract')
        meshheadinglist = medlinecitation.find('MeshHeadingList')
        mesh = []
        if meshheadinglist:
            for meshheading in meshheadinglist.findall('MeshHeading'):
                for i in meshheading:
                    mesh.append(i.text.lower())
        chemicallist = medlinecitation.find('ChemicalList')
        chemicaladd = []
        if chemicallist:
            for chemical in chemicallist.findall('Chemical'):
                chemicaladd.append(chemical.find('NameOfSubstance').text.lower())
        #print(abstract)
        if abstract:
            temp = abstract.find('AbstractText').itertext()
            abstracttext = ''
            for i in temp:
                abstracttext += i
            #print(abstracttext)
            #abstracttext = abstract.find('AbstractText').text.lower()
            res.append([PMID,articletitle,abstracttext,mesh,chemicaladd])



    for line in res:
        dic[line[0]] = {'title': line[1], 'abstract': line[2], 'mesh': line[3], 'chemical': line[4]}

with open('output_test.json', 'w') as output:
    json.dump(dic, output, indent=4)