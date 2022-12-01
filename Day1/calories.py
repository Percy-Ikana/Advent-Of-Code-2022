with open('Day1/input') as file:
    foodList = file.readlines()

elfCalorieList = [0]
for snack in foodList:
    if snack == "\n":
        #this means that we are on the next elf
        elfCalorieList.append(0)
    else:
        #this means that we add the calories to the current elf
        elfCalorieList[len(elfCalorieList)-1] += int(snack)

#Look at the max element in the list, add it to the cal list, and print for posterity, 
#then EXTERMINATE it from the list, do agian 2 more times for top three
TopThreeCal = 0
for i in range(3):
    TopThreeCal += max(elfCalorieList)
    print("the most calories are " , max(elfCalorieList) , "on elf", elfCalorieList.index(max(elfCalorieList)))
    elfCalorieList[elfCalorieList.index(max(elfCalorieList))] = 0
print("the sum of the top three calories is ", TopThreeCal)



