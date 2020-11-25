# from os import listdir
# from os.path import isfile, join
# import csv

# my_player = input("Enter the player name\n")

# player_name = my_player
# path = "players_zscore"
# pos = [i.rsplit('_',1)[1].split('.')[0] for i in listdir(path) if isfile(join(path,i)) and player_name in i]
# # print(pos)
# g_euclidean = []
# g_cosine = []
# for a in pos:

# 	# my_player_pos = input("Enter the player player position\n")
# 	my_player_pos = a
# 	my_player = player_name + "_" + my_player_pos	

# 	# pos = [i.rsplit('_',1)[1].split('.')[0] for i in listdir(path) if isfile(join(path,i)) and temp in i]

# 	# print(pos)

# 	players = [path + "/" + f for f in listdir(path)]

# 	my_player = path + "/" + my_player + ".csv"
# 	print(my_player)


# 	with open(my_player, newline='') as f:
# 		reader = csv.reader(f,delimiter=',')
# 		match_attributes = list(reader)
# 		for i in range(1,len(match_attributes)):
# 			match_attributes[i][1] = float(match_attributes[i][1])
# 	# print(match_attributes)
# 	my_player_position = match_attributes[0][1]
# 	my_player_attributes = match_attributes[1:]
# 	euclidean = []
# 	cosine = []

# 	for player in players:
# 		with open(player, newline='') as f:
# 			reader = csv.reader(f)
# 			attributes = list(reader)

# 		if my_player_position != attributes[0][1]: continue
# 		for i in range(1,len(attributes)):attributes[i][1] = float(attributes[i][1])

# 		minutes_played = attributes[1][1]
# 		player_attributes = attributes[1:]
# 		# print(player_attributes)
# 		eucli = 0
# 		prod = 0
# 		sq_sum_1 = 0
# 		sq_sum_2 = 0
# 		for i in range(1,len(player_attributes)):
# 			eucli += (player_attributes[i][1]-my_player_attributes[i][1])**2
# 			prod += player_attributes[i][1]*my_player_attributes[i][1]
# 			sq_sum_1 += player_attributes[i][1]**2
# 			sq_sum_2 += my_player_attributes[i][1]**2
# 		eucli = eucli**0.5
# 		if sq_sum_1!=0 and sq_sum_2!=0:
# 			prod = prod / ((sq_sum_1*sq_sum_2)**0.5)
		
# 		euclidean.append([eucli,player])
# 		cosine.append([prod,player])

# 	euclidean.sort()
# 	cosine.sort(reverse=True)


# 	g_euclidean = g_euclidean+euclidean[:11]
# 	g_cosine = g_cosine + cosine[:11]

# # print(g_euclidean)
# # print(g_cosine)
# g_euclidean.sort()
# g_cosine.sort(reverse=True)
# # print(g_euclidean)
# # print(g_cosine)
# print("Euclidean")
# # print(euclidean)
# for i in range(10+len(pos)):print(g_euclidean[i])

# print("\nCosine")
# # print(cosine)
# for i in range(10+len(pos)):print(g_cosine[i])
		
from os import listdir
from os.path import isfile, join
import csv

my_player = input("Enter the player name\n")
my_player_name = my_player
path = "players_zscore"
pos = [i.rsplit('_',1)[1].split('.')[0] for i in listdir(path) if isfile(join(path,i)) and my_player_name in i]
# print(pos)
g_euclidean = []
g_cosine = []
total_minutes = 0
print(pos)
for my_player_pos in pos:
# my_player_pos = input("Enter the player player position\n")
	my_player = my_player_name + "_" + my_player_pos

	path = "players_zscore"
	players = [path + "/" + f for f in listdir(path)]

	my_player = path + "/" + my_player + ".csv"

	with open(my_player, newline='') as f:
		reader = csv.reader(f,delimiter=',')
		match_attributes = list(reader)
		for i in range(1,len(match_attributes)):
			match_attributes[i][1] = float(match_attributes[i][1])

	my_player_position = match_attributes[0][1]
	my_player_minutes = match_attributes[1][1]
	my_player_attributes = match_attributes[1:]
	euclidean = []
	cosine = []

	for player in players:
		player_name = player.rsplit('_',1)[0].split('/')[1]
		if player_name == my_player_name: continue
		with open(player, newline='') as f:
			reader = csv.reader(f)
			attributes = list(reader)

		if my_player_position != attributes[0][1]: continue
		for i in range(1,len(attributes)):attributes[i][1] = float(attributes[i][1])

		minutes_played = attributes[1][1]
		player_attributes = attributes[1:]
		# print(player_attributes)
		
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
		cosine.append([prod,player])

	euclidean.sort()
	cosine.sort(reverse=True)

	# print("Euclidean")
	# # print(euclidean)
	# for i in range(11):print(euclidean[i])
	# print("\nCosine")
	# # print(cosine)
	# for i in range(11):print(cosine[i])
	total_minutes += my_player_minutes
	euclidean = [[a/my_player_minutes,b,a] for a,b in euclidean]
	cosine = [[a*my_player_minutes,b,a] for a,b in cosine]	
	g_euclidean = g_euclidean+euclidean[:11]
	g_cosine = g_cosine + cosine[:11]

# print(g_euclidean)
# print(g_cosine)
g_euclidean = [[a*total_minutes,b,c] for a,b,c in g_euclidean]
g_cosine = [[a/total_minutes,b,c] for a,b,c in g_cosine]
g_euclidean.sort()
g_cosine.sort(reverse=True)
# print(g_euclidean)
# print(g_cosine)
print("Euclidean")
print("Weighted Euclidean,Player_Name_Pos,Original Euclidean")
# print(euclidean)
for i in range(10):print(g_euclidean[i])

print("\nCosine")
print("Weighted Cosine,Player_Name_Pos,Original Cosine")
# print(cosine)
for i in range(10):print(g_cosine[i])