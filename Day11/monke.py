import time
with open('Day11/input') as file:
    inputList = [x.split('\n') for x in file.read().split('\n\n')]

start_time = time.time()
factor = 1
for monkey in inputList:
    monkey[0] = monkey[0].split(' ')[-1][:-1]
    monkey[1] = [int(x) for x in monkey[1].split(':')[-1].split(',')]
    monkey[3] = int(monkey[3].split(' ')[-1])
    monkey[4] = int(monkey[4].split(' ')[-1])
    monkey[5] = int(monkey[5].split(' ')[-1])
    monkey[2] = monkey[2].split(' ')[-3:]
    #this makes a number equal to all the tests, we can modulo by this, and keep numbers in check.
    factor *= monkey[3]
    #One more item for count
    monkey.append(0)

#monkey#
#items
#operation
#test
#if test true
#if test false
#items thrown

#for part one this should be 20
for x in range(0, 10000):
    for monkey in inputList:
        #for each monkey per round
        for item in monkey[1]:
            #for each item the monkey holds
            #make this a lamda function
            op1 = 0
            op2 = 0
            monkey[6] +=1
            if monkey[2][0] == "old":
                op1 = int(item)
            else:
                op1 = int(monkey[2][0])
            if monkey[2][2] == "old":
                op2 = int(item)
            else:
                op2 = int(monkey[2][2])
            if monkey[2][1] == '*':
                item = op1 * op2
                pass
            if monkey[2][1] == '+':
                item = op1+op2
            #part1 is item = item//3
            item %= factor
            #apply test
            if item % monkey[3] == 0:
                #true
                inputList[monkey[4]][1].append(item)
            else:
                #false 
                inputList[monkey[5]][1].append(item)
        monkey[1] = []
            
max = []
for monkey in inputList:
    max.append((monkey[0],monkey[6]))

max.sort()

print(max[-1][1]*max[-2][1])
print("--- %s seconds ---" % (time.time() - start_time))