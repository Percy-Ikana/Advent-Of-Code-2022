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
    grid = [[' ' for x in (range((maxPos[0] - minPos[0])*2))] for y in range((maxPos[1] - minPos[1])+3)]
    grid[-1] = ['#' for floor in grid[-1]]
    fillGridWithRocks(grid, rockFormations, minPos)
    grid[sandOrigin[1]][sandOrigin[0] - minPos[0]] = '+'
    return grid

def fillGridWithRocks(grid, rockFormations, minPos):
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
                gridXPos = point[0] - minPos[0]
                gridYPos = point[1] - minPos[1]
                #x and Y flip here to make the grid look like the example. 
                grid[gridYPos][gridXPos] = '#'

def printGrid(grid):
    graph = ''
    for line in grid:
        graph = graph + '\n' + ''.join(line)
    return graph

def inBounds(point, grid):
    if point[1] < 0 or point[1] >= len(grid):
        return False
    if point[0] < 0 or point[0] >= len(grid[1]):
        return False
    return True

def inBoundsPart1(point, minPos, maxPos):
    #0 because we cont car if its out of range from the top.
    if point[1] < 0 or point[1] > maxPos[1]:
        return False
    if point[0] < minPos[0] or point[0] > maxPos[0]:
        return False
    return True

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
    #we are going to cheat and make the minPos (x, 0)
    gridMinPos = (0, 0)

    #Build the simulation grid
    #this includes placing the rocks
    sandOrigin = (500,0)
    grid = buildGrid(gridMinPos, maxPos, sandOrigin, rockFormations)

    #now we simulate the sand
    endSim = False
    outOfBounds = False
    placedSand = 0
    placedSandPt1 = 0
    while not endSim:
        moved = True
        sandPos = (sandOrigin[0], sandOrigin[1])
        while moved:
            # we have out grain of sand, make sure we can move
            #down, down left, down right
            moved = False
            below = (sandPos[0], sandPos[1]+1)
            belowLeft = (sandPos[0]-1, sandPos[1]+1)
            belowRight = (sandPos[0]+1, sandPos[1]+1)

            belowInBounds = inBounds(below, grid)
            belowLeftInBounds = inBounds(belowLeft, grid)
            belowRightInBounds = inBounds(belowRight, grid)

            placed = False
            if belowInBounds and belowLeftInBounds and belowRightInBounds:
                if grid[below[1]][below[0]] == ' ':
                    #spot below is free, move to it
                    moved = True
                    sandPos = below
                elif grid[belowLeft[1]][belowLeft[0]] == ' ':
                    #spot below is free, move to it
                    moved = True
                    sandPos = belowLeft
                elif grid[belowRight[1]][belowRight[0]] == ' ':
                    #spot below is free, move to it
                    moved = True
                    sandPos = belowRight
                else:
                    #we cant move
                    grid[sandPos[1]][sandPos[0]] = 'o'
                    placedSand += 1
            if (not inBoundsPart1(below, minPos, maxPos) or not inBoundsPart1(belowLeft, minPos, maxPos) or not inBoundsPart1(belowRight, minPos, maxPos)) and not outOfBounds:
                #once this is checked and recorded, we dont need to check again
                placedSandPt1 = placedSand
                outOfBounds = True
            if (grid[below[1]][below[0]] == 'o' and grid[belowLeft[1]][belowLeft[0]] == 'o' and grid[belowRight[1]][belowRight[0]] == 'o' and sandPos == sandOrigin) or (not belowInBounds or not belowLeftInBounds or not belowRightInBounds):
                #the sand origin has been filled
                endSim = True

    print (placedSandPt1, placedSand)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()