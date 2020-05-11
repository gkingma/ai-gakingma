import random
import numpy as np
from numpy.lib.twodim_base import _min_int
from game import Game
from agent import Agent

class QLearningAgent(Agent):
    def __init__(self, games = 1000, alpha = .1, gamma = .6, epsilon = .1):
        self._games = games
        self._qTable = {}
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon
    
    def resolveQs(self, Qs, nextMax):
        for q in Qs:
            oldValue = self._qTable[q][Qs[q][0]]
            reward = Qs[q][1]
            self._qTable[q][Qs[q][0]] = oldValue * (1 - self._alpha) + self._alpha * (reward + self._gamma * nextMax)
            Qs.pop(q)

    def train(self):
        for i in range(self._games):
            #train on games
            unresolvedQs = {1:{},2:{}}
            game = Game()
            #used to evaluate differences in scores and determine if the q values need to be updated
            previousPlayer = 0
            previousScore = [0,0]
            while not game.over():
                #switch board to curent player's perspective
                game_clone, rot_flag = game.clone_turn()
                state = game_clone.state()
                player = game.turn_player()
                if not player == previousPlayer:
                    #resolve q values now that opponent's turn is complete
                    nextMax = 0
                    if state in self._qTable:
                        nextMax = max(self._qTable[state])
                    self.resolveQs(unresolvedQs[player],nextMax)
                if state in self._qTable:
                    #if this state has been seen before
                    if random.uniform(0,1) < self._epsilon:
                        #choose random action
                        moves = Agent.valid_indices(game_clone)
                        idx = random.choice(moves)
                        unresolvedQs[player[state]] = (int(idx), float(self._qTable[state][idx]))
                        move = game.rotate_board(rot_flag, idx)
                        game.move(move)
                    else :
                        #choose highest q value
                        moves = Agent.valid_indices(game_clone)
                        validQs = []
                        for move in moves:
                            validQs.append(self._qTable[state][move])
                        maxQ = max(validQs)
                        idx = 0
                        for i in range(len(validQs)):
                            if validQs[i] == maxQ:
                                idx = moves[i]
                        
                        unresolvedQs[player[state]] = (int(idx), float(self._qTable[state][idx]))
                        move = game.rotate_board(rot_flag, idx)
                        game.move(move)
                else:
                    self._qTable[state] = [0,0,0,0,0,0]
                    #choose random action
                    moves = Agent.valid_indices(game_clone)
                    idx = random.choice(moves)
                    unresolvedQs[player[state]] = (int(idx), float(self._qTable[state][idx]))
                    move = game.rotate_board(rot_flag, idx)
                    game.move(move)
                
                #net gain or loss inc points for turn
                scoreDifference = game.score()[0] - game.score()[1]
                scoreDifference = scoreDifference + previousScore[0] - previousScore[1]
                for q in unresolvedQs[1]:
                    unresolvedQs[1][q][1] = unresolvedQs[1][q][1] + scoreDifference
                for q in unresolvedQs[2]:
                    unresolvedQs[2][q][2] = unresolvedQs[2][q][2] - scoreDifference
                previousPlayer = player
                previousScore = game.score()
            
                if game.score()[0] >= 25:
                    for q in unresolvedQs[1]:
                        unresolvedQs[1][q][1] = unresolvedQs[1][q][1] + 25
                    for q in unresolvedQs[2]:
                        unresolvedQs[2][q][2] = unresolvedQs[2][q][2] - 25
                else :
                    for q in unresolvedQs[1]:
                        unresolvedQs[1][q][1] = unresolvedQs[1][q][1] - 25
                    for q in unresolvedQs[2]:
                        unresolvedQs[2][q][2] = unresolvedQs[2][q][2] + 25
                self.resolveQs(unresolvedQs[1], 0)
                self.resolveQs(unresolvedQs[2], 0)