# Import the pygame library, which is a set of Python modules designed for writing video games
import pygame

# Define a function to initialize the game
def init_game():
    # Initialize the pygame modules
    pygame.init()
    
    # Set the dimensions of the game window to 800x600 pixels
    screen = pygame.display.set_mode((800, 600))
    
    # Update the full display window to make the changes visible
    pygame.display.update()
    
    # Return the screen object, which represents the game window
    return screen

# Define a function to handle events, such as closing the game window
def handle_events(screen):
    # Get a list of all events that have occurred since the last call to this function
    for event in pygame.event.get():
        # Check if the event is a request to quit the game (e.g., closing the window)
        if event.type == pygame.QUIT:
            # If so, return False to indicate that the game should stop running
            return False
    # If no quit event was found, return True to indicate that the game should continue running
    return True

# Define the main game loop function
def game_loop(screen):
    # Initialize a flag to indicate whether the game is still running
    open = True
    
    # Enter the main game loop, which will continue until the game is quit
    while open:
        # Call the handle_events function to check for quit events
        open = handle_events(screen)
        
        # This is where you would put your game logic and drawing code
        # For now, it's just a comment, but you would replace this with your own code
        
        # Update the full display window to make the changes visible
        pygame.display.update()

# Define a function to quit the game
def quit_game():
    # Uninitialize all pygame modules to free up resources
    pygame.quit()
    
    # Exit the Python interpreter to completely close the game
    quit()

# Initialize the game by calling the init_game function
screen = init_game()

# Start the main game loop by calling the game_loop function
game_loop(screen)

# Quit the game by calling the quit_game function
quit_game()