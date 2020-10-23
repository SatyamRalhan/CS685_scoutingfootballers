html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
import csv
import requests
from bs4 import BeautifulSoup

cur=20
text="https://fbref.com"
url="https://fbref.com/en/comps/9/3232/schedule/"
while(url!=""):

    req=requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    nexturl=soup.find('div',id="info").find("div",{"class":"prevnext"}).find("a",{"class":"prev"})
    if(nexturl):
        url=text+nexturl['href']
    else:
        break
#    print(nexturl)
#    break
#    print(soup.prettify())
    
    table=soup.find('table')
    #print(table)
    rows=table.find_all('tr')
    #print(rows[0])
    
    matchlist=[]
    
    for i in range(1,len(rows)):
        match_report=rows[i].find('td',{"data-stat":"match_report"})
        team_1=rows[i].find('td',{"data-stat":"squad_a"})
       # print(team_1.text)
        team_2=rows[i].find('td',{"data-stat":"squad_b"})
        #print(match_report)
        #break
        link=match_report.find_all('a')
        #print(len(link))
        if(len(link)!=0):
            #print(team_1.text+","+team_2.text+","+link[0]['href'])
            matchlist.append([team_1.text,team_2.text,text+link[0]['href']])
        
    
#    print(matchlist)
    if(cur!=0):
        filename="epl"+str(cur-1)+"-"+str(cur)+".csv"
    else:
        filename="epl99-00.csv"
    with open(filename,'w+') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerows(matchlist)
#    print(soup.find_all('a')[0]['href'])
    if(cur==0):
        cur=99
    else:
        cur-=1