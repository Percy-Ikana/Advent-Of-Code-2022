#https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
#Thanks wikipedia
import time
import sys
import copy

class Hike:
    def __init__(self, unvisited, visited, startingHills, endingHill, hillMap, hillNumber):
        #setup class info
        self.unvisited = unvisited
        self.visited = visited
        self.startingHills = startingHills
        self.endingHill = endingHill
        self.hillMap = hillMap
        #make a dict of each hill, and the distance to it, defaults to the max word size for the cpu, -1 to prevent overflow (not that python can overflow)
        self.hillDistances = dict(zip(unvisited, [sys.maxsize-1]*hillNumber))

    def visit_hill(self, currentHill, visited, unvisited, hillDistances):
        #for each valid next hill for the current hill
        for nextHill in self.hillMap[currentHill]:
            #check if we have been here before
            if nextHill not in self.visited:
                #check to make sure that the dist from this node, to the next, is the shortest (or equal to the shortest) that we have yet found.
                if hillDistances[currentHill] + 1 < hillDistances[nextHill]:
                    hillDistances[nextHill] = hillDistances[currentHill] + 1
        #remove the current hill from the unvisited list, place it on the visited list.
        unvisited.remove(currentHill)
        visited.append(currentHill)

    def hike(self):
        #go until we have visisted the ending hill
        hillDistList = []
        for startingHill in self.startingHills:
            visited = copy.deepcopy(self.visited)
            unvisited = copy.deepcopy(self.unvisited)
            hillDistances = copy.deepcopy(self.hillDistances)
            hillDistances[startingHill] = 0
            while not set(self.endingHill).issubset(set(visited)):
                #grab the smallest distance hill in the list of unvisited hills
                current_hill = min(unvisited, key=hillDistances.get)
                #visit it
                self.visit_hill(current_hill, visited, unvisited, hillDistances)
            hillDistList.append([hillDistances[x] for x in self.endingHill])
        return hillDistList

def main():
    with open('Day12/input') as file:
        hillMap = [list(x.strip()) for x in file.readlines()]
    start_time = time.time()

    startPosition, endPosition = [],[]
    unvisitedHills = []
    visitedHills = []
    hillValidVisitsAtoZ = dict()
    hillValidVisitsZtoA = dict()
    hillNumber = 0

    #find the start and ending hills, and mark them, Change the letter at thier pos to be a for S and z for E, so math works right
    for x in range(len(hillMap)):
        for y in range(len(hillMap[x])):
            #check if starting hill or ending hill. for part 1, change to just S, so that will be the only starting point.
            if  hillMap[x][y] in ['S', 'a']:
                startPosition.append((x, y))
                hillMap[x][y] = 'a'
            elif  hillMap[x][y] == 'E':
                endPosition.append((x, y))
                hillMap[x][y] = 'z'
            #Build the list of unvisited hills.
            unvisitedHills.append((x, y))
            hillNumber += 1

    for x in range(len(hillMap)):
        for y in range(len(hillMap[x])):
            #we are building a list of what hills are valid next stops from each individual hill
            validVisitableHills = [[],[]]
            #for x and Y, check the prev and next for if valid. Diags are not valid, so this algo never checks them
            for n in [x-1,x+1]:
                #make sure the new position is still on the list
                if 0 <= n < len(hillMap):
                    #a step up of one, or down of any is valid
                    if ord(hillMap[n][y]) - ord(hillMap[x][y]) <= 1:
                        validVisitableHills[0].append((n, y))
                    if ord(hillMap[n][y]) - ord(hillMap[x][y]) >= -1:
                        validVisitableHills[1].append((n, y))
            for n in [y-1, y+1]:
                if 0 <= n < len(hillMap[x]):
                    if ord(hillMap[x][n]) - ord(hillMap[x][y]) <= 1:
                        validVisitableHills[0].append((x, n))
                    if ord(hillMap[x][n]) - ord(hillMap[x][y]) >= -1:
                        validVisitableHills[1].append((x, n))
            hillValidVisitsAtoZ[(x, y)] = validVisitableHills[0]
            hillValidVisitsZtoA[(x, y)] = validVisitableHills[1]
    
    #run the hike to find the easiest path
    graphPt2 = Hike(unvisitedHills, visitedHills, endPosition, startPosition, hillValidVisitsZtoA, hillNumber)
    graphPt1 = Hike(unvisitedHills, visitedHills, [(20,0)], endPosition,  hillValidVisitsAtoZ, hillNumber)
    
    print("The shortest path to the best signial is:", min(dist for distList in graphPt1.hike() for dist in distList))
    print("The shortest path from any bottom to the top is", min(dist for distList in graphPt2.hike() for dist in distList))
    
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()