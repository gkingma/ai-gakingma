from hungrytigeragent import HungryTigerAgent
from game import Game
import random
from matchup import Matchup
from hungrytigeragent import HungryTigerAgent
from scaredgoatagent import ScaredGoatAgent
from myscaredgoatagent import MyScaredGoatAgent
from stats import Stats

matchup = Matchup()
matchup.tigerAgent = HungryTigerAgent(matchup.game)
matchup.goatAgent = MyScaredGoatAgent(matchup.game)

#while not matchup.over:
    #matchup.turn()
    #print(matchup.game)

stats = Stats(matchup, 1000)
stats.playAll()
stats.summarize()
