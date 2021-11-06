import pygame
import random
import os

pygame.mixer.init()


pygame.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (35, 45, 40)

# Creating Game Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Welcome Image
welimg = pygame.image.load("welcome.png")
welimg = pygame.transform.scale(welimg, (screen_width, screen_height)).convert_alpha()

#Background Image
bgimg = pygame.image.load("games.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game over Image
goimg = pygame.image.load("game.png")
goimg = pygame.transform.scale(goimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes With Aditya")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 35)

# Score and Hiscore
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

# Snake Plotting
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

#
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))
        gameWindow.blit(welimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                
                pygame.mixer.music.load('games.mp3')
                pygame.mixer.music.play()
                
                gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Check if hiscore file exists
    if(not os.path.exists("hiscores.txt")):
        with open("hiscores.txt", "w") as f:
            f.write("0")

    with open("hiscores.txt", "r") as f:
        hiscore = f.read()
        
    # Creating Food
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60

    # Snake Collapse
    while not exit_game:
        if game_over:
            with open("hiscores.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(goimg, (0, 0))
            text_screen("Score: " + str(score ), green, 385, 350)
            
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # Movement Of Snake
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # Cheat Code
                    if event.key == pygame.K_q:
                        score +=10

                    # Quit Game
                    if event.key == pygame.K_t:
                        exit_game = True

                    # Pause
                    pause = 4000
                    if event.key == pygame.K_SPACE:
                        pygame.time.delay(pause)

            # Snake Speed
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # Snake Food Eating
            if abs(snake_x - food_x)<18 and abs(snake_y - food_y)<18:
                score +=10
                food_x = random.randint(20, screen_width - 30)
                food_y = random.randint(50, screen_height - 30)
                snk_length +=5
                if score>int(hiscore):
                    hiscore = score

            # Screen Blitting
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: "+str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            # Head and Size of Snake
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            # Deleting the previous path of Snake
            if len(snk_list)>snk_length:
                del snk_list[0]

            # Checking for collapse with body
            if head in snk_list[:-1]:
                game_over = True
                # Game Over Music
                pygame.mixer.music.load('game.mp3')
                pygame.mixer.music.play()
                
            # Checking for collapse with boundary
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('game.mp3')
                pygame.mixer.music.play()
                
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
