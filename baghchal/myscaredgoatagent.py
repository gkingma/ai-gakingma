from agent import Agent
from const import Const
from game import Game
from move import Move
from typing import List
import random

class MyScaredGoatAgent(Agent):
    def __init__(self, game : Game):
        super(MyScaredGoatAgent, self).__init__(game,Const.MARK_GOAT)
    def propose(self) -> Move:
        moves = self.game.goatMoves()
        safeMoves : list[Move]=[]
        safeMovesPriority : list[int]=[]
        for move in moves:
            self.game.play(move)
            tigerMoves = self.game.tigerMoves()
            captures : list[Move]=[]
            for tMove in tigerMoves:
                if tMove.capture:
                    captures.append(move)
            if len(captures) == 0:
                safeMoves.append(move)
                safeMovesPriority.append(len(tigerMoves))
            self.game.unplay(move)
        bestMoves : list[Move]=[]
        if len(safeMoves) != 0:
            bestPriority = min(safeMovesPriority)
            for i in range(len(safeMoves)):
                if safeMovesPriority[i] == bestPriority:
                    bestMoves.append(safeMoves[i])
        else:
            bestMoves = moves
        return random.choice(bestMoves)
