# From the tutorial https://youtu.be/AY9MnQ4x3zk. introduction to pygame
import pygame
from sys import exit  # Import the exit function from the sys module

# Initialize the Pygame modules
pygame.init()

# Set up the the widows display(the display surface), ((WIDTH,HIGHt))
screen = pygame.display.set_mode((800, 400))
# Set the title of the window 
pygame.display.set_caption('Runner')
# Create a clock object to control the frame rate
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)# (font.type, font.size)

#The regular surface
sky_surf = pygame.image.load('E:\Ryan\Programing languages\Python\Runner\graphics\Sky.png').convert()
ground_surf = pygame.image.load('E:\Ryan\Programing languages\Python\Runner\graphics\ground.png').convert()

score_surf = test_font.render('Runner game', True,'Blue')# text_information, anti-aliase "a technique used to improve the appearance of digital images by reducing the visibility of aliasing artifacts", color
score_rect =  score_surf.get_rect(center=(400, 50))


#snail
snail_surf = pygame.image.load('E:\Ryan\Programing languages\Python\Runner\graphics\snail\snail1.png').convert_alpha()# the conversion is to give pygame a simpler format to handle an like the png in result of smothness and flow, it's like a conversion to a more pygame friendly format
snail_rect = snail_surf.get_rect(bottomright = (600, 300))

#player 
player_surf = pygame.image.load('E:\Ryan\Programing languages\Python\Runner\graphics\Player\player_walk_1.png').convert_alpha()# the convert_apha() makes the image wiht transparent part lok correc on the screen
player_rect = player_surf.get_rect(midbottom = (80,300)) # Creates a rectangular(MARKING the sections) hitbox for the player, centered at the bottom, making collision detection easier.

# Main game loop
while True:
    # Handle events (e.g., closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Pygame and exit the program
            pygame.quit()
            exit()        
        #if event.type == pygame.MOUSEMOTION:
            #if player_rect.collidepoint(event.pos):
               # print('collision')

    #(blit) = block image transfer, placing a surfe on another surface and (x, y) is for the position from the top left conner  of the surface
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    pygame.draw.rect(screen, 'pink', score_rect) #display surface, color, score_rectangel,
    pygame.draw.rect(screen,'pink', score_rect,10) #additional  line_width and boder _radius screen.blit(score_surf, score_rect) snail_rect.x -= 4
    screen.blit(score_surf, score_rect)

    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800 #bing carirfull on the right and left, This code brings the snail back to the right side of the window after the stail gets to a point that is <  0, which is the left side of the window
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)

    #mouse_pos = pygame.mouse.get_pos()#  get the mouse position
    #if player_rect.collidepoint(mouse_pos): # check if the mouse is over the player
      #print(pygame.mouse.get_pressed()) #  print the mouse buttons state


    # Update the full display surface to make the changes visible
    pygame.display.update()

    # Limit the frame rate to 60 FPS "the numder of times the game updates and redraws the screen per second the higher the frame rate the smother the high reponsive the game will be "
    clock.tick(60)

    # Alternative method to limit the frame rate:
    # pygame.time.delay(1000 // 60)  # 1000 ms / 60 FPS