from sim_agents.Agent import EvolveableAgent
from sim_environment.SimulationEngine import SimulationEngine, SimulationLocation
from sim_environment.DarwinistSimulationEngine import DarwinistSimulationEngine, ModifiedSimulationLocation

from statistics import median, mean, stdev, StatisticsError
import random

final_results = []
k = 0
while k < 100:
    try:
        locations = []
        agents = []
        for i in range(0, 200):
            locations.append(ModifiedSimulationLocation(random.randint(1, 10) > 7))
        counts = [location.has_predator for location in locations]
        agents.append(EvolveableAgent())
        agents.append(EvolveableAgent())
        agents.append(EvolveableAgent())
        agents.append(EvolveableAgent())
        agents.append(EvolveableAgent())

        sim = DarwinistSimulationEngine(agents, locations)
        logs = []
        for j in range(1000):
            logs.append(sim.step())
        final_results.append(logs[-1])

        k += 1
        print(k)
    except StatisticsError:
        pass

for i in final_results:
    print(i)