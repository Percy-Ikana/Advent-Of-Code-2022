import time

def generateRocks():
    rocks = [[],[],[],[],[]]
    rocks[3] = ([(0,0),(0,1),(0,2),(0,3)])
    rocks[1] = ([(0,1),(1,0),(1,1),(1,2),(2,1)])
    rocks[2] = ([(0,0),(1,0),(2,0),(2,1),(2,2)])
    rocks[0] = ([(0,0),(1,0),(2,0),(3,0)])
    rocks[4] = ([(0,0),(0,1),(1,0),(1,1)])

    return rocks

def printGrid(grid):
    graph = ''
    minPos = (min(grid, key=lambda x: x[0])[0],min(grid, key=lambda y: y[1])[1])
    maxPos = (max(grid, key=lambda x: x[0])[0],max(grid, key=lambda y: y[1])[1])
    for y in range(maxPos[1], minPos[1]-1, -1):
        for x in range(1, 7+1):
            if (x,y) in grid:
                graph = graph+"#"
            else:
                graph = graph + '.'
        graph = graph + '\n'
    return graph

#returns if in bounds in the form of a modificaion to positoin, this is bad, but im doing it anyways
def checkJetBounds(rock, positon, jet, xBounds, grid):
    inBounds = True
    xMod = 0
    xPos = positon[0]
    if jet == '<':
        xMod = -1
    else:
        xMod = 1

    for point in rock:
        if point[0] + xMod + xPos < xBounds[0]:
            inBounds = False
        elif point[0] + xMod + xPos > xBounds[1]:
            inBounds = False
        if (point[0] + xMod + xPos, positon[1]+point[1]) in grid:
            inBounds = False
    if inBounds:
        return xMod
    else:
        return 0

def canDrop(rock, position, grid):
    for point in rock:
        newPoint = (point[0]+position[0] , point[1]-1+position[1])
        if newPoint in grid or newPoint[1] < 1:
            #cant move
            return False
    return True

def main():
    with open('Day17/input') as file:
        input = file.read()
    start_time = time.time()

    grid = set()
    rocks = generateRocks()
    #these bounds are inclusive, cannot go beyond
    #not mutable
    xBounds = (1,7)
    #mutable, the second positon is where the rocks spawn in the Y axis, they always apwan at X 3
    yBounds = [1, 4]
    
    fallenRocks = 0
    instruction = 0


    firstRock = True
    firstRockPos = set()

    rockCombos = {}

    #if we ever have a position where the X values of a bar rock match the first one, and that was the last input, we can end
    for fallenRocks in range(1000000000000):
        if fallenRocks % 100000 == 0:
            print(fallenRocks//1000000000000)
        #Whats the current fallen rock
        rock = rocks[fallenRocks%5]
        position = [3, yBounds[1]]
        
        if instruction != 0 and (fallenRocks%5, instruction%len(input)) not in rockCombos.keys():
            rockCombos[(fallenRocks%5, instruction%len(input))] = (fallenRocks, max(grid, key=lambda y: y[1])[1])
        elif instruction != 0 and (fallenRocks%5, instruction%len(input)) in rockCombos.keys():
            previousRock, oldHeight = rockCombos[(fallenRocks%5, instruction%len(input))]
            cycleLen = fallenRocks - previousRock
            if previousRock % cycleLen == 1000000000000%cycleLen:
                print("cycle Found",cycleLen, previousRock - fallenRocks)
                loopHeight = max(grid, key=lambda y: y[1])[1] - oldHeight
                remains = 1000000000000 - fallenRocks
                cyclesLeft = remains//cycleLen
                print(max(grid, key=lambda y: y[1])[1] + loopHeight*cyclesLeft)
                break
            pass

        lastRockPos = set()
        while True:
                #we first apply the checks, moving according to the jet, then moving down, or trying to.
                jetDir = input[instruction%len(input)]
                instruction+=1
                #Move if we can, for the jets
                move = checkJetBounds(rock, position, jetDir, xBounds, grid)
                position[0] += move
                #now check if we can move down
                if canDrop(rock, position , grid):
                    position[1] -=1
                else:
                    #add this rock to the grid, and start the next one
                    for point in rock:
                        grid.add((point[0]+position[0], point[1]+position[1]))
                        lastRockPos.add(point[0]+position[0])
                    yBounds[1] = max(grid, key=lambda y: y[1])[1] + 4
                    if firstRock:
                        firstRock = False
                        for x in grid:
                            firstRockPos.add(x[0])
                    if firstRockPos == lastRockPos:
                        #print(max(grid, key=lambda y: y[1])[1], fallenRocks)
                        if instruction%len(input) == 0 and instruction != 0:
                          pass  
                    break

    print(max(grid, key=lambda y: y[1])[1])
    with open('Day17/output', "w") as file:
        file.write(printGrid(grid))
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    main()