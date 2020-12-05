from os import listdir
from os.path import isfile, join
from difflib import get_close_matches
import csv

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
	else: exit() 

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
euclidean = []
cosine = []

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
	cosine.append([prod,player])

euclidean.sort()
cosine.sort(reverse=True)


euclidiff = []
for i in range(10):
	euclidiff.append(euclidean[i][1].split('/')[1].split('_')[0])
cosdiff = []
for i in range(10):
	cosdiff.append(cosine[i][1].split('/')[1].split('_')[0])


# for x in euclidiff:print(x)
print("Intersection")
inter = [x for x in euclidiff if x in cosdiff]
for i in range(1,3):print(inter[i])

# print("\nEuclidean")
eucli2 = [x for x in euclidiff if x not in cosdiff]
for i in range(2):print(eucli2[i])

# print("\nCosine")
cos2 = [x for x in cosdiff if x not in euclidiff]
for i in range(2):print(cos2[i])