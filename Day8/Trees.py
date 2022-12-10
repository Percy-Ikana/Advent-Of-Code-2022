import time

#After doind this, i learned of complex, which is this, but built in, whoops.

with open('Day8/input') as file:
    inputList = file.readlines()

start_time = time.time()
#make it a proper 2d list
trees = [list(x.strip()) for x in inputList]
#Count the perimeter, sub 4 to account for corners getting counted twice
visibleCount = len(trees)*2 + len(trees[0])*2 - 4 
#Most Scenic Tree for part 2, (x, y, scenic score). Start out at 0
topScenic = (0,0,0)
#loop through and start summing visible trees, as well as thier scenic score.
visibleMap = [[' ' for y in trees[0]] for x in trees]
for row in range(1,len(trees)-1):
    for col in range(1,len(trees[row])-1):

        collum = [trees[x][col] for x in range(len(trees))]

        #this are the lists of currently relevant trees
        currentTree = trees[row][col]
        leftTrees = trees[row][:col]
        rightTrees = trees[row][col+1:]
        upTrees = collum[:row]
        downTrees = collum[row+1:]
        #reverse left and up for math in part 2, so that index 0 is the closest tree
        upTrees.reverse()
        leftTrees.reverse()

        #see if the tree is visibke (the tallest) from iself to any edge
        if (currentTree > max(leftTrees)) or (currentTree > max(rightTrees)) or (currentTree > max(upTrees)) or (currentTree > max(downTrees)):
            visibleCount += 1
            visibleMap[row][col] = 'V'

        #now for part 2, we check how "scenic" of a tree this one is
        #with 4 loops, one for each direction
        #left, we want to start FROM the tree we are looking at, which should be index 0 for all lists
        #scenic defaults to 1, since this is multipication based, and we make a lsit of the tree directions
        scenic = 1
        treeDirs = [leftTrees, rightTrees, upTrees, downTrees]
        for dir in range(len(treeDirs)):
            for tree in range(len(treeDirs[dir])):
                if currentTree <= treeDirs[dir][tree]:
                    #+1 to make the multipication work later
                    #humans count from 1 anyways
                    scenic *= tree+1
                    break
                elif tree == len(treeDirs[dir])-1:
                    #same as above, we just hit the end of the grove
                    scenic *= tree+1
                    break
        if topScenic[2] < scenic:
            topScenic = (row, col, scenic)
            
print("From the outside you can see", visibleCount, "trees!")
print("the most scenic tree is at postion (", topScenic[0], "," , topScenic[1], ") with a score of",topScenic[2])
print("--- %s seconds ---" % (time.time() - start_time))