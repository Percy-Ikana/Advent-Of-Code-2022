import time
with open('Day10/input') as file:

    start_time = time.time()

    cycleWait = 0
    power, xVal, xadd, xReg = 0, 0, 0, 1

    grid = [[" " for x in range(40)] for x in range(6)]

    #run for 240 cycles
    for cycle in range(1,241):
        if cycle%40 == 20:
            #add cycle*power to the powerList if we are at a correct cycle
            power+=(cycle*xReg)

        #sub cyclewait
        cycleWait -=1
        if cycleWait < 1:
            input = file.readline()
            input = input.strip().split()
            #op is index 0, number to add, if present, is index 1
            if input[0] == "noop":
                pass
            if input[0] == "addx":
                cycleWait=2
                xVal = input[1]
                #dont add till next cycle
                xAdd = cycle+1

        #Print the pixel, if it is with int span
        pxRange = [xReg-1, xReg, xReg+1]
        #cucle -1 because the scanner starts at 0 and ends at 39, while cycles start at 1 and "end" at 40
        if abs((cycle-1)%40) in pxRange:
            grid[int(cycle/40)][(cycle%40)-1] = '#'
        #if this is the right cycle, add to x reg.
        if cycle == xAdd:
            xReg += int(xVal)
            xAdd = -1
           
    for each in grid:
        print(''.join(each))

    print(power)
    print("--- %s seconds ---" % (time.time() - start_time))