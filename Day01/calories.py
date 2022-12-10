import time

with open('Day01/input') as file:
    foodList = file.readlines()

start_time = time.time()
elfCalorieList = []
cals = 0
elfNumber = 1
for snack in foodList:
    if snack == "\n":
        #this means that we are on the next elf, so add the current info to the list, and reset/inc the tracking vars
        elfCalorieList.append((elfNumber, cals))
        cals = 0
        elfNumber += 1
    else:
        #this means that we add the calories to the current elf (always the last in the list),
        cals += int(snack)

elfCalorieList.sort(key=lambda x: x[1])

print("The Elves with the top three calories are ", elfCalorieList[-3:])
print("The sum of the top three calories is ", sum(cal for (_, cal) in elfCalorieList[-3:]))
print("--- %s seconds ---" % (time.time() - start_time))