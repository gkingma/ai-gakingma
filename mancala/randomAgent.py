import random
from agent import Agent

class RandomAgent(Agent):
    
    def _move(self, game):
        moves = Agent.valid_indices(game)
        if len(moves) < 1:
            return 0

        return random.choice(moves)