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

#Game loop
def game_loop():
    global high_score, score, snake_pos, snake_dir, food_pos, food_spawn, food_move_counter, paused
    paused = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running =  False
                pygame.quit()
                quit()
                #Movements
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != "DOWN":
                    snake_dir = "UP"
                elif event.key == pygame.K_DOWN and snake_dir != "UP":
                    snake_dir = "DOWN"
                elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                    snake_dir = "RIGHT"
                elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                    snake_dir = "LEFT"
                elif event.key == pygame.K_p: #toggle pause when P is pressed
                    paused = not paused

        #if the game is paused , skip updating the game logic
        if not paused :
            #move the snake
            if snake_dir == "UP":
                new_head = [snake_pos[0][0],snake_pos[0][1] - 10]
            elif snake_dir == "DOWN":
                new_head = [snake_pos[0][0],snake_pos[0][1] + 10]
            elif snake_dir == "LEFT":
                new_head = [snake_pos[0][0] - 10,snake_pos[0][1]]
            elif snake_dir == "RIGHT":
                new_head = [snake_pos[0][0] + 10 , snake_pos[0][1]]

            #Add new head to snake
            snake_pos.insert(0,new_head)
            
            #check if the snake eats food
            if (abs(snake_pos[0][0] - food_pos[0]) < SNAKE_SIZE) and (abs(snake_pos[0][1] - food_pos[1]) < SNAKE_SIZE):
                score+= 1 #increase the score when food is eaten
                food_spawn = False #food eaten, spawn new one
            else:
                snake_pos.pop() #removes the last segment to maintain the length


            #spawn new food
            if not food_spawn:
                while True:
                    food_pos = [random.randrange(0,WIDTH,10), random.randrange(0,HEIGHT,10)]
                    if food_pos not in snake_pos: #ensure food doesn't spawn on snake
                        break
                food_spawn = True


            # Collision detection
            # 1 wall collision
            if ( snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT):
                running = False #end game if snake hits wall
            
            # 2 self collision
            if ( snake_pos[0] in snake_pos[1]):
                running = False # end game if snake bites itself

            
            #high score updates
            if (score > high_score):
                high_score = score #updated high score
            
            #increase speed every 5 points
            SPEED = base_speed + ( score // 5) *2

            # move food every few frames after score 10
            if score >= 5:
                food_move_counter +=1 
                if food_move_counter >= food_move_delay:
                    new_food_pos = [random.randrange(0, WIDTH, 10 ), random.randrange(0, HEIGHT, 10)]

                    # ensure food doesn't move if the snake is close to it
                    if abs(new_food_pos[0] - snake_pos[0][0]) > 20 and abs (new_food_pos[1] - snake_pos[0][1]) > 20:
                        food_pos = new_food_pos
                        food_move_counter = 0 # reset counter after moving food
            # obstacles at high score
            obstacles = []

            # spawn obstacles after score 15
            if score >= 5 and len(obstacles) < 5:
                obstacles.append([random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT,10)])

            #check if snake hits and obstacle
            if snake_pos[0] in obstacles:
                running = False # GAME OVER

        #draw everything
        screen.fill(BLACK)

        #draw snake
        for segment in snake_pos:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

        #draw food
        pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1],FOOD_SIZE,FOOD_SIZE))

        #draw score
        score_text = font.render(f"Score:{score} High score : {high_score}",True,(255,255,255))
        screen.blit(score_text, (10,10))


        # display pause message if the game is paused
        if paused :
            pause_text = font.render("PAUSED - Press 'p' to Resume", True, WHITE)
            screen.blit(pause_text, (WIDTH //4, HEIGHT //2))


        pygame.display.flip()
        clock.tick(SPEED)
    
    
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

#start the game loop
main()
pygame.quit()