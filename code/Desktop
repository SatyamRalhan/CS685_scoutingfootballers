import os
from os.path import isfile, join
import csv

path = "players"
players = [path + "/" + f for f in os.listdir(path)]
print(players)

zscore = 55*[[0,0]] #to store mu,sigma
average = 55*[0]
sigma = 55*[0]

for player in players:
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)

	for	i in range(1,len(attributes)):
		average[i] += float(attributes[i][1])

for i in range(len(average)):
	average[i] /= len(players)

for player in players:
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)

	for	i in range(1,len(attributes)):
		sigma[i] += (float(attributes[i][1]) - average[i])**2

for i in range(len(sigma)):
	sigma[i] = (sigma[i]/len(players)) ** 0.5

for i in range(len(zscore)):
	zscore[i] = [average[i],sigma[i]]		 

current_directory = os.getcwd()
new_directory = current_directory + "/players_zscore"
if not os.path.exists(new_directory):
    os.makedirs(new_directory)

for player in players:
	player_zscore = new_directory + "/" + player.split('/')[-1]  

	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)

	result = [attributes[0]]	

	for i in range(1,len(attributes)):
		if zscore[i][1] == 0:
			score = 0
		else:
			score = (float(attributes[i][1]) - zscore[i][0]) / zscore[i][1]
		result.append([attributes[i][0],score])	

	with open(player_zscore, "w") as ids:
		writer_w = csv.writer(ids,delimiter=',')
		for res in result: writer_w.writerow(res)







