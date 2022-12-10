import time

with open('Day04/input') as file:
    pairList = file.readlines()

start_time = time.time()

subSets = 0
overlap = 0
for pair in pairList:
    #split the lists into 2 sets of ranges
    pair = pair.strip().split(',')
    range1 = pair[0].split('-')
    range2 = pair[1].split('-')

    range1 = [*range(int(range1[0]), int(range1[1])+1 )]
    range2 = [*range(int(range2[0]), int(range2[1])+1)]
    
    #make a full range with no dupes
    fullRange = set(range1+range2)

    #if either range 1 or 2 equals the full range, one is a subset
    if (len(range1) == len(fullRange) or len(range2) == len(fullRange)):
        subSets+=1
    #If the full ranage is smaller than range 1+2 there was overlap.
    if (len(range1+range2) > len(fullRange)):
        overlap+=1

print(subSets)
print(overlap)
print("--- %s seconds ---" % (time.time() - start_time))