import time
import copy
from math import ceil

opString = ""

def operation(monkey1, operation, monkey2):
    if operation == '+': return monkey1 + monkey2
    if operation == '-': return monkey1 - monkey2
    if operation == '*': 
        if (monkey1*monkey2 == 0):
            print("Mul bu 0")
        return monkey1 * monkey2
    if operation == '/': return monkey1 // monkey2 
    if operation == '=': return monkey1 == monkey2 

def reverseOperation(monkey1, operation, monkey2):
    if operation == '+': return monkey2 - monkey1
    if operation == '-': return monkey1 + monkey2
    if operation == '*': return ceil(monkey2 // monkey1)
    if operation == '/': return monkey1 * monkey2

def SolveMonkey(monkey, monkeyDict):
    if monkeyDict[monkey] == None:
        return None
    if type(monkeyDict[monkey]) == int or type(monkeyDict[monkey]) == float:
        return monkeyDict[monkey]
    else:
        monkey1Value = SolveMonkey(monkeyDict[monkey][0], monkeyDict)
        monkey2Value = SolveMonkey(monkeyDict[monkey][2], monkeyDict)
        #this is only useful in part2, where if one of the monkeys in the chain is the human, we will cascade none back up
        if monkey1Value == None or monkey2Value == None:
            return None
        return operation(monkey1Value, monkeyDict[monkey][1], monkey2Value)

def SolveHuman(monkey, monkeyDict, finalNumber):
    if monkey == "humn":
        monkeyDict["humn"] = finalNumber
        print(finalNumber)
        return finalNumber
    else:
        currMonkey = monkeyDict[monkey]
        monkey1Value = SolveMonkey(monkeyDict[monkey][0], monkeyDict)
        monkey2Value = SolveMonkey(monkeyDict[monkey][2], monkeyDict)

        if monkey1Value == 8669 or monkey2Value == 8669:
            return None

        if monkey1Value == None:
            newFinal = reverseOperation(finalNumber, monkeyDict[monkey][1], monkey2Value)
            monkey1Value = SolveHuman(monkeyDict[monkey][0], monkeyDict, newFinal)
        elif monkey2Value == None:
            newFinal = reverseOperation(monkey1Value, monkeyDict[monkey][1], finalNumber)
            monkey2Value = SolveHuman(monkeyDict[monkey][2], monkeyDict, newFinal)

        #monkeyDict[monkey] = operation(monkey1Value, monkeyDict[monkey][1], monkey2Value)
        return operation(monkey1Value, monkeyDict[monkey][1], monkey2Value)

def SolveRoot(monkeyDict):

        monkey1Value = SolveMonkey(monkeyDict["root"][0], monkeyDict)
        monkey2Value = SolveMonkey(monkeyDict["root"][2], monkeyDict)

        if monkey1Value == None:
            monkey1Value = SolveHuman(monkeyDict["root"][0], monkeyDict, monkey2Value)
        elif monkey2Value == None:
            monkey2Value = SolveHuman(monkeyDict["root"][2], monkeyDict, monkey1Value)
        print(monkey1Value, monkey2Value)
        return operation(monkey1Value, monkeyDict["root"][1], monkey2Value)

def main(filePath):
    with open(filePath) as file:
        input = file.read()
    start_time = time.time()

    input  = [[name, instruction.split(' ')] for monkey in input.split('\n') for name, instruction in [monkey.split(': ')]]
    monkeyDict = {}
    for monkey in input:
        if len(monkey[1]) == 1:
            monkey[1] = int(monkey[1][0])
        monkeyDict[monkey[0]] = monkey[1]

    part1MonkeyDict = copy.deepcopy(monkeyDict)

    print("part 1:", SolveRoot(part1MonkeyDict))

    monkeyDict["root"][1] = "="
    monkeyDict["humn"] = None
    SolveRoot(monkeyDict)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main('Day21/input')
    print("Test")
    main('Day21/inputTest')