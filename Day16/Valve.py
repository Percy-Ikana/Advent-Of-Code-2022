import time
import sys
import copy
import functools

class Hike:
    def __init__(self, unvisited, visited, origin, destination, tunnels):
        #setup class info
        self.unvisited = unvisited
        self.visited = visited
        self.origin = origin
        self.destination = destination
        self.tunnels = tunnels
        #make a dict of each hill, and the distance to it, defaults to the max word size for the cpu, -1 to prevent overflow (not that python can overflow)
        self.tunnelDistances = dict(zip(unvisited, [0]*len(tunnels)))

    def visit_hill(self, currentPosition, visited, unvisited, hillDistances):
        #for each valid next hill for the current hill
        nextHills = self.tunnels[currentPosition][1]
        for nextHill in self.tunnels[currentPosition][1]:
            #check if we have been here before
            #if nextHill not in self.visited:
                #check to make sure that the dist from this node, to the next, is the shortest (or equal to the shortest) that we have yet found.
                if hillDistances[currentPosition] + self.tunnels[nextHill][0] >= hillDistances[currentPosition]:
                    hillDistances[nextHill] = hillDistances[currentPosition] + self.tunnels[nextHill][0]
        #remove the current hill from the unvisited list, place it on the visited list.
        unvisited.remove(currentPosition)
        visited.append(currentPosition)

    def hike(self):
        #go until we have visisted the ending hill
        self.tunnelDistances[self.origin] = 0
        while not self.destination in self.visited:
            #grab the smallest distance hill in the list of unvisited hills
            current_hill = max(self.unvisited, key=self.tunnelDistances.get)
            #visit it
            self.visit_hill(current_hill, self.visited, self.unvisited, self.tunnelDistances)
        pass

numberofSims = 0
class Sim:
    def __init__(self, min, path, tunnels, openValves, lastOpenedValve):
        self.min = min
        self.path = path
        self.tunnels = tunnels
        self.openValves = openValves
        self.lastOpenedValve = lastOpenedValve
#you should move to the closest non-open valve, the open it when you arrive
#min is the min, path is a list of rooms walked through, and openValves is a dict of rooms, with the value as (flow rate, time opened), for final calc at the end
def sim(simulation):
    global numberofSims
    simNumber = numberofSims
    numberofSims += 1
    if (numberofSims%10000 == 0): print(numberofSims)
    if simulation.min == 30 or set(simulation.openValves.keys()) == simulation.tunnels.keys(): 
        return simulation
    else:
        #we have more time to simulate, so simulate
        location = simulation.path[-1]
        flows = []
        #check if locations valve is not zero, and is closed, if so, open
        if simulation.tunnels[location][0] !=0 and location not in simulation.openValves:
            #open Valve
            newOpenValves = copy.deepcopy(simulation.openValves)
            newOpenValves[location] = (simulation.tunnels[location][0], simulation.min)
            #and call back in
            flows.append(sim(Sim(simulation.min+1,copy.deepcopy(simulation.path), simulation.tunnels, newOpenValves, copy.deepcopy(len(simulation.path)))))
        if True:
            # we just move, which is really a do nothing for this I think
            
            for door in simulation.tunnels[location][1]:
                newPath = copy.deepcopy(simulation.path)
                newPath.append(door)
                backtracked = (len(simulation.path) >= 2 and door == simulation.path[-2] and len(simulation.tunnels[location][1]) > 1)
                bigLoop = (door in simulation.path[simulation.lastOpenedValve:])
                if backtracked or bigLoop:
                    pass
                else:
                    flows.append(sim(Sim(simulation.min+1, newPath, simulation.tunnels, copy.deepcopy(simulation.openValves), copy.deepcopy(simulation.lastOpenedValve))))
            if len(flows) > 0:
                top = max(flows,key = lambda flow: CalculateFlow(flow.openValves))
                return top
            else:
                return(Sim(30,[],[],[],[]))
            
def CalculateFlow(openValves):
    totalFlow = 0
    for item in openValves:
        rate = openValves[item][0]
        time = 30 - openValves[item][1]
        totalFlow += (rate*time)
    return totalFlow

compareFlows2 = lambda sim1, sim2: 1 if CalculateFlow(sim1.openValves) > CalculateFlow(sim2.openValves) else -1

#return the highest flow sim, with a priority on high flow, low min
def compareFlows(sim1, sim2):
    sim1Flow = CalculateFlow(sim1.openValves)
    sim2Flow = CalculateFlow(sim2.openValves)
    if sim2Flow > sim1Flow:
        return 1
    elif sim2Flow > sim1Flow:
        return -1
    else:
        return 0

def main():
    with open('Day16/inputTest') as file:
        input = file.read()
    start_time = time.time()

    #1, 4, anything past 8
    #this gives us: 0: room name, 1: a tuple with (flow valve speed, locations it connects to)
    rooms = [[part[1], (int(part[4].split('=')[1][:-1]), part[9:])] for line in input.split('\n') for part in [line.replace(',', '').split(" ")]]
    tunnels = {}
    for room in rooms:
        tunnels[room[0]] = room[1]


    result = sim(Sim(1,['AA'], tunnels, {}, 0))

    print(CalculateFlow(result.openValves))
    print(numberofSims)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()