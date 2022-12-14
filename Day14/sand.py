    #minPos = (min(cords, key=lambda x: x[0])[0],min(cords, key=lambda y: y[1])[1])
    #maxPos = (max(cords, key=lambda x: x[0])[0],max(cords, key=lambda y: y[1])[1])
import time
import sys

sign = lambda a: 1 if a>0 else -1 if a<0 else 0

def printGrid(grid):
    for line in grid:
        print (''.join(line))

def inBounds(point, grid):
    if point[1] < 0 or point[1] >= len(grid):
        return False
    if point[0] < 0 or point[0] >= len(grid[0]):
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
    #we will always make the list start at 0
    minPos = [sys.maxsize-1,0]
    maxPos = [-sys.maxsize,-sys.maxsize]
    for list in rockFormations:
        for point in list:
            if minPos[0] > point[0]:
                minPos[0] = point[0]
            if maxPos[0] < point[0]:
                maxPos[0] = point[0]

            if minPos[1] > point[1]:
                minPos[1] = point[1]
            if maxPos[1] < point[1]:
                maxPos[1] = point[1]

    #Build the simulation grid
    grid = [[' ' for x in (range((maxPos[0] - minPos[0])+1))] for y in range((maxPos[1] - minPos[1])+1)]
    sandOrigin = (500,0)
    grid[sandOrigin[1]][sandOrigin[0] - minPos[0]] = '+'
    #Now lets place all the rocks on the grid
    #We can heat, because each list only changes by one dimesion at a time,
    #and there are no single long lists

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

    #now we simulate the sand
    outOfBounds = False
    placedSand = 0
    while not outOfBounds:
        moved = True
        sandPos = ( sandOrigin[0] - minPos[0], sandOrigin[1])
        while moved:
            # we have out grain of sand, make sure we can move
            #down, down left, down right
            moved = False
            below = (sandPos[0], sandPos[1]+1)
            belowLeft = (sandPos[0]-1, sandPos[1]+1)
            belowRight = (sandPos[0]+1, sandPos[1]+1)
            placed = False
            if inBounds(below, grid) and inBounds(belowLeft, grid) and inBounds(belowRight, grid):
                if inBounds(below, grid) and grid[below[1]][below[0]] == ' ':
                    #spot below is free, move to it
                    moved = True
                    sandPos = below
                elif inBounds(belowLeft, grid) and grid[belowLeft[1]][belowLeft[0]] == ' ':
                    moved = True
                    sandPos = belowLeft
                elif inBounds(belowRight, grid) and grid[belowRight[1]][belowRight[0]] == ' ':
                    moved = True
                    sandPos = belowRight
                else:
                    #we cant move
                    grid[sandPos[1]][sandPos[0]] = 'o'
                    placedSand += 1
                    #printGrid(grid)
                    #time.sleep(.2)
            else:
                #one of the next destinations is out of bounds, so i think we are done checking.
                outOfBounds = True



    printGrid(grid)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()