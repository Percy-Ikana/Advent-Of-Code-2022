import time
import copy

getSign = lambda x : -1 if x < 0 else 1# if x > 0 else 0

class Number:
    def __init__(self, number) -> None:
        self.number = number

def mixList(input, timesToMix):
    orginalList = [Number(x) for x in input]
    mixedList = [x for x in orginalList]

    listLength = len(input)
    for mix in range(timesToMix):
        for element in range(0,listLength):
            mix = orginalList[element]
            currentMixIndex = mixedList.index(mix)
            newMixIndex = currentMixIndex + (abs(mix.number)%(listLength-1)*getSign(mix.number))
            if newMixIndex >=listLength:
                newMixIndex = (newMixIndex%listLength)+1
            if newMixIndex != currentMixIndex:
                mixedList.remove(mix)
                mixedList.insert(newMixIndex, mix)
    numList = [x.number for x in mixedList]
    return numList

def main(filePath):
    with open(filePath) as file:
        input = file.read()
    start_time = time.time()
    key = 811589153
    input = [int(line.strip()) for line in input.split('\n')]
    inputPart2 = [x*key for x in input]

    numList = mixList(input, 1)
    numList2 = mixList(inputPart2, 10)

    sumsPt1 = 0
    sumsPt2 = 0
    zeroIndexPt1 = numList.index(0)
    zeroIndexPt2 = numList2.index(0)
    for x in [1000,2000,3000]:
        sumsPt1 += numList[(x+zeroIndexPt1+1)%len(numList)-1]
        sumsPt2 += numList2[(x+zeroIndexPt2+1)%len(numList2)-1]
    print(sumsPt1, sumsPt2)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main('Day20/input')
    #main('Day20/inputTest')