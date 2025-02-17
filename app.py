import pygame
import random
import os




#initialize the game
pygame.init()



#set up display
WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Python's Hunger")


#Colors
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

font = pygame.font.Font(None,40)




def draw_text(text, x,y,color = WHITE,center=False):
    # to draw text on the screen
    text_surface = font.render(text, True, color)  # Use render() instead
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)  # Center text at (x, y)
    else:
        text_rect.topleft = (x, y)  # Place text at (x, y) without centering

    screen.blit(text_surface, text_rect)


def main_menu():
    # landing page
    running = True
    selected = 0 # 0 - start game, 1 - leaderboard, 2 -exit
    options = ["Start Game", "Leaderboard", "Exit"]
    while running:
        screen.fill(BLACK)
        draw_text("PYTHON'S HUNGER",WIDTH//2, HEIGHT //4, GREEN, center=True)

        for i, option in enumerate(options):
            color = RED if i == selected else WHITE # Highlight the selected option
            draw_text(option, WIDTH // 2, HEIGHT // 2 + i * 50, color, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: #start the game
                    selected = (selected - 1)% len(options)  #move up
                elif event.key == pygame.K_DOWN: #leaderboard
                    selected = (selected + 1)%len(options) #move down
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: #exit
                    if selected ==0: # start game
                        return "start"
                    elif selected == 1: # leaderboard
                        return "leaderboard"
                    elif selected == 2: #exit
                        pygame.quit()
                        exit()

def show_leaderboard():
    """Display the leaderboard (To be implemented)."""
    screen.fill(BLACK)
    draw_text("Leaderboard (Coming Soon)", WIDTH // 3, HEIGHT // 3, WHITE)
    draw_text("Press ESC to go back", WIDTH // 3, HEIGHT // 2, WHITE)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False  # Return to main menu




# adjusting the size of the snake and food
SNAKE_SIZE = 20
FOOD_SIZE = 20

#snake variables
snake_pos = [[100,100],[90,100],[80,100]] # snake body ( list of segments)
snake_dir = "RIGHT" #initial direction

#snake base speed
base_speed= 25    #Snake speed


#food variables
food_pos = [random.randrange(0,WIDTH - FOOD_SIZE,FOOD_SIZE), random.randrange(0,HEIGHT - FOOD_SIZE, FOOD_SIZE)]
food_spawn = True

#Scoring system
score = 0
high_score = 0

# timer 
food_move_counter = 0 # initialize counter
food_move_delay = 200 #Move food after 100 frames (~4 frames)



#load high score from file
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        content = f.read().strip() #removes spaces/new lines
        if content.isdigit(): #ensure its a valid number
            high_score = int(content)
        else:
            high_score = 0 #rest to  0 if file is empty or invalid
else:
    high_score = 0 #default high score if file doesn't exist
print(f"loaded high score : {high_score}")

#font for high score
font = pygame.font.Font(None, 36)

# #font for game over message
# font = pygame.font.Font(None,36)

#clock to control game speed
clock = pygame.time.Clock()


#reset game
def reset_game():
    global snake_pos, snake_dir, score, food_pos, food_spawn
    snake_pos = [[100,100], [90,100], [80,100]] #reset the snake position
    snake_dir = "RIGHT" #reset direction
    score = 0
    food_pos = [random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)]
    food_spawn = True

#game_over
def game_over():
    global high_score
    #save high score if needed
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score)) #save new high score
    
    #show the high score and game over message
    screen.fill(BLACK)
    score_text = font.render(f"Score:{score} High score: {high_score}", True, (255,255,255))
    screen.blit(score_text, (WIDTH //4, HEIGHT // 2 - 50))  #display above game over text

    #show game over message
    # screen.fill(BLACK)
    text =  font.render("Game Over! Press SPACE to restart or ESC to exit!!",True,WHITE)
    screen.blit(text, (WIDTH //4, HEIGHT//2))
    pygame.display.flip()

    #wait for user input before quitting
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #restart the game
                    reset_game()
                    waiting = False
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()





# Obstacles list should be global so it persists
OBSTACLE_EVENT = pygame.USEREVENT + 1  
pygame.time.set_timer(OBSTACLE_EVENT, 10000)


#game loop
def game_loop():
    global high_score, score, snake_pos, snake_dir, food_pos, food_spawn, food_move_counter, paused
    global obstacles

    obstacles = []
    obstacles_timer = 0 
    obstacle_interval = 1500

    paused = False
    running = True

    # Clear old obstacles and generate new ones at score 15
    obstacles.clear()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Movements
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != "DOWN":
                    snake_dir = "UP"
                elif event.key == pygame.K_DOWN and snake_dir != "UP":
                    snake_dir = "DOWN"
                elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                    snake_dir = "RIGHT"
                elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                    snake_dir = "LEFT"
                elif event.key == pygame.K_p:  # Pause the game
                    paused = not paused
            
            # Triggered every 10 seconds to update obstacles
            elif event.type == OBSTACLE_EVENT:
                obstacles.clear()  # Remove old obstacles
                for _ in range(5):  # Generate 5 new obstacles
                    obstacles.append([random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)])


        if not paused:
            # Move the snake
            if snake_dir == "UP":
                new_head = [snake_pos[0][0], snake_pos[0][1] - 10]
            elif snake_dir == "DOWN":
                new_head = [snake_pos[0][0], snake_pos[0][1] + 10]
            elif snake_dir == "LEFT":
                new_head = [snake_pos[0][0] - 10, snake_pos[0][1]]
            elif snake_dir == "RIGHT":
                new_head = [snake_pos[0][0] + 10, snake_pos[0][1]]

            # Add new head to the snake
            snake_pos.insert(0, new_head)

            # Check if the snake eats food
            if (abs(snake_pos[0][0] - food_pos[0]) < SNAKE_SIZE) and (abs(snake_pos[0][1] - food_pos[1]) < SNAKE_SIZE):
                score += 1
                food_spawn = False
            else:
                snake_pos.pop()  # Remove the last segment to maintain length

            # Spawn new food
            if not food_spawn:
                while True:
                    food_pos = [random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)]
                    if food_pos not in snake_pos:
                        break
                food_spawn = True

            # spawn obstacles
            if score >= 5 and len(obstacles) < 5:
                while len(obstacles) < 5:
                    new_obstacle = [random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)]
                    if new_obstacle not in snake_pos and new_obstacle != food_pos:
                        obstacles.append(new_obstacle)

            # to check if snake hits an obstacle
            if tuple(snake_pos[0]) in [tuple(obs) for obs in obstacles]:  # Convert to tuples for comparison
                choice = game_over_screen()  # Show Game Over Screen
                if choice == "restart":
                    reset_game()
                    return game_loop()  # Restart the game
                else:
                    pygame.quit()
                    exit()


            #change obstacles every obstacle_interval frames
            if obstacles_timer >= obstacle_interval:
                obstacles.clear()
                for _ in range(5):
                    obstacles.append([random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10)])
                obstacle_timer = 0
            

            # Wall Collision
            if (
                snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH
                or snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT
            ):
                choice = game_over_screen()
                if choice == "restart":
                    reset_game()
                    return game_loop()
                else:
                    pygame.quit()
                    exit()

            # Self Collision
            if snake_pos[0] in snake_pos[1:]:
                choice = game_over_screen()
                if choice == "restart":
                    reset_game()
                    return game_loop()
                else:
                    pygame.quit()
                    exit()
            
            for obstacle in obstacles:
                if snake_pos[0] == obstacle:
                    choice = game_over_screen()
                    if choice == "restart":
                        main() 
                    else:
                        pygame.quit()
                        exit()

        # draw everything
        screen.fill(BLACK)

        # Draw Snake
        for segment in snake_pos:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

        # Draw Food
        pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE))

        # draw obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, (255, 165, 0), (obstacle[0], obstacle[1], 20, 20))

        # Draw Score
        score_text = font.render(f"Score: {score} High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Pause message
        if paused:
            pause_text = font.render("PAUSED - Press 'P' to Resume", True, WHITE)
            screen.blit(pause_text, (WIDTH // 4, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(30)

    
    
    main()
    #after the game loop ends, call game_over and check if the game should restart
    if game_over():
        game_loop() # restart the game loop


# main function to start the game
def main():
    while True :
        choice = main_menu()
        if choice == "start":
            reset_game()
            game_loop()
        elif choice == "leaderboard":
            show_leaderboard()

def game_over_screen():
    screen.fill(BLACK)  # Clear the screen
    draw_text("GAME OVER", WIDTH // 2, HEIGHT // 3, RED, center=True)
    draw_text("Press ENTER to Restart", WIDTH // 2, HEIGHT // 2, WHITE, center=True)
    draw_text("Press ESC to Exit", WIDTH // 2, HEIGHT // 2 + 50, WHITE, center=True)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart the game
                    return "restart"
                elif event.key == pygame.K_ESCAPE:  # Exit the game
                    pygame.quit()
                    exit()


#start the game loop
main()
pygame.quit()