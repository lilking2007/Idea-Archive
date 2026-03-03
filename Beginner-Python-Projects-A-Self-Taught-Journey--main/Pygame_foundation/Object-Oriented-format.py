# Import the pygame library, which is a set of Python modules designed for writing video games
import pygame

# Define a function to initialize the game
def init_game():
    # Initialize the pygame modules
    # This is necessary to start using pygame, and it sets up some internal state that pygame needs to function
    pygame.init()
    
    # Set the dimensions of the game window to 800x600 pixels
    # The set_mode function returns a Surface object, which represents the game window
    # The Surface object has methods for drawing on the window, getting the window's dimensions, and more
    screen = pygame.display.set_mode((800, 600))
    
    # Update the full display window to make the changes visible
    # This is necessary because pygame uses a technique called double buffering, where it draws on a hidden surface and then swaps it with the visible surface
    # The update function makes the changes visible by swapping the buffers
    pygame.display.update()
    
    # Return the screen object, which represents the game window
    # This is so that other functions can use the screen object to draw on the window
    return screen

# Define a function to handle events, such as closing the game window
def handle_events(screen):
    # Get a list of all events that have occurred since the last call to this function
    # Events are things like key presses, mouse movements, and window closures
    # The event.get function returns a list of Event objects, which represent the events that have occurred
    for event in pygame.event.get():
        # Check if the event is a request to quit the game (e.g., closing the window)
        # The QUIT event is a special event that pygame sends when the user tries to close the window
        if event.type == pygame.QUIT:
            # If so, return False to indicate that the game should stop running
            # This is so that the game loop can exit and the game can quit
            return False
    # If no quit event was found, return True to indicate that the game should continue running
    # This is so that the game loop can continue running and the game can keep going
    return True

# Define the main game loop function
def game_loop(screen):
    # Initialize a flag to indicate whether the game is still running
    # This flag is used to control the game loop, and it's set to False when the game should quit
    open = True
    
    # Enter the main game loop, which will continue until the game is quit
    # The game loop is the main loop of the game, and it's where the game's logic and drawing code go
    while open:
        # Call the handle_events function to check for quit events
        # This is necessary to handle events like window closures and key presses
        open = handle_events(screen)
        
        # This is where you would put your game logic and drawing code
        # For now, it's just a comment, but you would replace this with your own code
        # Game logic code would go here, such as updating the game state and moving objects around
        # Drawing code would go here, such as drawing the game's graphics and text
        
        # Update the full display window to make the changes visible
        # This is necessary to make the changes visible, and it's the same as the update function in the init_game function
        pygame.display.update()

# Define a function to quit the game
def quit_game():
    # Uninitialize all pygame modules to free up resources
    # This is necessary to clean up after the game and free up any resources that pygame is using
    pygame.quit()
    
    # Exit the Python interpreter to completely close the game
    # This is necessary to completely close the game and exit the Python interpreter
    quit()

# Initialize the game by calling the init_game function
# This sets up the game window and initializes the pygame modules
screen = init_game()

# Start the main game loop by calling the game_loop function
# This starts the game loop and begins the game
game_loop(screen)

# Quit the game by calling the quit_game function
# This quits the game and exits the Python interpreter
quit_game()