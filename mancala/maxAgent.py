import random
from agent import Agent
from game import Game

class MaxAgent(Agent):

    def _move(self, game):
        game_clone, rot_flag = game.clone_turn()
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