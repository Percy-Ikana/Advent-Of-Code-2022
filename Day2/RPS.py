import time

with open('Day2/input') as file:
    matchList = file.readlines()

start_time = time.time()

#part1 12645
playPointsDict = {"A":1, "B":2, "C":3, "X":1, "Y":2, "Z":3}
matchPointsDict = {"A X":3, "A Y":6, "A Z":0, "B X":0, "B Y":3, "B Z":6, "C X":6, "C Y":0, "C Z":3}
#Part 2 x win, y draw, z lose
matchPointsPt2Dict = {"A Z":8, "A Y":4, "A X":3, "B Z":9, "B Y":5, "B X":1, "C Z":7, "C Y":6, "C X":2}


totalPoints = [0,0]
for match in matchList:
    cleanMatch = match.strip()
    totalPoints[0] += playPointsDict[cleanMatch[-1]] + matchPointsDict[cleanMatch]
    totalPoints[1] += matchPointsPt2Dict[cleanMatch]

print(totalPoints[0])
print(totalPoints[1])
print("--- %s seconds ---" % (time.time() - start_time))