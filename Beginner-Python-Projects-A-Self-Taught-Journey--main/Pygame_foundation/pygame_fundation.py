import pygame #importing the pygame library 
pygame.init() #initialize pygame

# Initialize Pygame
screen = pygame.display.set_mode((800, 600)) #set the display mode to a window size  of 800x600
pygame.display.update() #Update the display to make the window visible

open = True # Initialize a variable to control the game loop
while  open: #Start the game loop
    for event in pygame.event.get(): #Get all events from the queue 
        if event.type == pygame.QUIT: #Check if the user wants to quit 
            open = False  #If the user wants to quit, set the open variable to False to exit the game loop


#game mode:


pygame.quit()  #Quit pygame
quit() #quit the program 