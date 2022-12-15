import time
import sys

sign = lambda a: 1 if a>0 else -1 if a<0 else 0

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

distance =lambda pointOne, pointTwo: abs(pointOne[0] - pointTwo[0]) + abs(pointOne[1] - pointTwo[1])

def findBoundingBox(point, dist):
    minPos = [sys.maxsize,sys.maxsize]
    maxPos = [-sys.maxsize,-sys.maxsize]

    minPos[0] = point[0] - dist
    maxPos[0] = point[0] + dist

    minPos[1] = point[1] - dist
    maxPos[1] = point[1] + dist

    return (minPos, maxPos)

#returns two points denoting the intersection between two rectangles
def findIntersection(box1, box2):
    minPos = [0,0]
    maxPos = [0,0]

    #min X
    if box1[0][0] < box2[0][0]:
        minPos[0] = box2[0][0]
    else:
        minPos[0] = box1[0][0]
    #max x
    if box1[1][0] > box2[1][0]:
        maxPos[0] = box2[1][0]
    else:
        maxPos[0] = box1[1][0]

    #min Y
    if box1[0][1] < box2[0][1]:
        minPos[1] = box2[0][1]
    else:
        minPos[1] = box1[0][1]
    #max Y
    if box1[1][1] > box2[1][1]:
        maxPos[1] = box2[1][1]
    else:
        maxPos[1] = box1[1][1]

    return (minPos, maxPos)

#finds all known positions, but really friggin slowly.
def bruteForce(sensorDict, beaconSet, minPos, maxPos):
    lineKnownPositions = set({})
    for x in range(minPos[0], maxPos[0]+1):
        print((x+abs(minPos[0]))/(abs(minPos[0])+maxPos[0]), "done")
        for y in range(minPos[1], maxPos[1]+1):
            #for evey point on this grid, if it is not already a sensor or beacon, check if it is "known", aka, in distance of at least one sensor
            known = False
            if (x,y) not in sensorDict and (x,y) not in beaconSet:
                for sensor in sensorDict:
                    dist = distance(sensor, (x,y))
                    if dist <= sensorDict[sensor]:
                        known = True
                        break
                if known:
                    lineKnownPositions.add((x,y))
    return lineKnownPositions

#finds all known positions, I cant think of a way to make it faster, but this is still painfully slow.
#this improves on the above by only checking the points around each sensor, not all points within the min/max bounding box
def smartFind(sensorDict, beaconSet):
    lineKnownPositions = set({})
    for sensor in sensorDict:
        bounding = findBoundingBox(sensor, sensorDict[sensor])
        for x in range(bounding[0][0], bounding[1][0]+1):
            for y in range(bounding[0][1], bounding[1][1]+1):
                dist = distance((x,y), sensor)
                if dist <= sensorDict[sensor] and (x,y) not in beaconSet:
                    lineKnownPositions.add((x,y))
    return lineKnownPositions

#finds all positions with a specified Y range
def smartSmartFind(sensorDict, beaconSet, searchArea):
    lineKnownPositions = set({})
    total = len(sensorDict)
    parsed = 0
    for sensor in sensorDict:
        print(parsed/total, "done")
        parsed+=1
        bounding = findBoundingBox(sensor, sensorDict[sensor])
        bounding = findIntersection(bounding, searchArea)
        for x in range(bounding[0][0], bounding[1][0]+1):
            for y in range(bounding[0][1], bounding[1][1]+1):
                dist = distance((x,y), sensor)
                if dist <= sensorDict[sensor]:
                    if (x,y) not in beaconSet:
                        lineKnownPositions.add((x,y))
    return lineKnownPositions

#finds all positions with a specified Y range
def emptyFindFind(sensorDict, beaconSet, searchArea):
    unknownPositions = set({})
    for sensor in sensorDict:
        bounding = findBoundingBox(sensor, sensorDict[sensor])
        bounding = findIntersection(bounding, searchArea)
        for x in range(bounding[0][0]-1, bounding[1][0]+2):
            for y in range(bounding[0][1]-1, bounding[1][1]+2):
                dist = distance((x,y), sensor)
                if dist == sensorDict[sensor]+1:
                    #this is an unknown position, for thi
                    if (x,y) not in beaconSet or (x,y) not in sensorDict:
                        unknownPositions.add((x,y))
    for position in unknownPositions:
        for sensor in sensorDict:
            knownpos = smartSmartFind(sensorDict, beaconSet, findBoundingBox(sensor, sensorDict[sensor]))
    return unknownPositions - knownpos

def findEmptySpotsWithinArea(sensorDict, beaconSet, searchArea):
    empty = set({})
    filled = fillLines(sensorDict, beaconSet, searchArea)
    for x in range(searchArea[0][0], searchArea[1][0]):
        for y in range(searchArea[0][1], searchArea[1][1]):
            if (x,y) not in sensorDict and  (x,y) not in beaconSet:
                empty.add((x,y))

    return (empty - filled)

