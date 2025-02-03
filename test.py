"""

Test file 
Project: Python's Hunger (Snake Game)
Description: A classic Snake game implemented in Python using the Pygame library.
             The player controls a snake to eat food, grow longer, and avoid collisions
             with walls or itself. The game includes a scoring system and dynamic speed.

Author: Aksal Manoj
Date: October 10, 2023
Version: 1.0

Dependencies:
    - Python 3.x
    - Pygame library (install via `pip install pygame`)

Usage:
    - Run the script using Python: `python snake_game.py`
    - Use arrow keys to control the snake's direction.
    - Press 'Q' to quit the game.


"""

import pygame
import random
import os

# Initialize the game
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python's Hunger")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Snake variables
snake_pos = [[100, 100], [90, 100], [80, 100]]  # snake body (list of segments)
snake_dir = "RIGHT"  # initial direction

# Snake base speed
BASE_SPEED = 25  # Base speed set to 40
speed = BASE_SPEED  # Current speed starts at base

# Food variables
food_pos = [random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)]
# Ensure initial food is not on snake's body
while food_pos in snake_pos:
    food_pos = [random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)]
food_spawn = True

# Scoring system
score = 0
high_score = 0

# Load high score from file
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        content = f.read().strip()
        if content.isdigit():
            high_score = int(content)
        else:
            high_score = 0
else:
    high_score = 0
print(f"Loaded high score: {high_score}")

# Font for score display
font = pygame.font.Font(None, 36)

# Clock to control game speed
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Movement controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                snake_dir = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                snake_dir = "DOWN"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                snake_dir = "RIGHT"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                snake_dir = "LEFT"

    # Move the snake
    if snake_dir == "UP":
        new_head = [snake_pos[0][0], snake_pos[0][1] - 10]
    elif snake_dir == "DOWN":
        new_head = [snake_pos[0][0], snake_pos[0][1] + 10]
    elif snake_dir == "LEFT":
        new_head = [snake_pos[0][0] - 10, snake_pos[0][1]]
    elif snake_dir == "RIGHT":
        new_head = [snake_pos[0][0] + 10, snake_pos[0][1]]

    # Insert new head
    snake_pos.insert(0, new_head)

    # Check if snake eats food
    if snake_pos[0] == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_pos.pop()  # Remove tail if no food eaten

    # Spawn new food if needed
    if not food_spawn:
        while True:
            new_food = [random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)]
            if new_food not in snake_pos:
                food_pos = new_food
                break
        food_spawn = True

    # Collision detection with walls
    if (snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or
        snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT):
        running = False

    # Self-collision detection
    if snake_pos[0] in snake_pos[1:]:
        running = False

    # Update high score
    if score > high_score:
        high_score = score

    # Adjust speed based on score (base speed + 2 per 5 points)
    speed = BASE_SPEED + (score // 5) * 2

    # Move food periodically after score 10
    if score >= 10 and random.randint(1, 40) == 1:
        new_food_pos = [random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)]
        # Check distance from snake head before moving
        if (abs(new_food_pos[0] - snake_pos[0][0]) > 20 and
            abs(new_food_pos[1] - snake_pos[0][1]) > 20):
            food_pos = new_food_pos

    # Draw everything
    screen.fill(BLACK)
    for segment in snake_pos:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], 10, 10))
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], 10, 10))

    # Display score
    score_text = font.render(f"Score: {score} High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)  # Control game speed

# Save high score
if score > high_score:
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Game over screen
screen.fill(BLACK)
score_text = font.render(f"Score: {score} High Score: {high_score}", True, WHITE)
game_over_text = font.render("Game Over! Press any key to exit.", True, WHITE)
screen.blit(score_text, (WIDTH // 4, HEIGHT // 2 - 50))
screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
pygame.display.flip()

# Wait for user input to exit
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()