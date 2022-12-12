#this wont work, too slow.

import time
import copy

import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(6000)
print(sys.getrecursionlimit())

with open('Day12/input') as file:
    inputList = [list(x.strip()) for x in file.readlines()]

start_time = time.time()

def findPath(pos, end, map, mapSize ,visitedList):
    #chek if this posiiton is even in bounds
    seen = [(x[0][0],x[0][1]) for x in visitedList]
    if pos[0][0] < 0 or pos[0][1] < 0 or pos[0][0] >= len(map) or pos[0][1] >= len(map[pos[0][0]]) or pos[0] in seen or len(visitedList) == mapSize:
        #this is not a valid position, or we have already checked it
        return -1
        pass
    #check if our current posiiton is equal to E
    elif pos[0] == end[0] and ord(map[pos[0][0]][pos[0][1]]) - ord(map[visitedList[-1][0][0]][visitedList[-1][0][1]]) <= 1:
        #We have found the end
        pos = [(pos[0][0],pos[0][1]), 'E']
        visitedList = copy.deepcopy(visitedList)
        visitedList.append(pos)
        print("path found with length", len(visitedList))
        return visitedList
    #check to see if the current square is even a valid posiiton from the previous, unless this is the first
    elif len(visitedList) < 2 or ord(map[pos[0][0]][pos[0][1]]) - ord(map[visitedList[-1][0][0]][visitedList[-1][0][1]]) <= 1 or len(visitedList) > mapSize:
        pass
        if not len(visitedList) == 0 and map[visitedList[-1][0][0]][visitedList[-1][0][1]] == 'v' and map[pos[0][0]][pos[0][1]] == 'z':
            temp1 = ord(map[pos[0][0]][pos[0][1]])
            temp2 = ord(map[visitedList[-1][0][0]][visitedList[-1][0][1]])
            pass
        #this is a position where we can check the next lists 
        visitedList = copy.deepcopy(visitedList)
        visitedList.append(pos)
        pos1 = [(pos[0][0] - 1, pos[0][1]), '^']
        pos2 = [(pos[0][0] + 1, pos[0][1]), 'v']
        pos3 = [(pos[0][0], pos[0][1] - 1), '<']
        pos4 = [(pos[0][0], pos[0][1] + 1), '>']
        posList = [findPath(pos1, end, map, mapSize ,visitedList), findPath(pos2,end, map, mapSize ,visitedList), findPath(pos3,end, map, mapSize ,visitedList),findPath(pos4,end, map, mapSize ,visitedList)]
        minLenIndex = -1
        for each in posList:
            if type(each) is list:
                if minLenIndex == -1:
                    minLenIndex = posList.index(each)
                elif len(each) < len(posList[minLenIndex]):
                    minLenIndex = posList.index(each)
        return posList[minLenIndex]
    else:
        #this is an invalid pos
        return -1
        

#find position of S and E
mapSize = 0
start, end = [],[]
for line in range(len(inputList)):
    for pos in range(len(inputList[line])):
        if inputList[line][pos] == 'S':
            start = [(line, pos), 'X']
            inputList[line][pos] = 'a'
        if inputList[line][pos] == 'E':
            end.append([(line, pos), 'X'])
            inputList[line][pos] = 'z'
        mapSize +=1

#begin the recusion
ans = findPath(start, end,inputList, mapSize , [])

for each in ans:
    inputList[each[0][0]][each[0][1]] = each[1][0]
print(len(ans)-1)

print("--- %s seconds ---" % (time.time() - start_time))