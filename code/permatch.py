
import csv
import requests
from bs4 import BeautifulSoup

text="https://fbref.com"

url="https://fbref.com/en/matches/5dc61284/Athletic-Club-Barcelona-August-16-2019-La-Liga"
req=requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

# print(soup.prettify())
playersdict={}
keys=[]
mydivs = soup.findAll("div", {"class": "table_wrapper"})
# print(mydivs[0].prettify())
for p in range(14):
    if (p+1)%7:
        mytable=mydivs[p].find("table")
        rows=mytable.findAll("tr")
        # print(rows[1])
        thiskeys=[]
        ths=rows[1].findAll("th")
        for i in ths:
            if i.getText() not in keys:
                keys.append(i.getText())
            thiskeys.append(i.getText())    
            # print(i.getText(),end=",")
        # print(thiskeys)
        # print()    
        for i in range(2,len(rows)-1):
        #     # print(i)
        #     # print(rows[i])
            th=rows[i].find("th")
            name=th.getText()
            tds=rows[i].findAll("td")
            localdict={}
            for k in range(len(tds)):
                localdict[thiskeys[k+1]]=tds[k].getText()
            if name in playersdict:    
                playersdict[name].update(localdict)
            else:
                playersdict[name]=localdict
    else:
        mytable=mydivs[p].find("table")
        rows=mytable.findAll("tr")
        # print(rows[1])
        thiskeys=[]
        ths=rows[1].findAll("th")
        for i in ths:
            if i.getText() not in keys:
                keys.append(i.getText())
            thiskeys.append(i.getText())
        for i in range(2,len(rows)):
        #     # print(i)
        #     # print(rows[i])
            th=rows[i].find("th")
            name=th.getText()
            tds=rows[i].findAll("td")
            localdict={}
            for k in range(len(tds)):
                localdict[thiskeys[k+1]]=tds[k].getText()
            if name in playersdict:    
                playersdict[name].update(localdict)
            else:
                playersdict[name]=localdict                    
            # print(localdict)
        
        # if 
        # print()    
# rows=table.find_all('tr')
# print(rows)
# print(mydivs)
# matchlist=[]
# print(keys)
# print(mydivs[6])
for i in playersdict:
    print(i,playersdict[i])
    print("\n\n\n")
# for i in range(1,len(rows)):
#     match_report=rows[i].find('td',{"data-stat":"match_report"})
#     team_1=rows[i].find('td',{"data-stat":"squad_a"})
#    # print(team_1.text)
#     team_2=rows[i].find('td',{"data-stat":"squad_b"})
#     #print(match_report)
#     #break
#     link=match_report.find_all('a')
#     #print(len(link))
#     if(len(link)!=0):
#         #print(team_1.text+","+team_2.text+","+link[0]['href'])
#         matchlist.append([team_1.text,team_2.text,text+link[0]['href']])
        
# print(matchlist)

# with open('matchestry.csv','w+') as csvfile:
#     csvwriter=csv.writer(csvfile)
#     csvwriter.writerows(matchlist)
# print(soup.find_all('a')[0]['href'])
