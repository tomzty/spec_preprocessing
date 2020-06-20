import xml.etree.ElementTree as ET
import json

root = ET.parse('pubmed20n0001.xml').getroot()

res = []

for child in root:
    medlinecitation = child.find('MedlineCitation')
    PMID = medlinecitation.find('PMID').text
    
    article = medlinecitation.find('Article')
    articletitle = article.find('ArticleTitle').text.lower()
    
    abstract = article.find('Abstract')
    
    meshheadinglist = medlinecitation.find('MeshHeadingList')
    mesh = []
    for meshheading in meshheadinglist.findall('MeshHeading'):
        for i in meshheading:
            mesh.append(i.text.lower())
    chemicallist = medlinecitation.find('ChemicalList')
    chemicaladd = []
    if not chemicallist:
        continue
    for chemical in chemicallist.findall('Chemical'):
        chemicaladd.append(chemical.find('NameOfSubstance').text.lower())
    if abstract:
        abstracttext = abstract.find('AbstractText').text.lower()
        res.append([PMID,articletitle,abstracttext,mesh,chemicaladd])


dic = {}
for line in res:
    dic[line[0]] = {'title': line[1], 'abstract': line[2], 'mesh': line[3], 'chemical': line[4]}


with open('output_test.json', 'w') as output:
    json.dump(dic, output, indent=4)