"""
Space Dodge Game

This program implements a simple space-themed game called "Space Dodge" using the Pygame library.
 The game is designed to test the player's reaction time and spatial awareness as they navigate a spaceship through a field of moving stars.

Gameplay Overview

In this game, the player controls a spaceship that must avoid colliding with stars that are moving downwards towards it. 
The game ends when a star collides with the spaceship, and the player's score is displayed.

Key Features

Simple and intuitive gameplay
Real-time collision detection and response
Time-based scoring system
Basic graphics and sound effects using Pygame
Code Structure

The program is organized into the following components:

main function: serves as the entry point of the program
Game loop: updates the game state and renders the game graphics
Collision detection system: checks for collisions between the spaceship and stars
Graphics and sound effects: uses Pygame to render the game graphics and play sound effects
Purpose

This program is designed to demonstrate basic game development concepts using Pygame, including game loops, collision detection, and graphics rendering. 
It can be used as a starting point for more complex game development projects or as a learning tool for programmers new to Pygame.
"""

import pygame
import time
import random

#initialize the pygame fornt module
pygame.font.init()

#the pygame window (WIN)
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Space Dodge") #the title of the window

#load the background image and scale it to fit the game window
BG = pygame.transform.scale(pygame.image.load('E:\Ryan\Programing languages\Python\Space doge game\bg.png'), (WIDTH, HEIGHT)).convert()

#the character  (PLAYER)
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
#setting the player valocity
PLAYER_VEL = 5

#the obstacal (STAR)
STAR_WIDTH = 10
STAR_HEIGHT = 20
#setting the stars valocity
STAR_VEL = 3

#create a font object for redering text
FONT = pygame.font.SysFont("comicsans", 30)
def draw(player, elapsed_time, stars):
    """
    Drawing the game elements on the screen.
    Args:
        player  (pygame.Rect): The player's rectangle.
        elapsed_time (float): The time elapsed since the started 
        stars (list):A list of star rectangles
    """
    #draw the background
    WIN.blit(BG, (0, 0))
    #Render the elapsed time as text
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    #Draw the elapsed time on the screen
    WIN.blit(time_text, (10, 10))

    #Draw the player recangle on the screen
    pygame.draw.rect(WIN, "red", player)

    #Draw each star rectangle on the screen
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update() #updating the display to make the drawn elements visible


def main(): #the main game loop
    run = True #init the game loop flag

    #create a player rectangle at the bottom of the screen
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()#clock object controling the frame rate
    start_time = time.time()#recoding the games starting time
    elapsed_time = 0#init the elapsed time

#star addition increment
    star_add_increment = 2000
    star_count = 0 #init the star count

    stars = [] #init the list of str rectangles 
    hit = False #init hit flag

    #game loop
    while run:
        #increment the star count by the time elapsed since the last frame
        star_count += clock.tick(60)
        #calculate the elapsed time since the game sarted
        elapsed_time = time.time() - start_time

        #if the star count exceeds the star addition increment, add new stars
        if star_count > star_add_increment:
            for _ in range(3):
                #generate a random  x position for the new star
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                #create a new star rectangle at the top of the  screen
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star) #add the star to the list of stars

            #decrease the star addition increment to increase the difficulty
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0 #reset the star count
        
        #Handlw events(e.g., closing the game window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#stop the game loop if the game window is closed
                run = False
                break

       #setting the keyboard controles
        keys = pygame.key.get_pressed() #getting the current state of the keyboard 

        #Move the player let if te left arrowkey is pressed
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        
        #Move the player right if the right arrow key is pressed
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        #Move each star downwards
        for star in stars[:]:
            star.y += STAR_VEL
            #remove the star if it goes of the screen
            if star.y > HEIGHT:
                stars.remove(star)
            #check for collision with the player
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star) 
                hit = True #showint that the player is  hit
                break

        #Display you ("You lost !") if the player has been hit
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white") #The text object and the font object
            #The center possition of the text object
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)  #delay for 4 seconds
            break #breaking out of the loop

        #drawing the player and star on the screen
        draw(player, elapsed_time, stars)

    #Quit the pygame library
    pygame.quit()
    
"""
The if__name__ == "__main__": is a special value that indicates whether the module is being run dictly 
or imported as a module by another program
"""
if __name__ == "__main__": #The entry point of the program
    main() #Call the main function to start the game
