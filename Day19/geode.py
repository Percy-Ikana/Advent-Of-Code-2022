import time
import copy 
import sys

class Simulation:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.robots = {
        "Ore" : 1,
        "Clay" : 0,
        "Obsidian": 0,
        "Geode": 0
        }
        self.resources = {
        "Ore" : 0,
        "Clay" : 0,
        "Obsidian": 0,
        "Geode": 0
        }

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


    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    #main('Day19/input')
    main('Day19/inputTest')