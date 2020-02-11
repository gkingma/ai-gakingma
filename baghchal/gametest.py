import unittest

from const import Const
from game import Game
from move import Move


class GameTest(unittest.TestCase):
 
    def testTigerMove(self):
        game = Game()
        moves = game.tigerMoves()
        self.assertTrue(len(moves),12)

if __name__ == '__main__':
    unittest.main()
