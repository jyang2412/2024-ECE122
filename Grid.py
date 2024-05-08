#Daniel Zadorozhnyy 34274290
#Jay (Jinmo) Yang 34278275
from tkinter import *
from Pixel import Pixel
import numpy as np
import random, time


class Grid:
    def __init__(self, root, nrow, ncol, scale):   #initialize variables and create the grid
        self.root = root
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg="black")
        self.canvas.pack()
        self.pixels=[]
        self.matrix = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                self.canvas.create_rectangle(j*scale, i*scale, j*scale+scale, i*scale+scale, fill="black", outline="gray")

    def random_pixels(self,npixels, cID):    #create given number of pixels in random location
        for num in range(npixels):
            j = random.randint(0,self.ncol-1)
            i = random.randint(0,self.nrow-1)
            self.addij(i,j,cID)

    def addij(self,i,j,c):                   #add pixel at a given location (using coordinates converted to i,j)
        pix = Pixel(self.canvas,i,j,self.nrow,self.ncol,self.scale,c)
        if c>0:
             self.pixels.append(pix)
             self.matrix[i][j]=c

    def addxy(self,x,y):                    #add pixel at a given location (using coordinates from mouse)
        j = int((x // self.scale))
        i = int((y // self.scale))
        print("insert %s %s %s %s %s" % (x,y,i,j,int(self.matrix[i][j])))
        self.addij(i,j,1)


    def delxy(self,x,y):                    #delete pixel at a given location (using coordinates from mouse)
        j = int((x / self.scale))
        i = int((y / self.scale))
        if  self.matrix[i][j]!=0:     #if not black, delete and reset
            self.matrix[i][j] = 0 
            self.reset()    
        elif self.matrix[i][j] == 0:  #if black, flush the row
            self.flush_row(i)

    def delij(self, i, j):                  #delete pixel at a given location (using coordinates converted to i,j)
        if  self.matrix[i][j]!=0:   #same as delxy
            self.matrix[i][j] = 0 
            self.reset()    
        elif self.matrix[i][j] == 0:
            self.flush_row(i)        
        
    def reset(self):                        #reset the grid. Delete pixels and redraw the updated grid
        for i in range(len(self.pixels)):
            self.pixels[i].delete()
        #Recreate grid of pixels using matrix
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if int(self.matrix[i][j]) > 0:
                    self.addij(i,j,int(self.matrix[i][j]))
    
    def flush_row(self,i): #run animation, delete color pixels in a given row, and shifts down the rows above
        leftpixels=[]
        rightpixels=[]
        for index in range(3):
                leftpixels.append(Pixel(self.canvas, i, index, self.nrow, self.ncol, self.scale, 7, vector=[0,2]))
                rightpixels.append(Pixel(self.canvas, i, self.ncol-index, self.nrow, self.ncol, self.scale, 7, vector=[0,-2]))
        for t in range(int(self.ncol / 4)):  #animation
            for pixel in leftpixels:
                pixel.next()
            for pixel in rightpixels:
                pixel.next()
            self.canvas.update()
            time.sleep(0.05)
        for index in range(3):
            leftpixels[index].delete()
            rightpixels[index].delete()
        self.matrix[1:i+1,:] = self.matrix[0:i,:]  #shifts down
        self.matrix[0,:] = 0                       #change matrix element to 0 (black)
        self.reset()                               #call reset to redraw



### To complete






#########################################################
############# Main code #################################
#########################################################

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk()                # instantiate a tkinter window
        mesh = Grid(root,50,30,20) # instantiate a Grid object
        mesh.random_pixels(25,1) # generate 25 random (white) pixels in the Grid

        
        ####### Tkinter binding mouse actions
        root.bind("<Button-1>",lambda e:mesh.addxy(e.x,e.y))
        root.bind("<Button-2>",lambda e:mesh.delxy(e.x,e.y))
        

        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

