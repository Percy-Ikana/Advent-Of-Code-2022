import time
with open('Day7/input') as file: inputList = file.readlines()
start_time = time.time()
currentDir, fileDict, sizeDict = '/', {'/': []}, {'/': 0}
for i in range(len(inputList)):
    input = inputList[i].split()
    if input[0] == '$':
        if input[1] == "cd":
            if input[2] == '/':currentDir = '/'
            elif input[2] == "..":currentDir = "\\".join(currentDir.split('\\')[:-1])
            else:
                newDir = currentDir + '\\' + input[2]
                if newDir in fileDict.keys(): currentDir = currentDir + '\\' + input[2]
                else: print("Directory ", newDir, " is not known try ls, or prehaps it does not exist")
        elif input[1] == "ls":
            while (i+1 < len(inputList)) and (inputList[i+1][0] != '$'):
                i+=1
                input = inputList[i].split()
                if input[0] == 'dir':
                    newDir = currentDir + '\\' + input[1]
                    if newDir not in fileDict.keys():
                        fileDict[newDir] = []
                        sizeDict[newDir] = 0
                elif input[0] != '$':
                    file = (int(input[0]), input[1])
                    fileDict[currentDir].append(file)
                    sizeDict[newDir] += file[0]
                else: i -=1
for key in fileDict.keys(): 
    for dir in key.split('\\'): sizeDict['\\'.join(key.split('\\')[:key.split('\\').index(dir)+1])] += sizeDict[key]
smallestDeleteDir, totalUnderHundoK, maxSpace, minFreeSpace = '/', 0, 70000000, 30000000
for key in sizeDict:
    if sizeDict[key] <= 100000: totalUnderHundoK += sizeDict[key]
    freeSpace = maxSpace - (sizeDict['/'] - sizeDict[key])
    if freeSpace > minFreeSpace: 
        if sizeDict[key] < sizeDict[smallestDeleteDir]: smallestDeleteDir = key
print("Sum OF dirs with a size under 100,000: ", totalUnderHundoK)
print("The smallest dir that can be deleted for the update is " , smallestDeleteDir, " with a size of ",sizeDict[smallestDeleteDir])
print("--- %s seconds ---" % (time.time() - start_time))