from abc import ABC
from enum import Enum
from math import tanh
import random

class AgentAction(Enum):
    RUN = 0
    WARN = 1


class Agent:
    def __init__(self):
        self.is_dead = False

    def make_decision(self):
        raise NotImplementedError("Agent can't decide whether it should live or die")

    def kill(self):
        self.is_dead = True

    def __str__(self):
        return repr(self)

    def procreate(self):
        raise NotImplementedError("Generic agents cannot procreate")
    
    def __repr__(self):
        text = "Dead" if self.is_dead else "Alive"
        return f"{text}{type(self).__name__}"
        

class NormalAgent(Agent):
    def __init__(self):
        self.is_dead = False

    def make_decision(self):
        return AgentAction.RUN

    def procreate(self):
        children = []
        children.append(NormalAgent())
        if random.randint(1, 10) > 9:
            children.append(NormalAgent())
        return children
    

class HeroicAgent(Agent):
    def __init__(self):
        super().__init__()

    def make_decision(self):
        return AgentAction.WARN

    def procreate(self):
        children = []
        children.append(HeroicAgent())
        if random.randint(1, 10) > 9:
            children.append(HeroicAgent())
        return children

class EvolveableAgent(Agent):
    def __init__(self, action_chance=0):
        super().__init__()
        self.action_chance = action_chance
        self.feed_counter = 0
        self.save_counter = 0
    
    def make_decision(self):
        if random.random() < (tanh(self.action_chance/10)/2) + 0.5:
            return AgentAction.WARN
        else:
            return AgentAction.RUN
    
    def feed(self):
        self.feed_counter += 1

    def procreate(self):
        if self.feed_counter == 3:
            self.feed_counter = 0
            self.kill()
            children = []
            children.append(EvolveableAgent(self.action_chance + random.choices([-1, 0, 1] + [k for k in range(1, self.save_counter + 1)])[0])) #1 if self.save_counter != 0 else random.choice([-1, 0])
            children.append(EvolveableAgent(self.action_chance + random.choices([-1, 0, 1] + [k for k in range(1, self.save_counter + 1)])[0]))
            return children
        else:
            return []
        
    def increment_save(self):
        self.save_counter += 1