from game import Game
from agent import Agent
from maxAgent import MaxAgent
from randomAgent import RandomAgent
from qlearning import QLearningAgent

qAgent = QLearningAgent(10000)
qAgent.train()

print('trained on 10000 games')
agent_two = MaxAgent()
wins = 0

for i in range(5000):
    game = Game()
    while not game.over():
        if game.turn_player() == 1:
            game.move(qAgent.move(game))
        else:
            game.move(agent_two.move(game))
    if game.score()[0] > game.score()[1]:
        wins = wins + 1

for i in range(5000):
    game = Game()
    while not game.over():
        if game.turn_player() == 2:
            game.move(qAgent.move(game))
        else:
            game.move(agent_two.move(game))
    if game.score()[1] > game.score()[0]:
        wins = wins + 1

print('QLearningAgent wins:\n{}'.format(wins))
del qAgent

qAgent = QLearningAgent(100000)
qAgent.train()

print('trained on 100000 games')
agent_two = MaxAgent()
wins = 0

for i in range(5000):
    game = Game()
    while not game.over():
        if game.turn_player() == 1:
            game.move(qAgent.move(game))
        else:
            game.move(agent_two.move(game))
    if game.score()[0] > game.score()[1]:
        wins = wins + 1

for i in range(5000):
    game = Game()
    while not game.over():
        if game.turn_player() == 2:
            game.move(qAgent.move(game))
        else:
            game.move(agent_two.move(game))
    if game.score()[1] > game.score()[0]:
        wins = wins + 1

print('QLearningAgent wins:\n{}'.format(wins))
del qAgent