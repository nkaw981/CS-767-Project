import random
from sim_agents.Agent import AgentAction, NormalAgent, HeroicAgent

class SimulationEngine:
    def __init__(self, agents, locations):
        self.agents = agents
        self.locations = locations
        self.logs = []

    def prune_agent(self):
        self.agents = [agent for agent in self.agents if not agent.is_dead]

    def move_agents(self):
        order_of_selection = random.sample(self.agents, len(self.agents))
        for agent in order_of_selection:
            found_location = False
            while not found_location:
                try:
                    random_location = random.choice(self.locations)
                    random_location.add_agent(agent)
                    found_location = True
                except:
                    #print("Agent starved")
                    agent.kill()
                    break
        self.prune_agent()

    def process_locations(self):
        for location in self.locations:
            location.process()

    def reset_locations(self):
        for location in self.locations:
            location.reset()

    def cycle_agents(self):
        new_agents = []
        for agent in self.agents:
            for new_agent in agent.procreate():
                new_agents.append(new_agent)
            agent.kill()
        self.prune_agent()
        self.agents = new_agents
        

    def step(self):
        self.move_agents()
        self.process_locations()
        self.reset_locations()
        self.prune_agent()
        self.cycle_agents()
        #self.print_state()
        heroic_count = len([agent for agent in self.agents if isinstance(agent, HeroicAgent)])
        normal_count = len([agent for agent in self.agents if isinstance(agent, NormalAgent)])
        self.logs.append({"heroic": heroic_count, "normal": normal_count})
        return {"heroic": heroic_count, "normal": normal_count}

    def print_state(self):
        heroic_count = len([agent for agent in self.agents if isinstance(agent, HeroicAgent)])
        normal_count = len([agent for agent in self.agents if isinstance(agent, NormalAgent)])
        print("Heroic Agents =", heroic_count)
        print("Normal Agents =", normal_count)

    def extinct_at(self):
        try:
            heroic_extinct_at = [e['heroic'] for e in self.logs].index(0) + 1
        except:
            heroic_extinct_at = None
        try:
            normal_extinct_at = [e['normal'] for e in self.logs].index(0) + 1
        except:
            normal_extinct_at = None

        return {'heroic': heroic_extinct_at, 'normal': normal_extinct_at}
        

    


class SimulationLocation:
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
                        if random.randint(1, 10) > 5:
                            noticing_agent.kill()

        
        

        
        
