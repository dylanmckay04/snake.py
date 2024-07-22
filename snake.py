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

# Draw background grid
def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "grey", rect, 1)
            
def main():
    global screen # Allows draw_grid() to access screen
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake.py")
    clock = pygame.time.Clock()
    
    snake_surface = pygame.Surface((80, 80))
    snake_surface.fill("green")
    snake_x_pos = 560
    snake_y_pos = 240
    snake_rect = snake_surface.get_rect(topleft=(snake_x_pos, snake_y_pos))
    snake_speed = BLOCK_SIZE
    direction = None
    
    apple_surface = pygame.Surface((80, 80))
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
                if event.key == pygame.K_w or event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
        
        # Update snake direction
        if direction == "UP":
            snake_y_pos -= snake_speed
        elif direction == "LEFT":
            snake_x_pos -= snake_speed
        elif direction == "DOWN":
            snake_y_pos += snake_speed
        elif direction == "RIGHT":
            snake_x_pos += snake_speed
        
        # Game over screen if snake touches walls or self
        if snake_x_pos > WINDOW_WIDTH - BLOCK_SIZE or snake_y_pos > WINDOW_HEIGHT - BLOCK_SIZE:
            break
        
        # Update rectangle positions
        snake_rect.topleft = (snake_x_pos, snake_y_pos)
        apple_rect.topleft = (apple_x_pos, apple_y_pos)
        
        # Check for collision
        if snake_rect.colliderect(apple_rect):
            apple_x_pos, apple_y_pos = get_random_position()
            apple_rect.topleft = (apple_x_pos, apple_y_pos)
            
        # Clear screen each frame & draw items
        screen.fill("black")
        draw_grid()
        
        screen.blit(apple_surface, apple_rect.topleft)
        screen.blit(snake_surface, snake_rect.topleft)
        
        # Draw all elements & update frames
        pygame.display.update()
        clock.tick(8)

if __name__ == "__main__":
    main()