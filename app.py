import pygame
import random


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
SPEED =40   #Snake speed

#food variables
food_pos = [random.randrange(0,WIDTH,10), random.randrange(0,HEIGHT, 10)]
food_spawn = True

#font for game over message
font = pygame.font.Font(None,36)

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
    
    #check if the snake ears food
    if snake_pos[0] == food_pos:
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



    #draw everything
    screen.fill(BLACK)

    #draw snake
    for segment in snake_pos:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], 10, 10))

    #draw food
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1],10,10))

    pygame.display.flip()
    clock.tick(SPEED)

#show game over message
screen.fill(BLACK)
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