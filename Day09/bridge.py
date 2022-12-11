import time
#After doing this, i learned of complex, which is this, but built in, whoops.
with open('Day09/input') as file:
    inputList = file.readlines()

start_time = time.time()

#this includes the head, 10 for part 2, 2 for part 1, 
#this can track any arbitrary amount of tail touch positions
ropeLength = [2,10]
tailList = [[0,0] for _ in range(max(ropeLength))]
tailTouchList = [[[0,0]] for x in ropeLength]

#stealing this from the numpy modlue
def sign(num):
    if num == 0:
        return 0
    elif num > 0:
        return 1
    else:
        return -1

#calculate the diff between each index on two lists
def distanceBetween(x,y):
    if len(x) == len(y):
        dist = []
        for elem in range(len(x)):
            dist.append(x[elem] - y[elem])
        return dist
    else:
        #cant diff two diffrent sized lists
        return False

#this adds indexes of lists together, modifying the first list.
#I should chnage this to return the new list, not change existing
#return true if worked, false otherwise
def addMove(position, moveTuple):
    if len(position) == len(moveTuple):
        for i in range(len(position)):
            position[i] += moveTuple[i]
        return True
    else:
        return False

#discotnary of what each direction means in terms of moving on the grid
moves = {
    "L":(-1,0), 
    "R":(1,0),
    "U":(0,1),
    "D":(0,-1)
}

for input in inputList:

    input = input.strip().split()
    distance = input[1]
    direction = input[0]

    for i in range(int(distance)):
        #move the head, this in unconditional
        addMove(tailList[0],moves[direction])

        for j in range(1, max(ropeLength)):
            #get dist between current knot and previous knot
            diff = distanceBetween(tailList[j-1],tailList[j])

            #check if not right next to the previous knot in either directon
            #I initally checked abs(diff1 + diff2), but this ended in way more complex logic than handling them seperatly. 
            if abs(diff[0]) == 2 or abs(diff[1]) == 2:
                addMove(tailList[j] , [sign(diff[0]), sign(diff[1])])

            if j in ropeLength and tailList[j-1] not in tailTouchList[ropeLength.index(j)]: 
                #Python lists suck, so make a new list with the elements.
                tailTouchList[ropeLength.index(j)].append([tailList[j-1][0], tailList[j-1][1]])
        #if the last position of the tailList is not in the list of touched, add it.
        if tailList[-1] not in tailTouchList[-1]: 
            #Python lists suck, so make a new list with the elements.
            tailTouchList[-1].append([tailList[-1][0], tailList[-1][1]])

for i in range(len(ropeLength)):
    print ("Part",i+1,  "with a tail length of", len(tailTouchList[i]))
print("--- %s seconds ---" % (time.time() - start_time))