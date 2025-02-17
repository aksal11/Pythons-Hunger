import pygame
import random
import os




#initialize the game
pygame.init()
pygame.mixer.init()



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

# load sound effects
# move_sound = pygame.mixer.Sound("menu.wav")
pause_sound = pygame.mixer.Sound("sound/pause.wav")
select_sound = pygame.mixer.Sound("sound/select.wav")
game_over_sound = pygame.mixer.Sound("sound/game_over.wav")
snake_control_sound = pygame.mixer.Sound("sound/snake-control.wav")

#adjust volume
# move_sound.set_volume(0.5)  # Adjust between 0.0 (mute) and 1.0 (full volume)
pause_sound.set_volume(0.5)
select_sound.set_volume(0.5)
game_over_sound.set_volume(0.5)
snake_control_sound.set_volume(0.5)




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
    # Initialize sound effects
    pygame.mixer.init()
    # move_sound = pygame.mixer.Sound("menu.wav")  # Sound for menu navigation
    select_sound = pygame.mixer.Sound("sound/select.wav")  # Sound when selecting an option
    
    running = True
    selected = 0  # 0 - start game, 1 - leaderboard, 2 - exit
    options = ["Start Game", "Leaderboard", "Exit"]

    while running:
        screen.fill(BLACK)
        draw_text("PYTHON'S HUNGER", WIDTH // 2, HEIGHT // 4, GREEN, center=True)

        for i, option in enumerate(options):
            color = RED if i == selected else WHITE  # Highlight the selected option
            draw_text(option, WIDTH // 2, HEIGHT // 2 + i * 50, color, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)  # Move up
                    select_sound.play()
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)  # Move down
                    select_sound.play()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    select_sound.play()
                    pygame.time.delay(200)  # Small delay to allow sound to play
                    
                    if selected == 0:  # Start game
                        return "start"
                    elif selected == 1:  # Leaderboard
                        return "leaderboard"
                    elif selected == 2:  # Exit
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





#game loop
def game_loop():
    global high_score, score, snake_pos, snake_dir, food_pos, food_spawn, food_move_counter, paused
   


   
    # Initialize sound effects
    pygame.mixer.init()
    # move_sound = pygame.mixer.Sound("menu.wav")  # Sound for snake movement
    pause_sound = pygame.mixer.Sound("sound/pause.wav")  # Sound for pausing the game
    select_sound = pygame.mixer.Sound("sound/select.wav")
    game_over_sound = pygame.mixer.Sound("sound/game_over.wav")
    snake_control_sound = pygame.mixer.Sound("sound/snake-control.wav")

    snake_control_sound.set_volume(0.1)
    select_sound.set_volume(0.4)

    paused = False
    running = True


    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Movements
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != "DOWN":
                    snake_dir = "UP"
                    snake_control_sound.play()
                elif event.key == pygame.K_DOWN and snake_dir != "UP":
                    snake_dir = "DOWN"
                    snake_control_sound.play()
                elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                    snake_dir = "RIGHT"
                    snake_control_sound.play()
                elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                    snake_dir = "LEFT"
                    snake_control_sound.play()
                elif event.key == pygame.K_p:  # Pause the game
                    paused = not paused
                    pause_sound.play()

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
                select_sound.play()
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
            

        # draw everything
        screen.fill(BLACK)

        # Draw Snake
        for segment in snake_pos:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

        # Draw Food
        pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE))

        

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
    game_over_sound.play()
    screen.fill(BLACK)  # Clear the screen
    draw_text("GAME OVER", WIDTH // 2, HEIGHT // 3, RED, center=True)
    draw_text("Press ENTER to Restart", WIDTH // 2, HEIGHT // 2, WHITE, center=True)
    draw_text("Press ESC to Exit", WIDTH // 2, HEIGHT // 2 + 50, WHITE, center=True)
    select_sound = pygame.mixer.Sound("sound/select.wav")
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart the game
                    select_sound.play()
                    return "restart"
                elif event.key == pygame.K_ESCAPE:  # Exit the game
                    select_sound.play()
                    pygame.quit()
                    exit()


#start the game loop
main()
pygame.quit()