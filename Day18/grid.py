import time
import copy 
import sys

#this code is ugly dont look at it.
#part 2 reuses some of the code form the hills, distrikas algo, although a plain BFS would have been enough.

class Hike:
    def __init__(self, unvisited, visited, startingHills, endingHill, hillMap, hillNumber):
        #setup class info
        self.unvisited = unvisited
        self.visited = visited
        self.startingHills = startingHills
        self.endingHill = endingHill
        self.hillMap = hillMap
        #make a dict of each hill, and the distance to it, defaults to the max word size for the cpu, -1 to prevent overflow (not that python can overflow)
        self.hillDistances = dict(zip(hillNumber, [sys.maxsize-1]*len(hillNumber)))

    def visit_hill(self, currentHill, visited, unvisited, hillDistances):
        #for each valid next hill for the current hill
        for x in range(-1,2):
            for y in range(-1,2):
                for z in range(-1,2):
                    #fuck corners
                    if (abs(x) + abs(y) + abs(z)) == 1:
                        nextHill = (x+currentHill[0],y+currentHill[1],z+currentHill[2])
                        if nextHill not in self.visited and nextHill in hillDistances:
                            #check to make sure that the dist from this node, to the next, is the shortest (or equal to the shortest) that we have yet found.
                            if hillDistances[currentHill] + 1 < hillDistances[nextHill]:
                                hillDistances[nextHill] = hillDistances[currentHill] + 1
                        else:
                            #this is a void spot, sp dont change the dist
                            pass
        #remove the current hill from the unvisited list, place it on the visited list.
        unvisited.remove(currentHill)
        visited.add(currentHill)

    def hike(self):
        #go until we have visisted the ending hill
        hillDistList = []
        checked = 1
        for startingHill in self.startingHills:
            print("checked", checked, "out of", len(self.startingHills))
            print("--- %s seconds ---" % (time.time()))
            checked+=1
            visited = copy.deepcopy(self.visited)
            unvisited = copy.deepcopy(self.unvisited)
            hillDistances = copy.deepcopy(self.hillDistances)
            hillDistances[startingHill] = 0
            while not set(self.endingHill).issubset(set(visited)):
                #grab the smallest distance hill in the list of unvisited hills
                current_hill = min(unvisited, key=hillDistances.get)
                if hillDistances[current_hill] == sys.maxsize-1:
                    break
                #visit it
                self.visit_hill(current_hill, visited, unvisited, hillDistances)
            
            hillDistList= [[x, hillDistances[x]] for x in self.endingHill]
        return hillDistList


def checkFace(square, grid):
    faces = {"uncovered":set(), "covered":set()}
    for x in range(-1,2):
        for y in range(-1,2):
            for z in range(-1,2):
                #fuck corners
                if (abs(x) + abs(y) + abs(z)) == 1:
                    faceCheck = (square[0]+x,square[1]+y,square[2]+z)
                    if faceCheck in grid:
                        faces["covered"].add(faceCheck)
                    else:
                        faces["uncovered"].add(faceCheck)
    return faces

def searchCube(point, grid, minPos, maxPos):
    #see if a point just outside the min bounds can be reached without crossing over 
    pass

def main():
    with open('Day18/input') as file:
        input = file.read()
    start_time = time.time()

    squares = [(int(x),int(y),int(z)) for line in input.split('\n') for x,y,z in [line.split(',')]]

    grid = set()

    for square in squares:
        grid.add(square)

    minPos = (min(grid, key=lambda x: x[0])[0],min(grid, key=lambda y: y[1])[1], min(grid, key=lambda z: z[2])[2])
    maxPos = (max(grid, key=lambda x: x[0])[0],max(grid, key=lambda y: y[1])[1],max(grid, key=lambda z: z[2])[2])

    uncoveredFaces = 0
    emptyPositions = set()
    for square in grid:
        faces = checkFace(square, grid) 
        for face in faces["uncovered"]:
            emptyPositions.add(face)
        uncoveredFaces += len(faces["uncovered"])

    #this basically checks a cube, which means we are still getting the "corners" that are not relevant
    emptyPositions = [x for x in emptyPositions if (minPos[0] < x[0] < maxPos[0]) and (minPos[1] < x[1] < maxPos[1]) and (minPos[2] < x[2] < maxPos[2])]

    print(uncoveredFaces)
    print("--- %s seconds ---" % (time.time() - start_time))

    minPos = (min(emptyPositions, key=lambda x: x[0])[0],min(emptyPositions, key=lambda y: y[1])[1], min(emptyPositions, key=lambda z: z[2])[2])
    maxPos = (max(emptyPositions, key=lambda x: x[0])[0],max(emptyPositions, key=lambda y: y[1])[1],max(emptyPositions, key=lambda z: z[2])[2])


    bounds = set()
    for x in range(minPos[0]-1,maxPos[0]+2):
        for y in range(minPos[1]-1,maxPos[1]+2):
            for z in range(minPos[2]-1,maxPos[2]+2):
                bounds.add((x,y,z))

    unvisited = bounds - grid#emptyPositions
    hike = Hike(unvisited, set(), {(minPos[0]-1, minPos[1]-1, minPos[2]-1)}, emptyPositions, grid,  bounds)
    test = hike.hike()
    test2 = [x[0] for x in test if x[1] == sys.maxsize-1]

    dupeFaces = 0
    for each in test2:
        dupe = checkFace(each, grid)["covered"]
        dupeFaces += len(dupe)

    print(uncoveredFaces - (dupeFaces))
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    main()