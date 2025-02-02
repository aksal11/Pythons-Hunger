import pygame
import random
import os


#initialize the game
pygame.init()

#set up display
WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Python's Hunger")


#Colors
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)


#snake variables
snake_pos = [[100,100],[90,100],[80,100]] # snake body ( list of segments)
snake_dir = "RIGHT" #initial direction
SPEED =15   #Snake speed

#food variables
food_pos = [random.randrange(0,WIDTH,10), random.randrange(0,HEIGHT, 10)]
food_spawn = True

#Scoring system
score = 0
high_score = 0

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


#Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =  False
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
    if snake_pos[0] == food_pos:
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



    #draw everything
    screen.fill(BLACK)

    #draw snake
    for segment in snake_pos:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], 10, 10))

    #draw food
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1],10,10))

    #draw score
    score_text = font.render(f"Score:{score} High score : {high_score}",True,(255,255,255))
    screen.blit(score_text, (10,10))

    pygame.display.flip()
    clock.tick(SPEED)

    #save high score to file
    if score > high_score:
        high_score = score
        with open("highscore.txt","w") as f:
            f.write(str(high_score)) #new high score saved



#show the high score
score_text = font.render(f"Score:{score} High score: {high_score}", True, (255,255,255))
screen.blit(score_text, (WIDTH //4, HEIGHT // 2 - 50))  #display above game over text

#show game over message
# screen.fill(BLACK)
text =  font.render("Game Over! Press any key to exit!!",True,WHITE)
screen.blit(text, (WIDTH //4, HEIGHT//2))
pygame.display.flip()

#wait for user input before quitting
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False
pygame.quit()