def findMinAndMaxCords(box1, box2):
    minPos = [0,0]
    maxPos = [0,0]

    #min X
    if box1[0][0] > box2[0][0]:
        minPos[0] = box2[0][0]
    else:
        minPos[0] = box1[0][0]
    #max x
    if box1[1][0] < box2[1][0]:
        maxPos[0] = box2[1][0]
    else:
        maxPos[0] = box1[1][0]

    #min Y
    if box1[0][1] > box2[0][1]:
        minPos[1] = box2[0][1]
    else:
        minPos[1] = box1[0][1]
    #max Y
    if box1[1][1] < box2[1][1]:
        maxPos[1] = box2[1][1]
    else:
        maxPos[1] = box1[1][1]

    return (minPos, maxPos)

def fillLines(sensorDict, beaconSet, searchArea):
    lines = {}
    #for each Y line in the search area, with this, X values kinda just dont matter TBH, ill cut them out later
    for y in range(searchArea[0][1], searchArea[1][1]+1):
        singleLine = set({})
        lines[y] = set({})
        for sensor in sensorDict:
            x = sensor[0]
            adjustedDist = sensorDict[sensor] - distance(sensor, (sensor[0], y))
            if adjustedDist >= 0:
                singleLine.add((max(x-adjustedDist, searchArea[0][0]), min(x+adjustedDist, searchArea[1][0])))
        #we have a list of tuples, so now we just need to convert that into a set of ranges
        #this is every point within the 
        #for taken in sorted(singleLine):
        #    for x in range(taken[0], taken[1]+1):
        #        lines[y].add((x, y))
        singleLine = sorted(singleLine)
        actualComp = 1
        for each in range(1, len(singleLine)):
            newRanges = combineRanges(singleLine[actualComp-1], singleLine[each])
            if len(newRanges) == 1:
                singleLine[actualComp-1] = newRanges[0]
            else:
                singleLine[actualComp-1] = newRanges[0]
                singleLine[actualComp] = newRanges[1]
                actualComp += 1


        lines[y] = set(singleLine[:actualComp])
    return lines

#if two sets overlap, this combines them into a single range
#this assumes the first set starts before the second set, and will not work otherwise
def combineRanges(set1, set2):
    start = 0
    end = 0
    #if the second sets start is less than the first sets end
    if set2[0] <= set1[1]+1:
        start = set1[0]
        #we check if the sets overlap
        if set2[1] <= set1[1]:
            end = set1[1]
        else:
            end = set2[1]
        return [(start,end)]
    else:
        #sets are either out of order, or not overlapping
        return [set1, set2]

def main():
    with open('Day15/input') as file:
        input = file.read()
    start_time = time.time()

    #parse the input. I did it this way to see if i could, I dont like it.
    sensorsAndBeacons = [ [(int(sensorPos[0].split('=')[1][:-1]),int(sensorPos[1].split('=')[1])),(int(beaconPos[0].split('=')[1][:-1]),int(beaconPos[1].split('=')[1]))] for line in input.split('\n') for sensor, beacon in [line.split(':')] for sensorPos, beaconPos in [[sensor.split(' ')[-2:], beacon.split(' ')[-2:]]]]
    
    #dict of sensors, the position is a key to the distance to the nearest sensor
    sensorDict = {}
    #this is just a set, we use this to determine if a spot is alredy occupied, basically.
    beaconSet = set({})

    minPos = [sys.maxsize,sys.maxsize]
    maxPos = [-sys.maxsize,-sys.maxsize]

    #build up the two sets
    #we can user the farthest in each direction (x,y) pair that is worth checking
    #we do this by iterating over the sensor list, and using the dist param as a modifier to see what points might matter
    for pair in sensorsAndBeacons:
        dist = distance(pair[0], pair[1])
        sensorDict[pair[0]] = dist
        beaconSet.add(pair[1])
        box = findBoundingBox(pair[0], dist)
        minPos, maxPos = findMinAndMaxCords(box, (minPos,  maxPos))

    #so we now have a list of sensors and thier distances, a list of beacons, and a bounding box of points to check
    #lineKnownPositions = bruteForce(sensorDict, beaconSet, minPos, maxPos)
    
    #part1Ranges = fillLines(sensorDict, beaconSet, [(-sys.maxsize, 10),(sys.maxsize,10)])
    part1Ranges = fillLines(sensorDict, beaconSet, [(-sys.maxsize, 2000000),(sys.maxsize,2000000)])
    scannedPositions = 0
    countedSensorsAndBeacons = 0
    for yPos in part1Ranges.keys():
        countedBeacons = [x for x in beaconSet if x[1] == yPos]
        countedSensors = [x for x in sensorDict if x[1] == yPos]
        countedSensorsAndBeacons += len(countedBeacons) + len(countedSensors)
        for radarRange in part1Ranges[yPos]:
            scannedPositions += (radarRange[1] - radarRange[0]) + 1
    scannedPositions -= countedSensorsAndBeacons

    print(scannedPositions)
    print("--- %s seconds ---" % (time.time() - start_time))
   
    #partTwoAnswer = fillLines(sensorDict, beaconSet, [(0, 0),(20,20)])
    xpos = 0
    ypos = 0
    partTwoAnswer = fillLines(sensorDict, beaconSet, [(0, 0),(4000000,4000000)])
    #partTwoAnswer = fillLines(sensorDict, beaconSet, [(0, 0),(20,20)])
    for key in partTwoAnswer.keys():
        if len(partTwoAnswer[key]) == 2:
            xpos = list(partTwoAnswer[key])[0][1] + 1
            ypos = key
    print(xpos*4000000 + ypos)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()