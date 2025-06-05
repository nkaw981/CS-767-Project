import random
from sim_agents.Agent import AgentAction, EvolveableAgent
from sim_environment.SimulationEngine import SimulationEngine, SimulationLocation
from statistics import median, mean, stdev

class DarwinistSimulationEngine(SimulationEngine):
    def __init__(self, agents, locations):
        super().__init__(agents, locations)

    @property
    def agent_count(self):
        return len(self.agents)

    def cycle_agents(self):
        new_agents = []
        for agent in self.agents:
            #print(self.agents)
            #print(agent)
            for new_agent in agent.procreate():
                new_agents.append(new_agent)
        self.prune_agent()
        self.agents += new_agents
        #print(self.agents)

    def feed_agents(self):
        for agent in self.agents:
            agent.feed()
        

    def step(self):
        #print(len(self.agents))
        self.move_agents()
        self.process_locations()
        self.reset_locations()
        self.prune_agent()
        self.feed_agents()
        self.cycle_agents()
        behavior = self.return_average_of_action_chance()
        self.logs.append(behavior)
        return behavior
    
    def return_average_of_action_chance(self):
        return {"mean": mean(agent.action_chance for agent in self.agents), "median": median(agent.action_chance for agent in self.agents), "count": self.agent_count}

    def print_state(self):
        pass

    def extinct_at(self):
        raise NotImplementedError("This function is not supported for this class.")


    
class ModifiedSimulationLocation(SimulationLocation):
    def __init__(self, has_predator=random.randint(1, 10) > 7):
        self.agents = []
        self.has_predator = has_predator

    def add_agent(self, agent):
        if len(self.agents) == 2:
            raise Exception("Location is full!")
        else:
            self.agents.append(agent)

    def reset(self):
        self.agents = []

    def process(self):
        if len(self.agents) == 0:
            return
        if self.has_predator:
            if len(self.agents) == 1:
                self.agents[0].kill()
                return
            else:
                which_agent = random.randint(0, 1)
                noticing_agent = self.agents[which_agent]
                match noticing_agent.make_decision():
                    case AgentAction.RUN:
                        self.agents.remove(noticing_agent)
                        self.agents[0].kill()
                    case AgentAction.WARN:
                        noticing_agent.increment_save()
                        if random.randint(1, 20) > 20:
                            noticing_agent.kill()

