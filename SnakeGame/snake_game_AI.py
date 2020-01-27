from snake_game_GUI import SnakeGameGUI
import pygame
import time
import random
import numpy as np

rand = random.Random()

class SnakeGameAI(SnakeGameGUI):
    
    def __init__(self, headless_mode = False):
        super().__init__(headless_mode)
        self.reverse = 1 # flag to allow snake to alternate directions

    def rand_move(self):
        return rand.choice([[-1, 0], [1, 0], [0, -1], [0, 1]])
    
    def get_safe_moves(self, temp_head = None): 
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        unsafe_moves = []

        if temp_head == None:
            temp_head_orig = self.head.copy()
        else:
            temp_head_orig = temp_head.copy()
        # remove unsafe moves
        for move in moves:
            temp_head = temp_head_orig.copy()
            temp_head[0] += move[0]
            temp_head[1] += move[1]

            if temp_head[0] < 0 or temp_head[0] >= self.height:
                unsafe_moves.append(move)
            elif temp_head[1] < 0 or temp_head[1] >= self.width:
                unsafe_moves.append(move)
            elif temp_head in self.snake: 
                unsafe_moves.append(move)

        for move in unsafe_moves:
            moves.remove(move)
        
        return moves

    def safe_move(self):
        moves = self.get_safe_moves()
        if len(moves) == 0: # no safe moves
            moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        return rand.choice(moves)

    def move2food(self):
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        unsafe_moves = []
        food_dir = []
        
        d0 = self.food[0] - self.head[0]
        if d0 != 0:
            food_dir.append([d0//abs(d0), 0])
        d1 = self.food[1] - self.head[1]
        if d1 != 0:
            food_dir.append([0, d1//abs(d1)])


        # remove unsafe moves
        for move in moves:
            temp_head = self.head.copy()
            temp_head[0] += move[0]
            temp_head[1] += move[1]

            if temp_head[0] < 0 or temp_head[0] >= self.height:
                unsafe_moves.append(move)
            elif temp_head[1] < 0 or temp_head[1] >= self.width:
                unsafe_moves.append(move)
            elif temp_head in self.snake: 
                unsafe_moves.append(move)

        for move in unsafe_moves:
            moves.remove(move)
        
        # move towards food first
        for move in moves:
            if move in food_dir:
                return move
            
        if len(moves) == 0: # no safe moves
            return [1, 0]
        else:
            return rand.choice(moves)
    
    def wiggle2food(self):
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        unsafe_moves = []
        food_dir = []
        
        d0 = self.food[0] - self.head[0]
        if d0 != 0:
            food_dir.append([d0//abs(d0), 0])
        d1 = self.food[1] - self.head[1]
        if d1 != 0:
            food_dir.append([0, d1//abs(d1)])


        # remove unsafe moves
        for move in moves:
            temp_head = self.head.copy()
            temp_head[0] += move[0]
            temp_head[1] += move[1]

            if temp_head[0] < 0 or temp_head[0] >= self.height:
                unsafe_moves.append(move)
            elif temp_head[1] < 0 or temp_head[1] >= self.width:
                unsafe_moves.append(move)
            elif temp_head in self.snake: 
                unsafe_moves.append(move)

        for move in unsafe_moves:
            moves.remove(move)
        
        # move towards food first
        self.reverse *= -1 # to alternate turning direction
        for move in moves[::self.reverse]:
        # for move in moves:
            if move in food_dir:
                return move
            
        if len(moves) == 0: # no safe moves
            return [1, 0]
        else:
            return rand.choice(moves)

    def run_game(self, player_ai = None):
            update_rate = 1
            fps = 60
            counter = 0
            vel = self.vel
            pygame.init()
            myfont = pygame.font.SysFont("monospace", 65)
            self.draw_board()
            pygame.display.update()

            exit_flag = False
            while exit_flag == False and self.game_state == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_flag = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            vel = [-1, 0]
                        elif event.key == pygame.K_DOWN:
                            vel = [1, 0]
                        elif event.key == pygame.K_LEFT:
                            vel = [0, -1]
                        elif event.key == pygame.K_RIGHT:
                            vel = [0, 1]
                        else:
                            vel = self.vel
                
                time.sleep(1.0/fps)
                counter += 1
                if counter >= update_rate:
                    if player_ai != None:
                        vel = player_ai()
                    self.update_vel(vel)
                    self.update_state()
                    counter = 0
                self.draw_board()
                pygame.display.update()

            label = myfont.render(f"Game Over!", 1, self.RED)
            self.SCREEN.blit(label, (self.WIDTH+10,50))
            pygame.display.update()

            while exit_flag == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_flag = True
            pygame.quit()


def main():
    my_game = SnakeGameAI()
    # my_game.run_game(my_game.rand_move)
    # my_game.run_game(my_game.safe_move)
    my_game.run_game(my_game.wiggle2food)
    # N = 100
    # scores = []
    # # best_game = []
    # # max_score = 0
    # for i in range(N):
    #     my_game = SnakeGameAI(True) # headless mode
    #     # game = [my_game.board.copy()]
    #     # my_game.run_game(my_game.safe_move2food)
    #     while(my_game.game_state):
    #         # vel = my_game.safe_move()        
    #         vel = my_game.safe_move2food()
    #         my_game.update_vel(vel)
    #         my_game.update_state()
    #     #     game.append(my_game.board.copy())
    #     # # print(f"Game Over! Score: {my_game.score}")
    #     scores.append(my_game.score)
    #     # if my_game.score > max_score:
    #     #     max_score = my_game.score
    #     #     best_game = game.copy()
    # print(f"max score: {max(scores)}")
    # print(f"mean score: {np.mean(scores)}")

    # # run the replay
    # # for board in best_game:
    # #     my_game.board = board
    # #     my_game.draw_board()
    # #     pygame.display.update()
    # #     time.sleep(0.25)
    
if __name__ == "__main__":
    main()