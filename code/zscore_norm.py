import os
import csv
path = "players/leagues/"
players = [path + f for f in os.listdir(path)]

zscore = 55*[[0,0]] #to store mu,sigma
average = 55*[0]
sigma = 55*[0]
for player in players:
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)
	# print(attributes)

	if attributes[0][1] != 'GK':continue
	for	i in range(1,len(attributes)):
		average[i] += float(attributes[i][1])

for i in range(len(average)):
	average[i] /= len(players)

for player in players:
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)
	if attributes[0][1] != 'GK':continue	
	for	i in range(1,len(attributes)):
		sigma[i] += (float(attributes[i][1]) - average[i])**2

for i in range(len(sigma)):
	sigma[i] = (sigma[i]/len(players)) ** 0.5

for i in range(len(zscore)):
	zscore[i] = [average[i],sigma[i]]

current_directory = os.getcwd()
new_directory = current_directory + "/players_zscore/"

if not os.path.exists(new_directory):
    os.makedirs(new_directory)

for player in players:
	player_zscore = new_directory + player.split('/')[-1]  
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)
	
	if attributes[0][1] != 'GK':continue

	result = [attributes[0]]
	for i in range(1,len(attributes)):
		if zscore[i][1] == 0:
			score = 0
		else:
			score = (float(attributes[i][1]) - zscore[i][0]) / zscore[i][1]
		result.append([attributes[i][0],round(score,4)])

	with open(player_zscore, "w") as ids:
		writer_w = csv.writer(ids,delimiter=',')
		for res in result: writer_w.writerow(res)



