import os 
import csv
path = 'players/'
league_dir = [f for f in os.listdir(path)]

player_dict = {}
for league in league_dir:
	print(league)
	league_path = path+league
	if os.path.isfile(league_path):continue

	for player in os.listdir(league_path):
		player_path = league_path+'/'+player

		with open(player_path, newline='') as f:
				reader = csv.reader(f)
				match_attributes = list(reader)

		if player not in player_dict:
			attr_dict = {}
			for i in range(len(match_attributes)):
				if i>0:
					if match_attributes[i][1] == '':match_attributes[i][1] = 0 
					match_attributes[i][1] = float(match_attributes[i][1])
				attr_dict[match_attributes[i][0]] = match_attributes[i][1]

			player_dict[player] = attr_dict
		
		else:
			for i in range(1,len(match_attributes)):
				if match_attributes[i][1] == '' : match_attributes[i][1] = 0
				player_dict[player][match_attributes[i][0]] += float(match_attributes[i][1])

for player in player_dict:
	if player_dict[player]['minutes'] < 300:continue
	
	result = []
	for k in player_dict[player]:
		if k=='minutes':continue
		if k=='position':
			result.append([k,player_dict[player][k]])
		else:
			result.append([k,player_dict[player][k]/player_dict[player]['minutes']])

	write_dir = path+"leagues/" 
	with open(write_dir+player, "w") as ids:
		writer_w = csv.writer(ids,delimiter=',')
		for res in result: writer_w.writerow(res)
