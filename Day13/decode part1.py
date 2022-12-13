import time
from ast import literal_eval
import functools

def inOrder(left, right):
    determineShorterList = lambda l, r: l if (len(l) < len(r)) else r

    #if they are equal we actually dont care
    shortestList = determineShorterList(left, right)

    isInOrder = 'undefined'
    ranOut = False
    for index in range(len(shortestList)):
        if not isInOrder:
            break
        if isinstance(left[index], int) and isinstance(right[index], int):
            #Okay, this needs to check UNTIL left is smaller than right, then it stops
            if left[index] < right[index]:
                return True
            elif left[index] > right[index]:
                return False
        elif isinstance(left[index], list) and isinstance(right[index], list):
            isInOrder = inOrder(left[index], right[index])
            if isInOrder != 'undefined':
                return isInOrder
        elif isinstance(left[index], list):
            isInOrder = inOrder(left[index], [right[index]])
            if isInOrder != 'undefined':
                return isInOrder
        elif isinstance(right[index], list):
            isInOrder = inOrder([left[index]], right[index])
            if isInOrder != 'undefined':
                return isInOrder

    #if we got here it means we ran out of items, so check list lengths.
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False
    return 'undefined'

def compare(left, right):
    equal = inOrder(left, right)
    if equal:
        return -1
    elif not equal:
        return 1
    else:
        return 0

def main():
    with open('Day13/input') as file:
        input = file.read()

    start_time = time.time()

    #part 1
    part1Lists = [x.split('\n') for x in input.split('\n\n')]
    #This should be able to be one line, not sure why it broke. fix later
    part1Lists = [[literal_eval(y),literal_eval(z)] for y, z in part1Lists]

    inOrderPairs = []
    for left, right in part1Lists:
        #check lengths
        if inOrder(left, right):
            inOrderPairs.append(part1Lists.index([left,right])+1)

    #now for part 2
    part2List = [x for x in input.split('\n')]
    #This should be able to be one line, not sure why it broke. fix later
    part2List = [literal_eval(y) for y in part2List if y != '']
    #add the decode keys to the list
    part2List.append([[2]])
    part2List.append([[6]])
    #sort using a comp function, using the in order from part 1
    part2List.sort(key = functools.cmp_to_key(compare))
    #calculate the key, which is index of the two keys mul together
    decodeKey = (part2List.index([[2]])+1)*(part2List.index([[6]])+1)

    #print answers
    print("Total In Order Pairs:", sum(inOrderPairs))
    print("Decode Key:", decodeKey)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()