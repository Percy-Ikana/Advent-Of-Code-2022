import time
import copy

with open('Day05/input') as file:
    inputList = file.read()

start_time = time.time()

inputList = inputList.split("\n\n")
#this gets me a list where the list can actually be seperated into '' or [_] easily.
inputList[0] = inputList[0].replace("    ", ' ')
#List comp takes the first aprt of the input, and seperates each row into a list consisiting of a value for each col of the input, for all rows
#resulting in a 2d list representing the input as in the file
inputList[0] = [part for x in inputList[0].split('\n')[:-1] for part in [x.split(" ")]]
#This takes the latter part of the input, and puts the values from the instructions into a tuple, where 1 = # boxes, 2 = Origin, 3 = Dest, 
#then puts all the tuples into a list
craneInstructions = [(int(parts[1]),int(parts[3])-1,int(parts[5])-1) for instruction in inputList[1].split('\n') for parts in [instruction.split(" ")]]

#this unholy peice of code takes the "boxes" input, and parses it into a lost of stacks that can be easily popped/pushed
boxesList = [[] for _ in inputList[0][0]]
for j in range(len(inputList[0][0])):
    for i in range(len(inputList[0])-1, -1, -1):
        if inputList[0][i][j] != '':
            boxesList[j].append(inputList[0][i][j])

#make a list for the part2 problem
problem2BoxList = copy.deepcopy(boxesList)

 
for instruction in craneInstructions:
    #part 1 solution, pop box off top of origin, append to dest, repeat however many times the instruction wants.
    for move in range(instruction[0]):
        boxesList[instruction[2]].append(boxesList[instruction[1]].pop())

    #part 2
    #slice the last X elements from the orgin stack, and put on the dest stack. This would also work for part1, if we reverse the list, but I like keeping the pop/place
    [problem2BoxList[instruction[2]].append(_) for _ in problem2BoxList[instruction[1]][-instruction[0]:]]
    #remove the boxes from the origin stack
    del problem2BoxList[instruction[1]][-instruction[0]:]
    

print(''.join([x[-1] for x in boxesList]).replace('[', '').replace(']', ''))
print(''.join([x[-1] for x in problem2BoxList]).replace('[', '').replace(']', ''))
print("--- %s seconds ---" % (time.time() - start_time))