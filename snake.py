import pygame
from random import randrange
from sys import exit

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BLOCK_SIZE = 80

# Random coordinates for apple
def get_random_position():
    x = randrange(0, WINDOW_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    y = randrange(0, WINDOW_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    return x, y

# Check if apple spawned inside snake
def is_apple_in_snake(apple_pos, snake_segments):
    return apple_pos in snake_segments

# Draw background grid
def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "grey", rect, 1)

# Display text
def display_message(text, size, color, y_offset=0):
    font = pygame.font.Font("fonts/data-latin.ttf", size)
    message = font.render(text, True, color)
    message_rect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + y_offset))
    screen.blit(message, message_rect)

# Welcome screen
def welcome_screen():
    while True:
        screen.fill("black")
        display_message("snake.py", 75, "green")
        display_message("Press any key to start", 50, 'white', 100)      
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return

# Game over screen
def game_over(score):
    pygame.mixer.music.stop()
    game_over_sound.play()
    
    while True:
        screen.fill("black")
        display_message(f"Game Over! Your Score: {score}", 75, "red")
        display_message("Press 'R' to Restart or 'Q' to Quit", 50, "white", 100)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main script
def main():
    global screen, game_over_sound # Allows access to draw_grid(), display_message(), welcome_screen(), game_over()
    pygame.init()
    pygame.mixer.init()
    
    # Load sound effects
    background_music = "audio/cyborg-ninja.wav"
    eat_sound = pygame.mixer.Sound("audio/eat-sound.wav")
    eat_sound.set_volume(.8)
    game_over_sound = pygame.mixer.Sound("audio/game-over.wav")
    game_over_sound.set_volume(.2)
    
    # Game window configuration
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("snake.py")
    clock = pygame.time.Clock()
    
    # Show welcome screen
    welcome_screen()
    
    while True:
        game_over_sound.stop() # Stop game over sound playing over music at start of new game
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1) # Loop background music
        pygame.mixer.music.set_volume(.1)
        
        # Snake attributes
        snake_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        snake_surface.fill("green")
        snake_x_pos = 560
        snake_y_pos = 240
        snake_speed = BLOCK_SIZE
        direction = None
        
        # Initialize snake segments & score
        snake_segments = [(snake_x_pos, snake_y_pos)]
        score = 0
        
        # Apple attributes
        apple_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        apple_surface.fill("red")
        apple_x_pos, apple_y_pos = get_random_position()
        apple_rect = apple_surface.get_rect(topleft=(apple_x_pos, apple_y_pos))
        
        # Main gameplay loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit game
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and direction != "DOWN":
                        direction = "UP"
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and direction != "RIGHT":
                        direction = "LEFT"
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and direction != "UP":
                        direction = "DOWN"
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and direction != "LEFT":
                        direction = "RIGHT"
            
        
            # Update snake direction
            if direction:
                # Add new head segment based on direction
                if direction == "UP":
                    new_head = (snake_segments[0][0], snake_segments[0][1] - snake_speed)
                elif direction == "LEFT":
                    new_head = (snake_segments[0][0] - snake_speed, snake_segments[0][1])
                elif direction == "DOWN":
                    new_head = (snake_segments[0][0], snake_segments[0][1] + snake_speed)
                elif direction == "RIGHT":
                    new_head = (snake_segments[0][0] + snake_speed, snake_segments[0][1])
                
                # Check for collision with body
                if new_head in snake_segments:
                    break
                
                # Insert new head segment
                snake_segments = [new_head] + snake_segments[:-1]
            
            # Check for collision with apple
            if snake_segments[0] == (apple_x_pos, apple_y_pos):
                while is_apple_in_snake((apple_x_pos, apple_y_pos), snake_segments): # Regenerate apple position if position inside snake
                    apple_x_pos, apple_y_pos = get_random_position()
                
                eat_sound.play()
                apple_rect.topleft = (apple_x_pos, apple_y_pos) # Move apple to new position
                snake_segments.append(snake_segments[-1]) # Add a new segment to the snake
                score += 1
                
            # Ensure the snake stays within the grid
            head_x, head_y = snake_segments[0]
            if head_x < 0 or head_x >= WINDOW_WIDTH or head_y < 0 or head_y >= WINDOW_HEIGHT:
                break
                
            # Clear screen each frame & draw items
            screen.fill("black")
            draw_grid()
            screen.blit(apple_surface, apple_rect.topleft)
            for segment in snake_segments:
                screen.blit(snake_surface, segment)
            
            # Draw all elements & update frames
            pygame.display.update()
            clock.tick(8)

        # Replay game if 'r' key is pressed
        if game_over(score):
            continue
        
if __name__ == "__main__":
    main()