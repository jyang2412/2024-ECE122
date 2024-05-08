#Daniel Zadorozhnyy 34274290
#Jay (Jinmo) Yang 34278275
from tkinter import *
from Grid import Grid
from Tetrominoes import Tetrominoes
import numpy as np
import time
import pygame
        
class Tetris(Grid):
    def __init__(self,root,nrow,ncol,scale):  #initialize variables
        super().__init__(root,nrow,ncol,scale) #Initialize Grid
        self.block = None #Initialize self.block to None for now, change later
        self.__pause = False #Keep track of if the game is paused
        self.__game_over = False #Keep track of if the game is over
        self.num_of_tetrominos_used = 0 #Used for increase the speed of the tetrominos later on


    def is_pause(self):    #return pause status 
        return self.__pause
    
    def pause(self):       #if called, change the pause status
        if self.__pause == False: #if not paused, pause
            self.__pause = True
            print("pause")
        elif self.__pause == True: #if paused, unpause
            self.__pause = False

    def is_game_over(self):
        if self.__game_over == True: #If the game is over, display a game over screen
            pygame.mixer.init()
            pygame.mixer.music.load("zapsplat_multimedia_game_sound_fun_arcade_organ_short_negative_fail_lose_003_54276.mp3") #Game arcade sound from zapsplat.com
            #https://www.zapsplat.com/music/game-sound-fun-arcade-organ-tone-short-negative-fail-or-lose-tone-3/
            pygame.mixer.music.play()
            self.canvas.create_text(self.ncol*self.scale // 2,self.nrow * self.scale // 2,text="GAME OVER",fill="orange",font=("Times New Roman",20))
        return self.__game_over

    def next(self):
        if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
            if self.block == None: #If the block does not have a value, set it to some random tetromino
                self.block = Tetrominoes.random_select(self.canvas,self.nrow,self.ncol,self.scale)
                self.block.activate() #Display onto grid
            
            self.block.down() #Move the tetromino down every frame
            new_i = self.block.i
            new_j = self.block.j

            if new_i == self.nrow - 3: #check collision for bottom rows
                self.in_place()
            elif new_i < self.nrow - 3:
                self.is_overlapping(new_i, new_j) #if the tetromino does not reach the bottom rows, check if it is overlapping with anything
                
    
    def in_place(self):
        """Iterate through the tetromino and place down every pixel associated with it"""
        for index_i in range(len(self.block.get_pattern())):
            for index_j in range(len(self.block.get_pattern()[0])):
                if self.block.get_pattern()[index_i][index_j] > 0:
                    self.addij(self.block.i + index_i, self.block.j + index_j, self.block.get_pattern()[index_i][index_j])
        #delete pixels associated with tetromino
        self.block.delete()
        self.block = None #Set self.block back to None, sso that it can then be initalized to another random tetromino in self.next()
        self.check_row() #After placing a tetromino, check if there is a row that is completely full
        """Scan top three rows, see if there are blocks there, if there are, that means the player has lost"""
        for i in range(3):
            for j in range(self.ncol):
                if self.matrix[i][j] > 0:
                    self.__game_over = True
        self.num_of_tetrominos_used = self.num_of_tetrominos_used + 1 #After placing down a tetromino, increase the number of tetrominos used, this will then be used to increase the speed of the game


    def is_overlapping(self,ii,jj):
        if self.block != None: #Make sure that self.block is not None
            ii = self.block.i + 1 #Get next possible i coordinate
            jj = self.block.j 
            for i_index in range(len(self.block.get_pattern())):
                for j_index in range(len(self.block.get_pattern()[0])): #Iterate through the entire tetromino
                    if self.block.get_pattern()[i_index][j_index] > 0: #For every pixel of the tetromino that is not a black pixel,
                        if self.matrix[ii + i_index][jj + j_index] > 0: #If there is a pixel in the same location
                            self.in_place() #Then set it in place
                            return #Exit function early if there is ever a scenario where the tetromino is overlapping with anything, place it immediately
            
    def is_overlapping_right(self,ii,jj): #put in right() to see if you can move right
        if self.block != None:
            ii = self.block.i
            jj = self.block.j + 1
            for i_index in range(len(self.block.get_pattern())):
                if jj > self.ncol - 3: #keep the tetromino within the bounds of the screen
                    return True 
                elif self.matrix[ii+i_index][jj] > 0: #If there is a pixel to the right, that means it cannot move to the right
                    return True
            return False #If it passes both checks, that means it is NOT overlapping on the right, allow for right movement in right()
                
    def is_overlapping_left(self,ii,jj):
        if self.block != None:
            ii = self.block.i
            jj = self.block.j - 1 #move left
            for i_index in range(len(self.block.get_pattern())):
                if jj < 0: #Keep tetromino within the bounds of the screen on the left side
                    return True
                elif self.matrix[ii+i_index][jj] > 0: #if there is a pixel to the left, that means it will be over lapping
                    return True
            return False #if it passes both conditions (in that they do not activate), that means it can move left in left()

    def check_row(self):
        for i in range(len(self.matrix)): #iterates through every rows
            if 0 not in self.matrix[i]: #if all the pixels are not black, then call flush_row
                self.flush_row(i)

    def up(self): 
        if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
            if self.can_rotate():  #call the can_rotate function to check if the block can be rotated
                self.block.rotate() #if true, rotate the block (to the next pattern)

    def can_rotate(self):
        if self.block != None:
            next_pattern_index = (self.block.currentPattern + 1) % len(self.block.patternList) #variables that represent next patter(after being rotated)
            next_pattern = self.block.patternList[next_pattern_index]
            
            for i_index in range(len(next_pattern)):  #check if the rotated block is overlapping with anything, and if so, return false. Otherwise return true so that we know it's safe to rotate the block
                for j_index in range(len(next_pattern[0])):
                    if next_pattern[i_index][j_index] > 0:
                        if self.matrix[self.block.i + i_index][self.block.j + j_index] > 0:
                            return False
            return True
                                       
    def down(self):
        if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
            while self.block != None: #until the block changes after being in place, call next. This drops the tetrominoe all the way down.
                self.next()

    def right(self):
        if self.block != None:
            if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
                if self.is_overlapping_right(self.block.i,self.block.j): #check if tetrominoe will overlap if moved to the right. If so, return to get out of the function immediately
                    return
                else:
                    self.block.right() #if not overlapping, move the tetrominoe to the right

    def left(self):
        if self.block != None:
            if self.__pause == False: #If the game is paused, prohibit the player from inputting commands
                #check first column of pattern
                if self.is_overlapping_left(self.block.i, self.block.j):  #check if the tetrominoe will overlap if it's moved to the left. If so, return to get out of the function
                    return                      
                else:
                    self.block.left()  #if not overlapping, move the tetrominoe to the left

                    


             

#########################################################
############# Main code #################################
#########################################################

    
def main():
    ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        game=Tetris(root,36,12,15) #change the scale back to 25
        
        ####### Tkinter binding mouse actions
        root.bind("<Up>",lambda e:game.up())
        root.bind("<Left>",lambda e:game.left())
        root.bind("<Right>",lambda e:game.right())
        root.bind("<Down>",lambda e:game.down())
        root.bind("<p>",lambda e:game.pause())        

        while True:
            if not game.is_pause(): game.next()
            root.update()   # update the graphic
            sleep_time = 0.25     #initial sleep time
        
            sleep_time = sleep_time - (0.005*game.num_of_tetrominos_used)  #as game progresses, sleep times decreases gradually
            if sleep_time <= 0.05:
                sleep_time = 0.05
                
            time.sleep(sleep_time)  # wait few second (simulation)
            if game.is_game_over(): break
        
        root.mainloop() # wait until the window is closed


        

if __name__=="__main__":
    main()

