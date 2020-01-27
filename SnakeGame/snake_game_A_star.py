from snake_game_AI import SnakeGameAI
import pygame
import time
import random
import numpy as np

rand = random.Random()

class SnakeGameAStar(SnakeGameAI):
    
    def __init__(self, headless_mode = False):
        super().__init__(headless_mode)
        self.path2food = []

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

    def wiggle_away(self):
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        unsafe_moves = []
        food_dir = []
        
        d0 = -self.food[0] + self.head[0]
        if d0 != 0:
            food_dir.append([d0//abs(d0), 0])
        d1 = -self.food[1] + self.head[1]
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

    def bf_explore(self, temp_head):                
        self.explored.append(temp_head)

        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            if head in self.explored:
                continue

            self.parents[str(head)] = temp_head
            if self.check4food(head):
                self.food_found = True
                return 
            elif head not in self.explored:
                if head not in self.not_explored:
                    self.not_explored.insert(0, head)

    def bf_search(self, temp_head = None):
        self.food_found = False
        self.not_explored = []
        self.explored = []
        self.parents = dict()
        if temp_head == None:
            temp_head = self.head.copy()
        orig_head = temp_head.copy()
        
        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            if self.check4food(head):
                return move
            else:
                self.not_explored.insert(0, head)
                self.parents[str(head)] = temp_head
        
        while len(self.not_explored) > 0:
            temp_head = self.not_explored.pop()
            self.bf_explore(temp_head)
            if self.food_found:
                break

        if self.food_found: # back track to move
            loc = self.food
            while self.parents[str(loc)] != orig_head:
                loc = self.parents[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]

        else: # no path to food, return random move, TODO: chose move that lives longest, how?
            # temp solution wiggle away from food
            return self.wiggle_away() #safe_move() # rand.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])

    def check4food(self, loc):
        if self.food[0] == loc[0] and self.food[1] == loc[1]:
            return True
        else:
            return False

    def empty_spaces(self):
        return [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0 or self.board[i, j] == -1]


    def heuristic(self, head):
        # distance to food
        d0 = self.food[0] - head[0]
        d1 = self.food[1] - head[1]
        return np.sqrt(d0**2 + d1**2)

    def astar_explore(self, temp_head):
        self.explored.append(temp_head)

        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristic(head)

            if str(head) not in self.parents.keys():
                self.parents[str(head)] = temp_head

            if head in self.explored:
                continue

            if self.check4food(head):
                self.food_found = True
                return 
            if [h, head] not in self.not_explored:
                self.not_explored.insert(0, [h, head])
                self.not_explored.sort()
   
    def astar1move(self):
        temp_head = self.head.copy()
        moves = self.get_safe_moves(temp_head)
        if moves == []: # no safe moves
            return [1, 0]

        min_h = 50000
        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristic(head)
            
            if self.check4food(head):
                return move
            elif h < min_h:
                min_h = h
                best_move = move

        return best_move

    def astar_search(self, temp_head = None):
        self.food_found = False
        self.not_explored = []
        self.explored = []
        self.parents = dict()
        if temp_head == None:
            temp_head = self.head.copy()
        orig_head = temp_head.copy()

        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristic(head)
            if str(head) not in self.parents.keys():
                self.parents[str(head)] = temp_head
            if self.check4food(head):
                return move
            else:
                self.not_explored.insert(0, [h, head])
                self.not_explored.sort()
        
        while len(self.not_explored) > 0:
            h_th = self.not_explored.pop(0)
            self.astar_explore(h_th[1])
            if self.food_found:
                break

        if self.food_found: # back track to move
            loc = self.food
            while self.parents[str(loc)] != orig_head:
                loc = self.parents[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]
        elif len(self.explored) > 0: 
            loc = self.explored[-1] # last point
            while self.parents[str(loc)] != orig_head:
                loc = self.parents[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]
        else: # no path to food, no path to far point
            return self.wiggle_away() #safe_move() # rand.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])


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
    my_game = SnakeGameAStar()
    # my_game.run_game(my_game.astar1move)
    my_game.run_game(my_game.astar_search)

    # # stats run
    # N = 100
    # scores = []
    # for i in range(N):
    #     my_game = SnakeGameAStar(True) # headless mode
    #     while(my_game.game_state):        
    #         vel = my_game.astar_search()
    #         my_game.update_vel(vel)
    #         my_game.update_state()
    #     scores.append(my_game.score)
    #     print(f"{i+1} runs complete! Score: {my_game.score}")
    # print(f"max score: {max(scores)}")
    # print(f"mean score: {np.mean(scores)}")
    
if __name__ == "__main__":
    main()