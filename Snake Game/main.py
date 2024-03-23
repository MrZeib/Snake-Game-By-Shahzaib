import pygame as pg
from random import randint
import os

pg.init()
pg.font.init()
pg.mixer.init()
food = pg.mixer.Sound("food.wav")
over = pg.mixer.Sound("over.wav")
icon = pg.image.load("snake.png")

screen_height : int = 800
screen_width : int = 500
font = pg.font.SysFont(None, 55)
clock = pg.time.Clock()
red : tuple = (255, 0, 0)
white : tuple = (255, 255, 255)
black : tuple = (0, 0, 0)

gameWindow = pg.display.set_mode((screen_height, screen_width))
pg.display.set_caption("Snak Game by Shahzaib Arain")
pg.display.set_icon(icon)
pg.display.update()

def plot_snake(gameWindow, color, snake_list, size):
    for x, y in snake_list:
        pg.draw.rect(gameWindow, color, [x, y, size, size])

def text_on_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def welcome():
    exit_game = True
    while exit_game:
        gameWindow.fill(black)
        text_on_screen("Welcome to Snaky Waik", white, 170, (screen_height/5)+20)
        text_on_screen("Press Enter To Play", white, 210, (screen_height/4)+20)
        text_on_screen("Created by Shahzaib", white, 200, (screen_height/2))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_game = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    gameLoop()
                    return
                if event.key == pg.K_ESCAPE:
                    exit_game : bool = True
                    return

        pg.display.update()
        clock.tick(60)

def gameLoop():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            high_score : int = int(f.read())
    else:
        with open("highscore.txt", "w") as f:
            f.write("0")
            high_score : int = 0
    exit_game : bool = False
    game_over : bool = False
    snack_x : int = 55
    snack_y : int = 55
    size : int = 20
    fps : int = 50
    velocity_x : int = 0
    velocity_y : int = 0
    init_velocity : int = 5
    food_x : int = randint(30, screen_height-30)
    food_y : int = randint(30, screen_width-30)
    score : int = 0
    distance : int = 10
    snake_length : int = 1
    snake_list : list = []
    snake_death : bool = True
    sides_death : bool = True
    while not exit_game:
        if game_over:
            gameWindow.fill(red)
            text_on_screen("Game Over!", white, (screen_width/2)+20, (screen_height/5)+20)
            text_on_screen("Press Enter to Restart the Game", white, 110, (screen_height/4)+20)
            text_on_screen("Created by Shahzaib", white, 200, (screen_height/2))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game : bool = True
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        gameLoop()
                        return
                        game_over = False
                    if event.key == pg.K_ESCAPE:
                        exit_game : bool = True
                        return
        else:
            gameWindow.fill(white)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game : bool = True
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit_game : bool = True
                        return
                    if event.key == pg.K_RIGHT:
                        velocity_x : int = init_velocity
                        velocity_y : int = 0
                    if event.key == pg.K_LEFT:
                        velocity_x : int = -init_velocity
                        velocity_y : int = 0
                    if event.key == pg.K_UP:
                        velocity_x : int = 0
                        velocity_y : int = -init_velocity
                    if event.key == pg.K_DOWN:
                        velocity_x : int = 0
                        velocity_y : int = init_velocity
                    if event.key == pg.K_x:
                        if snake_death:
                            snake_death : bool = False
                        else:
                            snake_death : bool = True
                    if event.key == pg.K_z:
                        score += 5
                    if event.key == pg.K_c:
                        if sides_death:
                            sides_death : bool = False
                        else:
                            sides_death : bool = True
                        
            if abs(snack_x - food_x) < distance and abs(snack_y - food_y) < distance:
                food.play()
                score += 1
                food_x : int = randint(30, screen_height-30)
                food_y : int = randint(30, screen_width-30)
                snake_length += 5
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))
            
            if sides_death:
                if snack_x < 0:
                    over.play()
                    game_over : bool = True
                elif snack_x > screen_width+280:
                    over.play()
                    game_over : bool = True
                elif snack_y > screen_height - 320:
                    over.play()
                    game_over : bool = True
                elif snack_y < 0:
                    over.play()
                    game_over : bool = True
            else:
                if snack_x < 0:
                    snack_x = screen_width+280
                elif snack_x > screen_width+280:
                    snack_x = -1
                elif snack_y > screen_height - 320:
                    snack_y = 0
                elif snack_y < 0:
                    snack_y = screen_height - 320
                
            snack_x += velocity_x
            snack_y += velocity_y
            head : list = []
            head.append(snack_x)
            head.append(snack_y)
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]
            if head in snake_list[:-1] and snake_death:
                over.play()
                game_over = True
            text_on_screen(f"Score: {score}  High Score: {high_score}", black, 5, 5)
            pg.draw.rect(gameWindow, red, [food_x, food_y, size, size], border_radius=8)
            plot_snake(gameWindow, black, snake_list, size)
        pg.display.update()
        clock.tick(fps)

welcome()
pg.quit()
quit()