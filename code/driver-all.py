from os import listdir
from os.path import isfile, join
import csv

my_player = input("Enter the player name\n")
my_player_pos = input("Enter the player player position\n")
my_player += "_" + my_player_pos

path = "players_zscore"
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
for i in range(50):
	euclidiff.append(euclidean[i][1].split('/')[1].split('_')[0])
cosdiff = []
for i in range(50):
	cosdiff.append(cosine[i][1].split('/')[1].split('_')[0])

# for i in range(15):print(euclidiff[i])
# for i in range(15):print(cosdiff[i])

# for x in euclidiff:print(x)
print("Intersection")
inter = [x for x in euclidiff if x in cosdiff]
for i in range(1,3):print(inter[i])

print("\nEuclidean")
eucli2 = [x for x in euclidiff if x not in cosdiff]
for i in range(2):print(eucli2[i])

print("\nCosine")
cos2 = [x for x in cosdiff if x not in euclidiff]
for i in range(2):print(cos2[i])