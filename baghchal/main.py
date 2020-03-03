from game import Game
import random
from matchup import Matchup
from hungrytigeragent import HungryTigerAgent
from scaredgoatagent import ScaredGoatAgent
from aggressivegoatagent import AggressiveGoatAgent
from stats import Stats

matchup = Matchup()  
matchup.tigerAgent = HungryTigerAgent(matchup.game)
matchup.goatAgent = AggressiveGoatAgent(matchup.game)

#while not matchup.over:
    #matchup.turn()
    #print(matchup.game)

stats = Stats(matchup, 100)
stats.playAll()
stats.summarize()
