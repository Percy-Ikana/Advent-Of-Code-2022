import time
import sys

sign = lambda a: 1 if a>0 else -1 if a<0 else 0



def findMinAndMaxCords(cords):
    minPos = [sys.maxsize,sys.maxsize]
    maxPos = [-sys.maxsize,-sys.maxsize]
    for list in cords:
        for point in list:
            if minPos[0] > point[0]:
                minPos[0] = point[0]
            if maxPos[0] < point[0]:
                maxPos[0] = point[0]

            if minPos[1] > point[1]:
                minPos[1] = point[1]
            if maxPos[1] < point[1]:
                maxPos[1] = point[1]
    return (minPos, maxPos)

def buildGrid(minPos, maxPos, sandOrigin, rockFormations):
    #we make the grid twice as wide as needed to make sure there is room for overflow
    gridDict = {}
    fillGridWithRocks(gridDict, rockFormations, minPos)
    height = abs(maxPos[1] - sandOrigin[1])
    floorFloor = sandOrigin[0] - height*2
    floorCeil = sandOrigin[0] + height*2
    for x in range(floorFloor,floorCeil):
        gridDict[(x, maxPos[1]+2)] = '#'
    return gridDict

def fillGridWithRocks(gridDict, rockFormations, minPos):
    for formation in rockFormations:
        #we sub one so we dont go out of bounds when checking the next elem
        for ridge in range(len(formation)-1):
            start =formation[ridge]
            end = formation[ridge+1]
            diffX = end[0] - start[0]
            diffY = end[1] - start[1]
            pointsToChange = []
            #for each point of distance
            #this supports rectangles, not just lines, but only lines are used
            for x in range(abs(diffX)+1):
                for y in range(abs(diffY)+1):
                    #ranges are dumb, so to account for negatives, we multiply by the sign of the diff
                    changeX =start[0]+(x*sign(diffX))
                    changeY= start[1]+(y*sign(diffY))
                    pointsToChange.append((changeX, changeY))
            #this could be combined with above, and might be later, but this was useful for debugging.
            for point in pointsToChange:
                gridDict[point] = '#'

def printGrid(grid):
    graph = ''
    minPos = (min(grid, key=lambda x: x[0])[0],min(grid, key=lambda y: y[1])[1])
    maxPos = (max(grid, key=lambda x: x[0])[0],max(grid, key=lambda y: y[1])[1])
    for y in range(minPos[1], maxPos[1]):
        for x in range(minPos[0], maxPos[0]):
            if (x,y) in grid:
                graph = graph+grid[(x,y)]
            else:
                graph = graph + ' '
        graph = graph + '\n'
    return graph

def main():
    with open('Day14/input') as file:
        input = file.read()

    start_time = time.time()
    
    #parse input into a list of cords. Once again, this should be able to be one line but I cant figure it out.
    rockFormations = [y for x in input.split('\n') for y in [x.split(' -> ')]]
    for list in range(len(rockFormations)):
        for elem in range(len(rockFormations[list])):
            element = rockFormations[list][elem]
            rockFormations[list][elem] = (int(element.split(',')[0]),int(element.split(',')[1]))
    
    #figure out the min and max positions in this list of lits of cords, we will use these to only bother with the relevant areas,
    #as well as using this to figure out when sand is OOB
    minPos, maxPos = findMinAndMaxCords(rockFormations)

    #Build the simulation grid
    #this includes placing the rocks
    sandOrigin = (500,0)
    gridDict = buildGrid(minPos, maxPos, sandOrigin, rockFormations)

    #now we simulate the sand
    placedSand = 0
    #-1 as a default, so we can check if any amount of sand gets placed (0 is an option)
    placedSandPt1 = -1
    while True:
        x,y = sandOrigin
        #check is the origin has had sand added
        if sandOrigin in gridDict:
                #the sand origin has been filled
                break
        
        while True:
            # we have out grain of sand, make sure we can move
            #down, down left, down right
            if (below := (x, y+1)) not in gridDict:
                    #spot below is free, move to it
                    x,y = below
            elif (belowLeft := (x-1, y+1)) not in gridDict:
                    #spot below is free, move to it
                    x,y = belowLeft
            elif (belowRight := (x+1, y+1)) not in gridDict:
                    #spot below is free, move to it
                    x,y = belowRight
            else:
                    #we cant move
                    gridDict[(x,y)] = 'o'
                    placedSand += 1
                    break
        #check if we have fallen to the level of the nearest floor
        if placedSandPt1 == -1 and not (y < maxPos[1]):
            #once this is checked and recorded, we dont need to check again
            #-1 becasue the last placed sand was in an invalid position
            placedSandPt1 = placedSand - 1

    print (placedSandPt1, placedSand)
    #print(printGrid(gridDict))
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()