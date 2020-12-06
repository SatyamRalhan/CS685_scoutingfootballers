from os import listdir
from os.path import isfile, join
import csv
from difflib import get_close_matches
# Attribute_possesion = [passes_completed, passes, dribbles_completed, dribbles, passes_completed_short, passes_short, passes_completed_medium, passes_medium, passes_completed_long, passes_long, passes_total_distance, passes_free_kicks, through_balls, passes_pressure, passes_switches, crosses, corner_kicks, passes_intercepted, passes_blocked, dispossessed]
# Attribute_attack = [goals, assists, pens_made, pens_att, shots_total, shots_on_target, sca, gca, xg, crosses_into_penalty_area, passes_into_final_third, passes_into_penalty_area, progressive_passes, carry_progressive_distance, assisted_shots, fouled, pens_won]
# Attribute_defense = [tackles, interceptions, blocks, tackles_won, dribble_tackles, dribbles_vs, pressures, pressure_regains, clearances, errors, aerials_won, aerials_lost, ball_recoveries, pens_conceded, fouls, cards_yellow_red]
#player to find similar

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

path = "players_zscore_all"

my_player = input("Enter the player name\n")

all_players = [f.split('.')[0] for f in listdir(path)]
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

players = [path + "/" + f for f in listdir(path)]
# print(players)
my_player = path + "/" + my_player + ".csv"
with open(my_player, newline='') as f:
	reader = csv.reader(f)
	match_attributes = list(reader)
	for i in range(1,len(match_attributes)):
		match_attributes[i][1] = float(match_attributes[i][1])

my_player_position = match_attributes[0][1]
my_player_attributes = getPlayerAttribute(match_attributes,my_player_position)
euclidean = []
cosine = []

for player in players:
	# print(player)
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)
	for i in range(1,len(attributes)):attributes[i][1] = float(attributes[i][1])	
	player_position = attributes[0][1]
	minutes_played = attributes[1][1]

	# if minutes_played < 300: continue
	if player_position=='GK':continue

	player_attributes = getPlayerAttribute(attributes,player_position)
	if poolmap[my_player_position] == poolmap[player_position]:
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
			prod = prod / ((sq_sum_1)*sq_sum_2)**0.5
		
		euclidean.append([eucli,player])
		cosine.append([prod,player])

for i in range(len(cosine)):
	cosine[i][0] = 1 - cosine[i][0]
euclidean.sort()
cosine.sort()

print("Euclidean")
# print(euclidean)
for i in range(11):print(euclidean[i])
print("\nCosine")
# print(cosine)
for i in range(11):print(cosine[i])
		






	


