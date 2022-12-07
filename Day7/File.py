import time

with open('Day7/input') as file:
    inputList = file.readlines()

start_time = time.time()
#$
#   - cd
#       - argument
#   - ls
#dir
#   - directory name
#numbers (file size)
#   - filename

#inital setup, since we start in
currentDir = '/'
fileDict = {'/': []}
sizeDict = {'/': 0}
for i in range(len(inputList)):
    #see above to understand what each index would be for each case
    input = inputList[i].split()
    if input[0] == '$':
        #this is a command, either a cd or ls
        #I actually dont thik we care about doing anything with ls
        if input[1] == "cd":
            #we not need to change into the specified directory, if it exists
            if input[2] == '/':
                #back to root. This is actually pointless, it only seems to occur once, at the start
                currentDir = '/'
            elif input[2] == "..":
                #Split the current dir into indexes, and drop the last one, this simulates moving to the parent.
                currentDir = "\\".join(currentDir.split('\\')[:-1])
            else:
                #this is a directory we need to check and switch to
                newDir = currentDir + '\\' + input[2]
                if newDir in fileDict.keys():
                    currentDir = currentDir + '\\' + input[2]
                else:
                    print("Directory ", newDir, " is not known try ls, or prehaps it does not exist")
        elif input[1] == "ls":
            #parse until we get a another command, setting things up as needed
            while (i+1 < len(inputList)) and (inputList[i+1][0] != '$'):
                i+=1
                input = inputList[i].split()
                if input[0] == 'dir':
                    newDir = currentDir + '\\' + input[1]
                    if newDir not in fileDict.keys():
                        fileDict[newDir] = []
                        sizeDict[newDir] = 0
                elif input[0] != '$':
                    #This means its a file with a size, place it in the list
                    #a tuple, with the size and name, in that order
                    file = (int(input[0]), input[1])
                    fileDict[currentDir].append(file)
                    sizeDict[newDir] += file[0]
                else:
                    #the next input was just a command, set i back so the loop goes as normal
                    i -=1

#Build up the dictonary of file sizes, we already have the totals for the files at each level
for key in fileDict.keys():
    keyDirs = key.split('\\')
    for dir in keyDirs:
        directory = '\\'.join(keyDirs[:keyDirs.index(dir)+1])
        sizeDict[directory] += sizeDict[key]

#part 1 var
totalUnderHundoK = 0
#part 2 vars
maxSpace = 70000000
minFreeSpace = 30000000
smallestDeleteDir = '/'
#loop for the counts as needed
for key in sizeDict:
    #part 1
    if sizeDict[key] <= 100000:
        totalUnderHundoK += sizeDict[key]
    #part 2
    freeSpace = maxSpace - (sizeDict['/'] - sizeDict[key])
    if freeSpace > minFreeSpace:
        if sizeDict[key] < sizeDict[smallestDeleteDir]:
            smallestDeleteDir = key

#part1
print("Files under 100,000: ", totalUnderHundoK)
#part2
print("The smallest dir that can be deleted for the update is " , 
    smallestDeleteDir, " with a size of ",sizeDict[smallestDeleteDir])
print("--- %s seconds ---" % (time.time() - start_time))