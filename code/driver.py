from os import listdir
from os.path import isfile, join
import csv

# Attribute_possesion = [passes_completed, passes, dribbles_completed, dribbles, passes_completed_short, passes_short, passes_completed_medium, passes_medium, passes_completed_long, passes_long, passes_total_distance, passes_free_kicks, through_balls, passes_pressure, passes_switches, crosses, corner_kicks, passes_intercepted, passes_blocked, dispossessed]
# Attribute_attack = [goals, assists, pens_made, pens_att, shots_total, shots_on_target, sca, gca, xg, crosses_into_penalty_area, passes_into_final_third, passes_into_penalty_area, progressive_passes, carry_progressive_distance, assisted_shots, fouled, pens_won]
# Attribute_defense = [tackles, interceptions, blocks, tackles_won, dribble_tackles, dribbles_vs, pressures, pressure_regains, clearances, errors, aerials_won, aerials_lost, ball_recoveries, pens_conceded, fouls, cards_yellow_red]

#player to find similar
my_player = input("Enter the player name")

position_stricker = ['FW']
position_winger = []
position_attacking_mid = []
position_center_mid = ['CM']
position_defensive_mid = ['']
position_center_back = ['CB']
position_full_back = []
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
	# atttibute_gk = attributes[]

	player_attribute = []
	for x in poolmap[player_position]:
		player_attribute += attribute_dict[x]
	
	return player_attribute					

path = "players_zscore"
players = [path + "/" + f for f in listdir(path)]
print(players)

my_player = path + "/" + my_player + ".csv"

with open(my_player, newline='') as f:
	reader = csv.reader(f)
	match_attributes = list(reader)
	for i in range(1,len(match_attributes)):match_attributes[i][1] = float(match_attributes[i][1])

my_player_position = match_attributes[0][1]
my_player_attributes = getPlayerAttribute(match_attributes,my_player_position)

euclidean = len(my_player_attributes) * [-1]
cosine = len(my_player_attributes) * [-1]
pi = 0
for player in players:
	with open(player, newline='') as f:
		reader = csv.reader(f)
		attributes = list(reader)
	for i in range(1,len(attributes)):attributes[i][1] = float(attributes[i][1])	

	player_position = attributes[0][1]
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
			sq_sum_2 +=my_player_attributes[i][1]**2

		euclidean[pi] = eucli**0.5
		if sq_sum_1!=0 and sq_sum_2!=0:
			cosine[pi] = prod / ((sq_sum_1)*sq_sum_2)**0.5
	pi+=1		  	


print(euclidean)
print(cosine)

		













	




