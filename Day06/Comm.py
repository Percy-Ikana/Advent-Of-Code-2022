import time

def detectCommString(str, length):
    #ensure the string is actually long enough
    if len(str) > length:
        #slice the last length elements from the string, and see if the set of them is equal to the length
        if len(set(str[-length:])) == length:
            #if yes, we have the position
            return len(str)
    return 0

with open('Day06/input') as file:
    start_time = time.time()
    #read 3 elements, this isnt needed, but like, why not?
    inputList = file.read(3)
    commLength = [4, 14]
    partsSolved = [False for x in commLength]
    lastSize = 0
    #while both problems not solved
    while not all(partsSolved):
        lastSize = len(inputList)
        inputList = inputList + file.read(1)
        #break if we are done with the file, or if no \n, if the string is the same size as last loop
        if inputList[-1] == '\n' or lastSize == len(inputList):
            break
        #Check for part 1 and 2 solutions
        for i in range(len(commLength)):
            if not partsSolved[i]:
                pos = detectCommString(inputList, commLength[i])
                if pos !=0:
                    print("Part ",i,": ", pos)
                    partsSolved[i] = True
    print("--- %s seconds ---" % (time.time() - start_time))