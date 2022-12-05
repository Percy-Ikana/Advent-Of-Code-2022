import time
import itertools
import copy

with open('Day5/input') as file:
    inputList = file.read()

start_time = time.time()

inputList = inputList.split("\n\n")
#this gets me a list where the list can actually be seperated
inputList[0] = inputList[0].replace("    ", ' ')
inputList[0] = [part for x in inputList[0].split('\n')[:-1] for part in [x.split(" ")]]
craneInstructions = [(int(parts[1]),int(parts[3])-1,int(parts[5])-1) for instruction in inputList[1].split('\n') for parts in [instruction.split(" ")]]

boxesList = [[] for _ in inputList[0][0]]
for j in range(len(inputList[0][0])):
    for i in range(len(inputList[0])-1, -1, -1):
        if inputList[0][i][j] != '':
            boxesList[j].append(inputList[0][i][j])

problem2BoxList = copy.deepcopy(boxesList)

#Solve Part 1
for instruction in craneInstructions:
    tempList = []
    for move in range(instruction[0]):
        boxesList[instruction[2]].append(boxesList[instruction[1]].pop())
        tempList.append(problem2BoxList[instruction[1]].pop())
    tempList.reverse()
    [problem2BoxList[instruction[2]].append(_) for _ in tempList]

print(''.join([x[-1] for x in boxesList]).replace('[', '').replace(']', ''))
print(''.join([x[-1] for x in problem2BoxList]).replace('[', '').replace(']', ''))
print("--- %s seconds ---" % (time.time() - start_time))