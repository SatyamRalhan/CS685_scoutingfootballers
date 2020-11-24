import csv
import requests
import os
from os import listdir
from os.path import isfile
from bs4 import BeautifulSoup

text="https://fbref.com"

path = "../../"
match_urls = [f for f in listdir(path)]
# for x in match_urls:print(x)

waste = open("Waste/wastefiles",'w')

for match_file in match_urls:

    if isfile(path+match_file):
        os.mkdir(match_file)

        with open(path + match_file, newline='\n',encoding='latin-1') as f:
            reader = csv.reader(f)
            urls = list(reader)

        # print(len(urls))

        for url in urls:
            req=requests.get(url[2])
            soup = BeautifulSoup(req.content, 'html.parser')
            print(url)

            playersdict={}
            keys=[]
            mydivs = soup.findAll("div", {"class": "table_wrapper"})


            for p in range(14):
                if (p+1)%7:
                    if len(mydivs) < p+1:continue
                    mytable=mydivs[p].find("table")
                    # print(mytable)
                    if mytable is None:
                        print(url[2],file = waste)
                        continue
                    rows=mytable.findAll("tr")
                    # print(rows[1])
                    thiskeys=[]
                    ths=rows[1].findAll("th")
                    for i in ths:
                        # if i.getText() not in keys:
                        #     keys.append(i.getText())
                        # thiskeys.append(i.getText())  
                        # print(i)
                        temp = i['data-stat']
                        if temp not in keys:
                            keys.append(temp)
                        thiskeys.append(temp)    
                        # print(i.getText(),end=",")
                    # print(keys)
                    # print(thiskeys)
                    # print()    
                    for i in range(2,len(rows)-1):
                    #     # print(i)
                    #     # print(rows[i])
                        th=rows[i].find("th")
                        name=th.getText()
                        #print(name+"\n")
                        tds=rows[i].findAll("td")
                        localdict={}
                        for k in range(len(tds)):
                            localdict[thiskeys[k+1]]=tds[k].getText()
                        if name in playersdict:    
                            playersdict[name].update(localdict)
                        else:
                            playersdict[name]=localdict
                else:
                    if(len(mydivs)<p+1):
                        continue
                    mytable=mydivs[p].find("table")
                    if mytable is None:
                        print(url[2],file = waste)
                        continue
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
            
            
            #print(s)

            for i in playersdict:
                if 'position' not in playersdict[i]:
                    print(i)
                    continue
                position=playersdict[i]['position'].split(',')[0]
                if(position=='GK'):
#                    print(playersdict[i])
#                    break
                    f=open('../gkattributes.txt','r')
                    lines=f.readlines()
                    s=[]
                    for l in lines:
                        s.append(l.split('\n')[0])
                    p_name = match_file+'/'+i.strip()+"_"+position+".csv" 
                    if(os.path.exists(p_name)):
                        with open(p_name,'r') as fi:
                            for line in csv.reader(fi):
                                if(line[0]!='position'):
                                    if line[0] in playersdict[i]:
                                        if line[1] == '':line[1] = '0'
                                        if playersdict[i][line[0]] == '':playersdict[i][line[0]] = 0
                                        playersdict[i][line[0]]=str(float(line[1])+float(playersdict[i][line[0]]))
                
                    with open(p_name,'w') as fi:
                        for attri in s:
                            if attri in playersdict[i]:
                                fi.write("%s,%s\n"%(attri,playersdict[i][attri]))
                else:
                    f=open('../attributes.txt','r')
                    lines=f.readlines()
                    s=[]
                    for l in lines:
                        s.append(l.split('\n')[0])
                    p_name = match_file+'/'+i.strip()+"_"+position+".csv" 
                    if(os.path.exists(p_name)):
                        with open(p_name,'r') as fi:
                            for line in csv.reader(fi):
                                if(line[0]!='position'):
                                    if line[0] in playersdict[i]:
                                        if line[1] == '':line[1] = '0'
                                        if playersdict[i][line[0]] == '':playersdict[i][line[0]] = 0
                                        playersdict[i][line[0]]=str(float(line[1])+float(playersdict[i][line[0]]))
                
                    with open(p_name,'w') as fi:
                        for attri in s:
                            if attri in playersdict[i]:
                                fi.write("%s,%s\n"%(attri,playersdict[i][attri]))
            

