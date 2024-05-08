#Daniel Zadorozhnyy 34274290
#Jay (Jinmo) Yang 34278275
from tkinter import *
from Grid import Grid
from Pixel import Pixel
import time
import random
import pygame

### complete class Snake
class Snake(Grid):
    def __init__(self,root,n_obstacles,n_fruit,nrow=50,ncol=30,scale=15):
        super().__init__(root,nrow,ncol,scale)
        self.n_obstacles = n_obstacles
        self.__n_fruit = n_fruit
        self.vector = [0,1]
        #spawn random obstacles
        super().random_pixels(n_fruit, 3)
        super().random_pixels(n_obstacles, 1)
        self.fix_num_of_fruits()
        
        self.__pause = False
        self.__game_over = False
        self.__score = 0

        self.snake = []
        self.start_i = nrow // 2
        self.start_j = ncol // 2
        self.make_snake()
                
    def make_snake(self):
        """Create a snake represented by a list containing Pixel() instances formed in the middle of the grid, created with a random direction and facing a random direction"""
        choice_of_vectors = [[1,0],[-1,0],[0,1],[0,-1]]
        rand_index = random.randint(0,3)
        self.vector = choice_of_vectors[rand_index] #randomly select a vector to then use to generate a snake facing a random direction
        if self.vector == [0,1]: #if the snake is going to the right, create body from the left
            for index in range(4):
                if index < 3:
                    body = Pixel(self.canvas, self.start_i, self.start_j - 3 + index, self.nrow, self.ncol, self.scale, 5, self.vector)
                    self.snake.append(body)
                else:
                    head = Pixel(self.canvas, self.start_i, self.start_j, self.nrow, self.ncol, self.scale, 4, self.vector)
                    self.snake.append(head)
        if self.vector == [0,-1]: #if the snake is starting off facing the left, create body in the opposite direction
            for index in range(4):
                if index < 3:
                    body = Pixel(self.canvas, self.start_i, self.start_j + 3 - index, self.nrow, self.ncol, self.scale, 5, self.vector)
                    self.snake.append(body)
                else:
                    head = Pixel(self.canvas, self.start_i, self.start_j, self.nrow, self.ncol, self.scale, 4, self.vector)
                    self.snake.append(head)
        if self.vector == [1,0]: #if snake is facing down, create body from the top
            for index in range(4):
                if index < 3:
                    body = Pixel(self.canvas, self.start_i - 3 + index, self.start_j, self.nrow, self.ncol, self.scale, 5, self.vector)
                    self.snake.append(body)
                else:
                    head = Pixel(self.canvas, self.start_i, self.start_j, self.nrow, self.ncol, self.scale, 4, self.vector)
                    self.snake.append(head)
        if self.vector == [-1,0]: #if snake is facing up, create body from the bottom
            for index in range(4):
                if index < 3:
                    body = Pixel(self.canvas, self.start_i + 3 - index, self.start_j, self.nrow, self.ncol, self.scale, 5, self.vector)
                    self.snake.append(body)
                else:
                    head = Pixel(self.canvas, self.start_i, self.start_j, self.nrow, self.ncol, self.scale, 4, self.vector)
                    self.snake.append(head)
    
    def fix_num_of_fruits(self): 
        """In case of a possibility where an obstacle spawns in the same location as a fruit, simply check for the number of fruit in the grid, and reassign the value to self.__n_fruit to ensure the player can still eat all fruit that are accessible"""
        num_fruit = 0
        for i_index in range(len(self.matrix)):
            for j_index in range(len(self.matrix[0])):
                if self.matrix[i_index][j_index] == 3:
                    num_fruit = num_fruit + 1
        self.__n_fruit = num_fruit

    
    def is_pause(self):
        """check if game is paused"""
        return self.__pause
    def pause(self):
        if self.__pause == False: #if the game is not already paused, pause it 
            self.__pause = True
            print("pause")
        elif self.__pause == True: #if the game is already paused, unpause it
            self.__pause = False
            print("unpause")

    def is_game_over(self):
        """Check if the game is over based on the variable self.__game_over
            If the game is over, check if the user has eaten all the fruit. If true, then the player has won the game
            If the game is over and all the fruit has not yet been eaten, that means the player has lost"""
        if self.__game_over == True:
            if self.__n_fruit == 0:
                pygame.mixer.init()
                pygame.mixer.music.load("zapsplat_multimedia_game_sound_slot_machine_win_or_spin_mallet_tone_002_65516.mp3") #Fruit machine sound, win or spin tone 2 from zapsplat.com
                #https://www.zapsplat.com/music/fruit-machine-sound-win-or-spin-tone-2/
                pygame.mixer.music.play()
                self.canvas.create_text(self.ncol*self.scale // 2,self.nrow * self.scale // 2,text="*** YOU WON ***",fill="orange",font=("Times New Roman",25))
                print("Your score: " + str(self.__score))
            else:
                pygame.mixer.init()
                pygame.mixer.music.load("zapsplat_multimedia_game_sound_fun_arcade_organ_short_negative_fail_lose_003_54276.mp3") #Game arcade sound from zapsplat.com
                #https://www.zapsplat.com/music/game-sound-fun-arcade-organ-tone-short-negative-fail-or-lose-tone-3/
                pygame.mixer.music.play()
                self.canvas.create_text(self.ncol*self.scale // 2,self.nrow * self.scale // 2,text="GAME OVER",fill="orange",font=("Times New Roman",25))
                print("Your score: " + str(self.__score))
        return self.__game_over

    def left(self):
        """Move the head of the snake left, as well as change the ij coordinate of the matrix to -3 so that the rest of the body can see the value and also move left when they reach the same ij coordinate"""
        if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
            current_i = self.snake[len(self.snake)-1].i 
            current_j = self.snake[len(self.snake)-1].j
            if self.snake[len(self.snake)-1].vector == [0,1] or self.snake[len(self.snake)-1].vector == [0,-1]:
                #If the snake is currently moving right or left, exit the function to make sure nothing happens
                return
            self.matrix[current_i][current_j] = -3 #For the matrix that represents the grid, set the (ij) coordinate to a negative value, so that when each pixel of the body of the snake is at that coordinate, it will see this value, and adjust its direction to go left
        
    def right(self):
        """Move the head of the snake left, as well as change the ij coordinate of the matrix to -1 so that the rest of the body can see the value and also move right when they reach the same ij coordinate"""
        if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
            current_i = self.snake[len(self.snake)-1].i 
            current_j = self.snake[len(self.snake)-1].j
            if self.snake[len(self.snake)-1].vector == [0,1] or self.snake[len(self.snake)-1].vector == [0,-1]:
                #If the snake is currently moving right or left, exit the function to make sure nothing happens
                return
            self.matrix[current_i][current_j] = -1 #For the matrix that represents the grid, set the (ij) coordinate to a negative value, so that when each pixel of the body of the snake is at that coordinate, it will see this value, and adjust its direction to go right

    def up(self):
        """Move the head of the snake up, as well as change the ij coordinate of the matrix to -2 so that the rest of the body can see the value and also move up when they reach the same ij coordinate"""
        if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
            current_i = self.snake[len(self.snake)-1].i 
            current_j = self.snake[len(self.snake)-1].j
            if self.snake[len(self.snake)-1].vector == [1,0] or self.snake[len(self.snake)-1].vector == [-1,]:
                #If the snake is currently moving up or down, exit the function to make sure nothing happens
                return
            self.matrix[current_i][current_j] = -2 #For the matrix that represents the grid, set the (ij) coordinate to a negative value, so that when each pixel of the body of the snake is at that coordinate, it will see this value, and adjust its direction to go up

    def down(self):
        """Move the head of the snake down, as well as change the ij coordinate of the matrix to -4 so that the rest of the body can see the value and also move down when they reach the same ij coordinate"""
        if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
            current_i = self.snake[len(self.snake)-1].i 
            current_j = self.snake[len(self.snake)-1].j
            if self.snake[len(self.snake)-1].vector == [1,0] or self.snake[len(self.snake)-1].vector == [-1,0]:
                #If the snake is currently moving up or down, exit the function to make sure nothing happens
                return
            self.matrix[current_i][current_j] = -4 #For the matrix that represents the grid, set the (ij) coordinate to a negative value, so that when each pixel of the body of the snake is at that coordinate, it will see this value, and adjust its direction to go down
    
    def next(self):
        """As the body of the snakes moves through the grid, each body part will check its (ij) coordinates and compare it to self.matrix[i][j]. If there is a negative value, that means the body part must adjust its vector to a corresponding direction"""
        if self.__pause == False: #If game is paused, do not allow next() to run, cannot have the screen update or have the vectors influence pixels
            for index in range(len(self.snake)-1,-1,-1): #Going backwards
                current_i = self.snake[index].i
                current_j = self.snake[index].j
                if self.matrix[current_i][current_j] == -1:
                    self.snake[index].right()
                elif self.matrix[current_i][current_j] == -2:
                    self.snake[index].up()
                elif self.matrix[current_i][current_j] == -3:
                    self.snake[index].left()
                elif self.matrix[current_i][current_j] == -4:
                    self.snake[index].down()
                self.snake[index].next()
                if index == 0: #After moving through the entirety of the snake, set the corresponding ij coordinate of the grid to a 0 in the matrix representing the grid
                    self.matrix[current_i][current_j] = 0 
            self.collision() #Check for collisions

    def collision(self):
        """Checks for collisions based on the (ij) coordinates of the snake head. If the snake head is at the same (ij) coordinates as an obstacle, fruit, or snake body part, react accordingly"""
        current_i = self.snake[-1].i #Get i coordinate of snake head
        current_j = self.snake[-1].j #Get j coordinate of snake head
        #obstacle
        if self.matrix[current_i][current_j] == 1: #If there is an obstacle in the same place as there is the snake head, then the game is over
            self.__game_over = True
        #fruit
        elif self.matrix[current_i][current_j] == 3: #If there is a fruit in the same place as there is the snake head, the the snake eats the fruit
            pygame.mixer.init() #Play eating sound
            pygame.mixer.music.load("zapsplat_cartoon_pop_short_simple_91196.mp3") #Short and simple cartoon pop from zapsplat.com
            #https://www.zapsplat.com/music/short-and-simple-cartoon-pop/
            pygame.mixer.music.play()
            super().delij(current_i,current_j) #Delete the fruit pixel from the grid
            self.__n_fruit = self.__n_fruit - 1 #Decrease the number of fruit left over
            self.__score += 10 #For each fruit eaten, incrememnt the score by 10
            if self.__n_fruit == 0: #If there are no fruit left over, the game is over
                self.__game_over = True
            #Based on the direction of the last body part of the snake, add an additional body part that is going in the same direction, but one pixel behind the previously last body part
            if self.snake[0].vector == [-1,0]: #going up
                self.snake.insert(0,Pixel(self.canvas,self.snake[0].i + 1,self.snake[0].j,self.nrow,self.ncol,self.scale,5,self.snake[0].vector)) #Add additional body part to the end of the snake that is also going up
            elif self.snake[0].vector == [1,0]: #going down
                self.snake.insert(0,Pixel(self.canvas,self.snake[0].i - 1,self.snake[0].j,self.nrow,self.ncol,self.scale,5,self.snake[0].vector)) #Add additional body part to the end of the snake that is also going down
            elif self.snake[0].vector == [0,1]: #going right
                self.snake.insert(0,Pixel(self.canvas,self.snake[0].i,self.snake[0].j - 1,self.nrow,self.ncol,self.scale,5,self.snake[0].vector)) #Add additional body part to the end of the snake that is also going right
            elif self.snake[0].vector == [0,-1]: #going left
                self.snake.insert(0,Pixel(self.canvas,self.snake[0].i,self.snake[0].j + 1,self.nrow,self.ncol,self.scale,5,self.snake[0].vector)) #Add additional body part to the end of the snake that is also going left
        #Check for collisions of the snake head with snake body part
        for i_index in range(len(self.snake)-1): #Index through entire list of snake
            if self.snake[-1].i == self.snake[i_index].i and self.snake[-1].j == self.snake[i_index].j: #If the snake head has the same (ij) coordinates as a snake body part, then they must have collided
                self.__game_over = True #Since the head has collided with snake body, the game is over
        

    
#########################################################
############# Main code #################################
#########################################################
    

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        python = Snake(root,20,20) #20 obstacles, and 20 fruits
        #python = Snake(root,5,5,25,25,30) # 5 obstacles/fruits, 25 row, 25 column, 30 scale
        
        
        ####### Tkinter binding mouse actions
        root.bind("<Right>",lambda e:python.right())
        root.bind("<Left>",lambda e:python.left())
        root.bind("<Up>",lambda e:python.up())
        root.bind("<Down>",lambda e:python.down())
        root.bind("<p>",lambda e:python.pause())
        
        while True:
            if not python.is_pause(): python.next()
            root.update()
            time.sleep(0.10)  # wait few second (simulation)
            #changed time.sleep from 0.15 to 0.10
            if python.is_game_over(): break
        
        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

