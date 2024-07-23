import pygame
from random import randrange
from sys import exit
from time import time

# Constants
BLOCK_SIZE = 40
GAME_WIDTH = 16 * BLOCK_SIZE
GAME_HEIGHT = 16 * BLOCK_SIZE
BORDER_WIDTH = 200
WINDOW_WIDTH = GAME_WIDTH + BORDER_WIDTH
WINDOW_HEIGHT = GAME_HEIGHT
HIGH_SCORE_FILE = "data/high_score.txt"

# Random coordinates for apple
def get_random_position():
    x = randrange(0, GAME_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    y = randrange(0, GAME_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    return x, y

# Check if apple spawned inside snake
def is_apple_in_snake(apple_pos, snake_segments):
    return apple_pos in snake_segments

# Draw background grid
def draw_grid():
    for x in range(0, GAME_WIDTH, BLOCK_SIZE):
        for y in range(0, GAME_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "grey", rect, 1)

# Display text
def display_message(text, size, color, y_offset=0, center=True, position=(0,0)):
    font = pygame.font.Font("fonts/data_latin.ttf", size)
    message = font.render(text, True, color)
    if center:
        message_rect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + y_offset))
    else:
        message_rect = message.get_rect(topleft=position)
    screen.blit(message, message_rect)

# Read high score from file
def read_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

# Write high score to file
def write_high_score(high_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(high_score))

# Reset high score to 0
def reset_high_score():
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(0))

# Welcome screen
def welcome_screen():
    while True:
        screen.fill("black")
        display_message("snake.py", 75, "green")
        display_message("Press any key to start", 50, 'white', 100)
        display_message("Press 'del' to start with reset High Score", 15, 'white', 300)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    reset_high_score()
                return

# Game over screen
def game_over(score, start_time, high_score):
    pygame.mixer.music.stop()
    game_over_sound.play()
    
    elapsed_time = int(time() - start_time)
    
    # Update high score if needed
    if score > high_score:
        high_score = score
        write_high_score(high_score)
        
    while True:
        screen.fill("black")
        display_message("Game Over!", 60, "red", -40)
        display_message(f"High Score: {high_score}", 40, "yellow", 20)
        display_message(f"Your Score: {score}", 40, "green", 80)
        if elapsed_time == 1:
            display_message(f"Total Elapsed Time: {elapsed_time} second", 40, "blue", 140) # Singular form of "second" when only 1 second elapsed before game over
        else:
            display_message(f"Total Elapsed Time: {elapsed_time} seconds", 40, "blue", 140)
        display_message("Press 'R' to Restart or 'Q' to Quit", 40, "white", 220)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over_sound.stop() # Stop game over sound playing over music at start of new game
                    return True, high_score
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main script
def main():
    global screen, game_over_sound # Allows access to draw_grid(), display_message(), welcome_screen(), game_over()
    pygame.init()
    pygame.mixer.init()
    
    # Load sound effects
    background_music = "audio/cyborg_ninja.wav"
    eat_sound = pygame.mixer.Sound("audio/eat_sound.wav")
    eat_sound.set_volume(.8)
    game_over_sound = pygame.mixer.Sound("audio/game_over.wav")
    game_over_sound.set_volume(.2)
    high_score_sound = pygame.mixer.Sound("audio/new_high_score.wav")
    high_score_sound.set_volume(.15)
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("snake.py")
    clock = pygame.time.Clock()
    
    # Show welcome screen
    welcome_screen()
    
    high_score = read_high_score()
    
    while True:
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1) # Loop background music
        pygame.mixer.music.set_volume(.1)
        
        # Snake attributes
        snake_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        snake_surface.fill("green")
        snake_x_pos = BLOCK_SIZE * 7
        snake_y_pos = BLOCK_SIZE * 7
        snake_speed = BLOCK_SIZE
        direction = None
        
        # Apple attributes
        apple_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        apple_surface.fill("red")
        apple_x_pos, apple_y_pos = get_random_position()
        apple_rect = apple_surface.get_rect(topleft=(apple_x_pos, apple_y_pos))
        
        # Initialize snake segments, score & time
        snake_segments = [(snake_x_pos, snake_y_pos)]
        score = 0
        start_time = time()
        
        # Main gameplay loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit game
                    pygame.quit()
                    exit()
                # Update snake direction
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and direction != "DOWN":
                        direction = "UP"
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and direction != "RIGHT":
                        direction = "LEFT"
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and direction != "UP":
                        direction = "DOWN"
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and direction != "LEFT":
                        direction = "RIGHT"
            
        
            if direction: # Snake begins moving once a direction key is pressed (i.e. if direction != None)
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
                    
                apple_rect.topleft = (apple_x_pos, apple_y_pos) # Move apple to new position
                snake_segments.append(snake_segments[-1]) # Add a new segment to the snake
                score += 1
                
                if score <= high_score:
                    eat_sound.play() # Play default eat sound if not high score
                else:
                    high_score_sound.play() # Play sound when new high score achieved
                    high_score = score
                    write_high_score(high_score) # Immediately write new high score to high_score.txt
                
            # Ensure the snake stays within the grid
            head_x, head_y = snake_segments[0]
            if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
                break
                
            # Clear screen each frame & draw items
            screen.fill("black")
            draw_grid()
            
            screen.blit(apple_surface, apple_rect.topleft)
            for segment in snake_segments:
                screen.blit(snake_surface, segment)
            
            # Draw game border
            pygame.draw.rect(screen, pygame.color.Color(20, 11, 71), (GAME_WIDTH, 0, BORDER_WIDTH, WINDOW_HEIGHT))
            
            # Display score and time elapsed
            elapsed_time = int(time() - start_time)
            display_message(f"High Score: {high_score}", 25, pygame.color.Color(255, 0, 100), center=False, position=(GAME_WIDTH + 20, 20))
            display_message(f"Score: {score}", 25, pygame.color.Color(255, 0, 100), center=False, position=(GAME_WIDTH + 20, 60))
            display_message(f"Time: {elapsed_time}", 25, pygame.color.Color(255, 0, 100), center=False, position=(GAME_WIDTH + 20, 100))
            
            # Draw all elements & update frames
            pygame.display.update()
            clock.tick(10)

        # Replay game if 'r' key is pressed
        play_again, high_score = game_over(score, start_time, high_score) # Unpack play_again option and updated high_score
        if play_again:
            continue
        
if __name__ == "__main__":
    main()
