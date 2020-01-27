import numpy as np
import random

rand = random.Random()

class SnakeGame():
    
    def __init__(self):
        self.game_state = True # False when Game Over
        self.height = 15
        self.width = 15
        self.size = [self.height, self.width]
        self.board = np.zeros(self.size)
        self.score = 0
        self.head = [self.height//2, self.width//2]  
        self.vel = rand.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
        self.snake = [[self.head[0] - i*self.vel[0], self.head[1] - i*self.vel[1]] for i in range(3)]
        for s in self.snake:
            self.board[s[0], s[1]] = 1
        self.board[self.head[0], self.head[1]] = 2
        self.food = self.rand_food()
        self.board[self.food[0], self.food[1]] = -1
    
    def __str__(self):
        b_str = " " + "_"*self.width + f"  Score: {self.score}\n"
        for i in range(self.height):
            b_str += "|"
            for j in range(self.width):
                if self.board[i, j] == 2:
                # if [i, j] == self.head:
                    b_str += "X"
                elif self.board[i, j] == 1:
                # elif [i, j] in self.snake:
                    b_str += "x"
                elif self.board[i, j] == -1:
                # elif [i, j] == self.food:
                    b_str += "O"
                else:
                    b_str += " "
            b_str += "|\n"
        b_str += u" \u0305"*self.width 
        return b_str

    def rand_food(self):
        empty_spaces = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
        return rand.choices(empty_spaces)[0]
    
    def update_vel(self, vel):
        temp_head = [self.head[0] + vel[0], self.head[1] + vel[1]]
        if temp_head != self.snake[1]: # make sure it's not previous body part
            self.vel = vel

    def update_state(self):
        self.head[0] += self.vel[0]
        self.head[1] += self.vel[1]

        if self.head[0] < 0 or self.head[0] >= self.height:
            self.head = self.snake[0].copy() # did not enter valid move
            self.game_state = False
        elif self.head[1] < 0 or self.head[1] >= self.width:
            self.head = self.snake[0].copy() # did not enter valid move
            self.game_state = False
        elif self.head in self.snake[2::]: # snake in body and no u-turn
            self.head = self.snake[0].copy() # did not enter valid move
            self.game_state = False 
        elif self.head not in self.snake: # snake moved
            if self.head == self.food: # ate food, grow snake, gen food
                self.score += 1
                self.snake.insert(0, self.head.copy())
                self.board[self.snake[1][0], self.snake[1][1]] = 1
                self.board[self.head[0], self.head[1]] = 2
                self.food = self.rand_food()
                self.board[self.food[0], self.food[1]] = -1
            else: # move snake
                self.snake.insert(0, self.head.copy())
                self.board[self.snake[1][0], self.snake[1][1]] = 1
                self.board[self.head[0], self.head[1]] = 2
                rem = self.snake.pop()
                self.board[rem[0], rem[1]] = 0
        else:
            self.head = self.snake[0].copy() # did not enter valid move
                

def main():
    my_game = SnakeGame()
    while(my_game.game_state):
        print(my_game)
        move = input("Enter move: ")
        if move == "w":
            vel = [-1, 0]
        elif move == "s":
            vel = [1, 0]
        elif move == "a":
            vel = [0, -1]
        elif move == "d":
            vel = [0, 1]
        else:
            vel = my_game.vel
        
        my_game.update_vel(vel)
        my_game.update_state()

if __name__ == "__main__":
    main()