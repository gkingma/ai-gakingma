import random
import numpy as np
from numpy.lib.twodim_base import _min_int
from game import Game
from agent import Agent

class QLearningAgent(Agent):
    def __init__(self, games = 10000, alpha = .3, gamma = .7, epsilon = .2):
        self._games = games
        self._qTable = {}
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon

    def qTable(self):
        f = open('output.txt', 'w+')
        f.write(str(self._qTable))
        f.close()
    
    def resolveQs(self, Qs, nextMax):
        for q in Qs:
            oldValue = self._qTable[q][Qs[q][0]]
            reward = Qs[q][1]
            self._qTable[q][Qs[q][0]] = oldValue * (1 - self._alpha) + self._alpha * (reward + self._gamma * nextMax)
        while len(Qs):
            Qs.popitem()

    def train(self):
        for i in range(self._games):
            self._alpha = ((self._games - i + 1) / self._games) * .6 + .3
            self._gamma = ((self._games - i + 1) / self._games) * .5 + .4
            #self._epsilon = ((self._games - i + 1) / self._games) * .8 + .1
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
                        unresolvedQs[player][state] = [int(idx), float(self._qTable[state][idx])]
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
                        
                        unresolvedQs[player][state] = [int(idx), float(self._qTable[state][idx])]
                        move = game.rotate_board(rot_flag, idx)
                        game.move(move)
                else:
                    self._qTable[state] = [0,0,0,0,0,0]
                    #choose random action
                    moves = Agent.valid_indices(game_clone)
                    idx = random.choice(moves)
                    unresolvedQs[player][state] = [int(idx), float(self._qTable[state][idx])]
                    move = game.rotate_board(rot_flag, idx)
                    game.move(move)
                
                #net gain or loss inc points for turn
                scoreDifference = game.score()[0] - game.score()[1]
                scoreDifference = scoreDifference + previousScore[0] - previousScore[1]
                for q in unresolvedQs[1]:
                    unresolvedQs[1][q][1] = unresolvedQs[1][q][1] + scoreDifference
                for q in unresolvedQs[2]:
                    unresolvedQs[2][q][1] = unresolvedQs[2][q][1] - scoreDifference
                previousPlayer = player
                previousScore = game.score()
            
                if game.score()[0] >= 25:
                    for q in unresolvedQs[1]:
                        unresolvedQs[1][q][1] = unresolvedQs[1][q][1] + 25
                    for q in unresolvedQs[2]:
                        unresolvedQs[2][q][1] = unresolvedQs[2][q][1] - 25
                else :
                    for q in unresolvedQs[1]:
                        unresolvedQs[1][q][1] = unresolvedQs[1][q][1] - 25
                    for q in unresolvedQs[2]:
                        unresolvedQs[2][q][1] = unresolvedQs[2][q][1] + 25
                self.resolveQs(unresolvedQs[1], 0)
                self.resolveQs(unresolvedQs[2], 0)
    
    def _move(self, game):
        game_clone, rot_flag = game.clone_turn()
        state = game_clone.state()
        if state in self._qTable:
            moves = Agent.valid_indices(game_clone)
            validState = True
            for move in moves:
                if self._qTable[state] == 0:
                    validState = False
            if validState:
                maxQ = -10000
                idx = moves[0]
                for move in moves:
                    if self._qTable[state][move] > maxQ:
                        maxQ = self._qTable[state][move]
                        idx = move
                final_move = game.rotate_board(rot_flag, idx)
                return final_move
    
        moves = Agent.valid_indices(game_clone)
        scores = []
        for move in moves:
            clone = game_clone.clone()
            clone.move(move)
            scores.append(clone.score()[0])
        maxScore = 0
        for score in scores:
            if score > maxScore:
                maxScore = score
        best_moves = []
        for i in range(len(scores)):
            if scores[i] == maxScore:
                best_moves.append(moves[i])

        final_move = game.rotate_board(rot_flag, random.choice(best_moves))
        return final_move