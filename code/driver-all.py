from os import listdir
from os.path import isfile, join
from difflib import get_close_matches
from scipy.special import softmax

import csv

with open("survey_ranks.csv", newline='') as f:
	reader = csv.reader(f)
	ranks = list(reader)

eucli_point = 0
cos_point = 0

position_stricker = ['FW']
position_winger = ['LW','RW']
position_attacking_mid = ['AM']
position_center_mid = ['LM','CM','RM','MF']
position_defensive_mid = ['CDM','DM']
position_center_back = ['CB','DF']
position_full_back = ['RB','LB','WB']
position_goalkeeper = ['GK']
poolmap = {}

for x in position_stricker:
	poolmap[x] = ["attribute_attack"]
for x in position_winger:
	poolmap[x] = ["attribute_possesion","attribute_attack"]
for x in position_attacking_mid:
	poolmap[x] = ["attribute_possesion","attribute_attack"]		
for x in position_center_mid:
	poolmap[x] = ["attribute_possesion"]
for x in position_defensive_mid:
	poolmap[x] = ["attribute_possesion","attribute_defence"]
for x in position_full_back:
	poolmap[x] = ["attribute_defence","attribute_defence","attribute_possesion"]
for x in position_center_back:
	poolmap[x] = ["attribute_possesion","attribute_defence"]
for x in position_goalkeeper:
	poolmap[x] = ["atttibute_gk"]

def getPlayerAttribute(attributes,player_position):
	attribute_dict = {}
	attribute_dict["attribute_possesion"] = attributes[2:22]
	attribute_dict["attribute_attack"] = attributes[22:39]
	attribute_dict["attribute_defence"] = attributes[39:]
	attribute_dict["attribute_gk"] = attributes[:]

	player_attribute = []
	for x in poolmap[player_position]:
		player_attribute += attribute_dict[x]
	
	return player_attribute


def weight(points,pref):
	global eucli_point
	global cos_point
	if pref == "": return
	if len(pref)>1:return
	pref=int(pref)
	if pref == 3 or pref == 4: eucli_point += points
	elif pref == 5 or pref == 6: cos_point += points
	else:
		eucli_point += points/2
		cos_point += points/2

for i in range(len(ranks)):
	for j in range(len(ranks[i])):
		if (j+1)%4 == 0: continue
		elif (j+1)%4 == 1: weight(3,ranks[i][j])
		elif (j+1)%4 == 2: weight(2,ranks[i][j])
		elif (j+1)%4 == 3: weight(1,ranks[i][j])

# print(eucli_point,cos_point)

path = "players_zscore"

my_player = input("Enter the player name\n")
all_players = [f.split('_')[0] for f in listdir(path)]
if my_player not in all_players:
	gcm = get_close_matches(my_player,all_players)
	if len(gcm) > 0: gcm=gcm[0]
	else:
		print("Enter valid player name")
		exit()
	print("Did you mean",gcm,"[y/n]")
	user_response = input()
	if user_response == 'y': my_player = gcm
	else:
		print("Enter valid player name")
		exit() 

pos = [i.rsplit('_',1)[1].split('.')[0] for i in listdir(path) if isfile(join(path,i)) and my_player in i]
print("Enter the player position out of the following:")

for x in pos:print(x,end=" ")
my_player_pos = input("\n")

my_player += "_" + my_player_pos
players = [path + "/" + f for f in listdir(path)]
my_player = path + "/" + my_player + ".csv"

with open(my_player, newline='') as f:
	reader = csv.reader(f,delimiter=',')
	match_attributes = list(reader)
	for i in range(1,len(match_attributes)):
		match_attributes[i][1] = float(match_attributes[i][1])

my_player_position = match_attributes[0][1]
my_player_attributes = match_attributes[1:]
euclidean,eucli_val = [],[]
cosine,cos_val = [],[]

for player in players:
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)

	if my_player_position != attributes[0][1]: continue
	for i in range(1,len(attributes)):attributes[i][1] = float(attributes[i][1])

	minutes_played = attributes[1][1]
	player_attributes = attributes[1:]
	
	eucli = 0
	prod = 0
	sq_sum_1 = 0
	sq_sum_2 = 0
	for i in range(1,len(player_attributes)):
		eucli += (player_attributes[i][1]-my_player_attributes[i][1])**2
		prod += player_attributes[i][1]*my_player_attributes[i][1]
		sq_sum_1 += player_attributes[i][1]**2
		sq_sum_2 += my_player_attributes[i][1]**2
	eucli = eucli**0.5
	if sq_sum_1!=0 and sq_sum_2!=0:
		prod = prod / ((sq_sum_1*sq_sum_2)**0.5)
	
	euclidean.append([eucli,player])
	eucli_val.append(eucli)
	cosine.append([prod,player])
	cos_val.append(1-prod)

eucli_val = softmax(eucli_val)
cos_val = softmax(cos_val)

final_order = []

for i in range(len(euclidean)):
	euclidean[i][0] = eucli_val[i]
	cosine[i][0] = cos_val[i]
	name = euclidean[i][1]
	value = eucli_val[i]*eucli_point + cos_val[i]*cos_point
	final_order.append([value,name])

final_order.sort()
print("\nThe following players could be a possible replacement:")
for i in range(1,11):
	print(str(i)+":",final_order[i][1].split('/')[1].split('_')[0])
