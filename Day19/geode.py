import time
import copy 
import sys

simCount = 0

#This is unfinished

class Simulation:
    def __init__(self, blueprint, robots, resources, simMin, timelimit, maxResourcesNeeded):
        self.blueprint = blueprint
        self.robots = copy.deepcopy(robots)
        self.resources = copy.deepcopy(resources)
        self.simMin = copy.deepcopy(simMin)
        self.timeLimit = timelimit
        self.maxResourcesNeeded = maxResourcesNeeded

    def runMin(self, simulation):
        #if we are out of time, we return the amount of geodes collected
        if simulation.simMin == simulation.timeLimit+1:
            #print(simulation.resources["Geode"])
            return simulation.resources["Geode"]
        #lets check if we can build any robots, and if we can, launch a sim for *each*, along with one where nothing is built (to save up for a diffrent robot)
        #but this loop just determins what we can build BEFORE collecting resources
        #this var holds the buildable robots and the new resource totals after its built. We also have the 
        buildableBots = []
        for robot in self.robots:
            #if we can build this robot, and dont have MORE OF THEM THAN COULD EVER BE NEEDED
            if simulation.canBuild(robot) and simulation.robots[robot] < simulation.maxResourcesNeeded[robot]:
                newResources = simulation.collectResources()
                buildableBots.append(simulation.BuildBot(robot, newResources))

        #collect GEMS
        simulation.resources = simulation.collectResources()
        buildableBots.append((simulation.robots, simulation.resources))
        #progress
        GeodeCounts = []
        for path in buildableBots:
            GeodeCounts.append(simulation.runMin(Simulation(simulation.blueprint,path[0],path[1],(simulation.simMin+1), simulation.timeLimit, simulation.maxResourcesNeeded)))

        return max(GeodeCounts)

    def collectResources(self):
        resources = copy.deepcopy(self.resources)
        for robot in self.robots:
            resources[robot] += self.robots[robot]
        return resources

    def subresources(self, resource1, resource2):
        newTotals = {}
        for each in resource1:
            newTotals[each] = resource1[each]
        for each in resource2:
            newTotals[each] = newTotals[each] - resource2[each]
        return newTotals

    def canBuild(self, robot):
        for resource in self.blueprint[robot]:
            if self.resources[resource] < self.blueprint[robot][resource]:
                return False
        return True
    
    def BuildBot(self, robot, resources):
        newRobots = copy.deepcopy(self.robots)
        newRobots[robot] +=1
        return (newRobots, self.subresources(resources, self.blueprint[robot]))

def determineMaxCosts(blueprint):
    maxResources = {
        "Ore":0,
        "Clay":0,
        "Obsidian":0,
        "Geode":sys.maxsize
    }
    for each in blueprint:
        for type in blueprint[each]:
            if blueprint[each][type] > maxResources[type]:
                maxResources[type] = blueprint[each][type]
    return maxResources

def main(filePath):
    with open(filePath) as file:
        input = file.read()
    start_time = time.time()

    #Parse the input, ending with a dict of blueprints, which contains a dict of robots and thier costs
    #robots collect ore equal to thier name, and cost ore equal to whats in the value of thier key-value pair.
    blueprints = {}
    for line in input.split('\n'):
        robots = line.split(':')[1].split('.')
        robotCosts = {}
        robotCosts["Ore"] = {"Ore": int(robots[0].strip().split(' ')[4])}
        robotCosts["Clay"] = {"Ore": int(robots[1].strip().split(' ')[4])}
        robotCosts["Obsidian"] = {"Ore": int(robots[2].strip().split(' ')[4]), "Clay": int(robots[2].strip().split(' ')[7])}
        robotCosts["Geode"] = {"Ore": int(robots[3].strip().split(' ')[4]), "Obsidian": int(robots[3].strip().split(' ')[7])}
        blueprints[line.split(':')[0]] = robotCosts

    #setup inital robot states
    robot = {
        "Ore" : 1,
        "Clay" : 0,
        "Obsidian": 0,
        "Geode": 0
        }

    resources = {
        "Ore" : 0,
        "Clay" : 0,
        "Obsidian": 0,
        "Geode": 0
        }

    for blueprint in blueprints:
        maxResources = determineMaxCosts(blueprints[blueprint])
        simulation = Simulation(blueprints[blueprint], robot, resources, 1, 24, maxResources)
        print(simulation.runMin(simulation))


    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    #main('Day19/input')
    main('Day19/inputTest')