with open('input') as file:
    lines = file.readlines()

elfCalorieList = [0]
mostPackedElfNumber = 0
for line in lines:
    if line == "\n":
        #this means that we are on the next elf
        elfCalorieList.append(0)
    else:
        #this means that we add the calories to the current elf
        elfCalorieList[len(elfCalorieList)-1] += int(line)

TopThreeCal = max(elfCalorieList)
print("the most calories are " , max(elfCalorieList) , "on elf", elfCalorieList.index(max(elfCalorieList)))
elfCalorieList[elfCalorieList.index(max(elfCalorieList))] = 0
TopThreeCal += max(elfCalorieList)
print("the second most calories are " , max(elfCalorieList) , "on elf", elfCalorieList.index(max(elfCalorieList)))
elfCalorieList[elfCalorieList.index(max(elfCalorieList))] = 0
TopThreeCal += max(elfCalorieList)
print("the third calories are " , max(elfCalorieList) , "on elf", elfCalorieList.index(max(elfCalorieList)))
print("the sum of the top three calories is ", TopThreeCal)



