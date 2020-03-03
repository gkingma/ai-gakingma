# SmartGoatAgent
# Usually an even split between wins, losses, and draws (average goat)
# Matt Behnke
from agent import Agent
from const import Const
from game import Game
from move import Move
from typing import List, Optional
from hungrytigeragent import HungryTigerAgent
import random

#FInd corners
def checkCorners(move):
    if(str(move) == 'Ga1' or str(move) == 'Ge1' or str(move) == 'Ga5' or str(move) == 'Ge5'):
        return move
    return None

#Convert move to numerical
def convertToNumerical(strMove: str):
        newMove = [0,0]
        if strMove[0] == 'G':
            strMove = list(strMove)
            if(strMove[1] == 'b'):
                newMove[0] = 1
            elif(strMove[1] == 'c'):
                newMove[0] = 2
            elif(strMove[1] == 'd'):
                newMove[0] = 3
            elif(strMove[1] == 'e'):
                newMove[0] = 4
            newMove[1] = int(strMove[2]) - 1
        else:
            strMove = list(strMove)
            if(strMove[0] == 'b'):
                newMove[0] = 1
            elif(strMove[0] == 'c'):
                newMove[0] = 2
            elif(strMove[0] == 'd'):
                newMove[0] = 3
            elif(strMove[0] == 'e'):
                newMove[0] = 4
            newMove[1] = int(strMove[1]) - 1

        #print(strMove)
        return newMove

# Convert capture to numerical
def convertTigerPounce(strMove: str):
    send1 = [strMove[1], strMove[2]]
    send2 = [strMove[4] , strMove[5]]
    send1Str = "".join(send1)
    send2Str = "".join(send2)
    move1 = convertToNumerical(send1Str)
    move2 = convertToNumerical(send2Str)
    hotSpot = [0, 0]
    hotSpot[0] = (move1[0] + move2[0]) / 2
    hotSpot[1] = (move1[1] + move2[1]) / 2
    return hotSpot

# Hotspots
def dangerMoves(tigerMoves):
        hotSpots = list()
        for tiger in tigerMoves:
            if tiger.capture:
                hotSpot = convertTigerPounce(str(tiger))
                hotSpots.append(hotSpot)
        return hotSpots

class SmartGoatAgent(Agent):
    #Constructors 
    def __init__(self, game: Game):
        super(SmartGoatAgent, self).__init__(game, Const.MARK_GOAT)
        self._hungryTigerAgent = HungryTigerAgent(game)

    #Check Corners
    def checkCorners(self, moves):
        for move in moves:
            if(str(move) == 'Ga1' or str(move) == 'Ge1' or str(move) == 'Ga5' or str(move) == 'Ge5'):
                return move
        return None
                
    
    def propose(self) -> Move:

        # Get Moves
        moves = self.game.goatMoves()

        safe : List[Move]=[]
        wins : List[Move]=[]
        loses : List[Move]=[]
        draws : List[Move]=[]
        scared : List[Move]=[]
        smartSafe : List[Move]=[]
        
        # Look ahead       
        for move in moves:
            self.game.play(move)
            tigerMove : Optional[Move] = self._hungryTigerAgent.propose() \
                if self.game.state == Const.STATE_TURN_TIGER else None
            playedState : int = self.game.state
            self.game.unplay(move)

            # Switched favoring a safe move over a draw
            # Check if corners are avaliable, if so take it
            if playedState == Const.STATE_WIN_GOAT:
                wins.append(move)
            elif playedState == Const.STATE_WIN_TIGER:
                loses.append(move)
            elif checkCorners(move) != None:
                smartSafe.append(move)
            elif not tigerMove.capture:
                safe.append(move)
            elif playedState == Const.STATE_DRAW:
                draws.append(move)
            else:
                scared.append(move)

        # Return the Move
        if len(wins) != 0:
            return random.choice(wins) 
        elif len(smartSafe) != 0:
            return random.choice(smartSafe)
        elif len(safe) != 0:
            return random.choice(safe)
        elif len(draws) != 0:
            return random.choice(draws)
        elif len(scared) != 0:
            return random.choice(scared)
        else:
            return random.choice(moves)


        
