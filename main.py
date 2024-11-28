import asyncio
import pygame
from random import randrange
from sys import exit
from time import time

# Constants
BLOCK_SIZE = 66
GAME_WIDTH = 16 * BLOCK_SIZE
GAME_HEIGHT = 16 * BLOCK_SIZE
BORDER_WIDTH = 280
WINDOW_WIDTH = GAME_WIDTH + BORDER_WIDTH
WINDOW_HEIGHT = GAME_HEIGHT
HIGH_SCORE_FILE = "data/high_score.txt"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Initialize default starting color as green
start_color = (0, 255, 0)
end_color = (0, 100, 0)

is_music_muted = False # Global variable for toggle_music()

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
def display_message(text, size, color: pygame.Color, y_offset = 0, center = True, position = (0,0)):
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
    write_high_score(0)

# Mute & unmute music
def toggle_music():
    global is_music_muted
    if is_music_muted:
        pygame.mixer.music.set_volume(0.1)
        is_music_muted = False
    else:
        pygame.mixer.music.set_volume(0)
        is_music_muted = True

# Interpolate snake color for gradient
def interpolate_color(start_color, end_color, factor):
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * factor),
        int(start_color[1] + (end_color[1] - start_color[1]) * factor),
        int(start_color[2] + (end_color[2] - start_color[2]) * factor)
    )

# Welcome screen
async def welcome_screen():
    while True:
        screen.fill("black")
        display_message("snake.py", 200, "green")
        display_message("Press any key to start", 95, "white", 250)
        display_message("Press 'del' to start with reset High Score", 30, "white", 500)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE: # Start game with reset high score
                    reset_high_score()
                elif event.key == pygame.K_ESCAPE: # Allow to exit game on main menu by pressing escape
                    pygame.quit()
                    exit()
                return
            
        await asyncio.sleep(0)

# Color select screen
async def color_selection_screen():
    while True:
        screen.fill("black")
        display_message("Select Snake Color", 85, "white")
        display_message("Press 'R' for Red", 50, RED, 100)
        display_message("Press 'O' for Orange", 50, ORANGE, 150)
        display_message("Press 'Y' for Yellow", 50, YELLOW, 200)
        display_message("Press 'G' for Green", 50, GREEN, 250)
        display_message("Press 'B' for Blue", 50, BLUE, 300)
        display_message("Press 'P' for Purple", 50, PURPLE, 350)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return RED, (100, 0, 0)
                elif event.key == pygame.K_o:
                    return ORANGE, (100, 50, 0)
                elif event.key == pygame.K_y:
                    return YELLOW, (185, 165, 0)
                elif event.key == pygame.K_g:
                    return GREEN, (0, 100, 0)
                elif event.key == pygame.K_b:
                    return BLUE, (0, 0, 100)
                elif event.key == pygame.K_p:
                    return PURPLE, (64, 0, 64)
                
        await asyncio.sleep(0)
        
# Game over screen
async def game_over(score, start_time, high_score):
    pygame.mixer.music.stop()
    game_over_sound.play()
    elapsed_time = int(time() - start_time)
    
    # Update high score if needed
    if score > high_score:
        high_score = score
        write_high_score(high_score)
        
    while True:
        screen.fill("black")
        display_message("Game Over!", 150, "red", -60)
        display_message(f"High Score: {high_score}", 80, "yellow", 65)
        display_message(f"Your Score: {score}", 80, "green", 160)
        if elapsed_time == 1:
            display_message(f"Total Elapsed Time: {elapsed_time} second", 60, "blue", 260) # Singular form of "second" when only 1 second elapsed before game over
        else:
            display_message(f"Total Elapsed Time: {elapsed_time} seconds", 60, "blue", 260)
        display_message("Press 'R' to Restart | 'C' to change color | 'Q' to Quit", 40, "white", 380)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over_sound.stop() # Stop game over sound playing over music at start of new game
                    return True, high_score, False
                elif event.key == pygame.K_c:
                    return False, high_score, True
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                    
        await asyncio.sleep(0)
        
