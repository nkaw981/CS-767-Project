from sim_agents.Agent import NormalAgent, HeroicAgent
from sim_environment.SimulationEngine import SimulationEngine, SimulationLocation

from statistics import median, mean, stdev
import random

a1 = NormalAgent()
a2 = HeroicAgent()
a3 = NormalAgent()
a4 = HeroicAgent()

l1 = SimulationLocation(True)
l2 = SimulationLocation(False)

locations = []
agents = []

seed = -1655191079 #random.randint(-2147483648, 2147483648)
print(seed)
random.seed(seed)

for i in range(0, 200):
    locations.append(SimulationLocation())

for i in range(0, 100):
    agents.append(NormalAgent())
    agents.append(HeroicAgent())

sim = SimulationEngine(agents, locations)

logs = []

for i in range(1000):
    logs.append(sim.step())

def sim1(trials=10):
    results = []
    
    for i in range(trials):
        locations = []
        agents = []
        for i in range(0, 100):
            locations.append(SimulationLocation())

        for i in range(0, 100):
            agents.append(NormalAgent())
        
        sim = SimulationEngine(agents, locations)
        logs = []
        for i in range(1000):
            logs.append(sim.step())
        results.append(logs[-1])

    print("Sim1: # of Normal Agents left (mean, median) =", sum([values['normal'] for values in results])/trials, median([values['normal'] for values in results]))

    return results

def sim2(trials=10):
    results = []

    for i in range(trials):
        locations = []
        agents = []
        for i in range(0, 100):
            locations.append(SimulationLocation())

        for i in range(0, 100):
            agents.append(HeroicAgent())
        
        sim = SimulationEngine(agents, locations)
        logs = []
        for i in range(1000):
            logs.append(sim.step())
        results.append(logs[-1])
        #print(logs[-1])

    print("Sim2: # of Heroic Agents left (mean, median) =", sum([values['heroic'] for values in results])/trials, median([values['heroic'] for values in results]))

    return results

def sim3(trials=10):
    results = []
    extinct_at = []
    for i in range(trials):
        locations = []
        agents = []
        for i in range(0, 50):
            locations.append(SimulationLocation())

        for i in range(0, 50):
            agents.append(NormalAgent())
            agents.append(HeroicAgent())
            
        sim = SimulationEngine(agents, locations)
        logs = []
        for i in range(1000):
            logs.append(sim.step())
        #print(logs[-1])
        extinct_at.append(sim.extinct_at())
        results.append(logs[-1])

    print("Sim3:")
    print("# of Heroic Agents left (mean, median, stdev) =", mean([values['heroic'] for values in results]), median([values['heroic'] for values in results]), stdev([values['heroic'] for values in results]))
    print("# of Normal Agents left (mean, median, stdev) =", mean([values['normal'] for values in results]), median([values['normal'] for values in results]), stdev([values['normal'] for values in results]))
    print()
    print("# of times Normal Agents go extinct:", [values['normal'] for values in results].count(0))
    print("# of times Heroic Agents go extinct:", [values['heroic'] for values in results].count(0))
    
    all_normal_extincts = [values['normal'] for values in extinct_at]
    all_normal_extincts = [a for a in all_normal_extincts if a]

    all_heroic_extincts = [values['heroic'] for values in extinct_at]
    all_heroic_extincts = [a for a in all_heroic_extincts if a]
    
    print("# of cycles it takes for Normal Agents to go extinct (mean, median, stdev):", mean(all_normal_extincts), median(all_normal_extincts), stdev(all_normal_extincts))
    print("# of cycles it takes for Heroic Agents to go extinct (mean, median, stdev):", mean(all_heroic_extincts), median(all_heroic_extincts), stdev(all_heroic_extincts))
    return results