# Main script
async def main():
    global screen, game_over_sound # Allows access for draw_grid(), display_message(), welcome_screen(), game_over()
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)  # Improves sound quality
    pygame.mixer.init()
    
    # Load sound effects
    snake_move_sound = pygame.mixer.Sound("audio/snake_move.ogg")
    snake_move_sound.set_volume(.5)
    eat_sound = pygame.mixer.Sound("audio/eat_sound.ogg")
    eat_sound.set_volume(.8)
    game_over_sound = pygame.mixer.Sound("audio/game_over.ogg")
    game_over_sound.set_volume(.2)
    high_score_sound = pygame.mixer.Sound("audio/new_high_score.ogg")
    high_score_sound.set_volume(.15)
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("snake.py")
    clock = pygame.time.Clock()
    
    # Show welcome screen
    await welcome_screen()
    # Show color selection screen and get gradient colors
    start_color, end_color = await color_selection_screen()
    high_score = read_high_score()
    
    while True:
        pygame.mixer.music.load("audio/cyborg_ninja.ogg")
        pygame.mixer.music.play(-1) # Loop background music
        pygame.mixer.music.set_volume(.1)
        
        # Snake attributes
        snake_x_pos = BLOCK_SIZE * 7
        snake_y_pos = BLOCK_SIZE * 7
        snake_speed = BLOCK_SIZE
        direction = None
            
        # Apple surface & attributes
        apple_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        if start_color == RED:
            apple_surface.fill(GREEN) # Make apple green if snake is red
        else:
            apple_surface.fill(RED)
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
                    pygame.quit()
                    exit()
                # Update snake direction
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and direction != "DOWN":
                        snake_move_sound.play()
                        direction = "UP"
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and direction != "RIGHT":
                        snake_move_sound.play()
                        direction = "LEFT"
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and direction != "UP":
                        snake_move_sound.play()
                        direction = "DOWN"
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and direction != "LEFT":
                        snake_move_sound.play()
                        direction = "RIGHT"
                    elif event.key == pygame.K_m: # Mute/unmute music
                        toggle_music()
                
            if direction: # Snake begins moving once a direction key is pressed (i.e. if direction != None)
                # Add new head segment based on direction
                if direction == "UP" and (direction != "DOWN" and direction != "LEFT" and direction != "RIGHT"): # Make sure snake does not try to move opposing directions and run into itself
                    new_head = (snake_segments[0][0], snake_segments[0][1] - snake_speed)
                elif direction == "LEFT" and (direction != "DOWN" and direction != "UP" and direction != "RIGHT"):
                    new_head = (snake_segments[0][0] - snake_speed, snake_segments[0][1])
                elif direction == "DOWN" and (direction != "UP" and direction != "LEFT" and direction != "RIGHT"):
                    new_head = (snake_segments[0][0], snake_segments[0][1] + snake_speed)
                elif direction == "RIGHT" and (direction != "DOWN" and direction != "LEFT" and direction != "UP"):
                    new_head = (snake_segments[0][0] + snake_speed, snake_segments[0][1])
                    
                # Check for collision with body
                if new_head in snake_segments and (new_head != snake_segments[1] and new_head != snake_segments[2]): # Collision with head and the two segments immediately behind should not count (avoids accidental death by sharp turns and death with only two or three segments):
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
            screen.fill(BLACK)
            draw_grid()
            
            screen.blit(apple_surface, apple_rect.topleft)
            
            # Draw snake with gradient
            for index, segment in enumerate(snake_segments):
                factor = index / (len(snake_segments) - 1) if len(snake_segments) > 1 else 0
                segment_color = interpolate_color(start_color, end_color, factor)
                snake_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                snake_surface.fill(segment_color)
                screen.blit(snake_surface, segment)
            
            # Draw game border
            pygame.draw.rect(screen, pygame.color.Color(20, 11, 71), (GAME_WIDTH, 0, BORDER_WIDTH, WINDOW_HEIGHT))
            
            # Display score and time elapsed
            elapsed_time = int(time() - start_time)
            display_message(f"High Score: {high_score}", 30, pygame.color.Color(255, 0, 50), center=False, position=(GAME_WIDTH + 20, 20))
            display_message(f"Score: {score}", 30, pygame.color.Color(255, 0, 50), center=False, position=(GAME_WIDTH + 20, 80))
            display_message(f"Time: {elapsed_time}", 30, pygame.color.Color(255, 0, 50), center=False, position=(GAME_WIDTH + 20, 140))
            
            # Draw all elements & update frames
            pygame.display.update()
            clock.tick(10)

            await asyncio.sleep(0)
        # Replay game if 'r' key is pressed
        play_again, high_score, change_color = await game_over(score, start_time, high_score) # Unpack play_again option and updated high_score
        if play_again:
            continue
        elif change_color:
            start_color, end_color = await color_selection_screen()
            
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())