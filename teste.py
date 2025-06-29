import pygame
import sys
import random
import math
import time

pygame.display.set_caption('Snake')

pygame.font.init()

game_running = True

width = 480
height = 480

size = (width, height)

window = pygame.display.set_mode(size) # our surface type

pygame.display.set_caption("Snake Game by Nick Rinaldi")

class Food:
    def __init__(self, block_size, surface, x_loc, y_loc): # pass in color and random_x/random_y. block size is a constant 
        self.block_size = block_size
        self.surface = surface # green
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, window):
        window.blit(self.surface, (self.x_loc, self.y_loc))

class Snake:

    def __init__(self, block_size, surface, x_loc, y_loc):
        self.block_size = block_size
        self.surface = surface # red
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.body = []
        self.direction = None
        self.velocity = 20
        self.mask = pygame.mask.from_surface(self.surface)
 
    def draw(self, color, window, block_size):
        self.seg = []
        self.head = pygame.Rect(self.x_loc, self.y_loc, block_size, block_size)
        pygame.draw.rect(window, color, self.head)
        if len(self.body) > 0:
            for unit in self.body:
                segment = pygame.Rect(unit[0], unit[1], block_size, block_size)
                pygame.draw.rect(window, color, segment)
                self.seg.append(segment)

    def add_unit(self):
        if len(self.body) != 0:
            index = len(self.body) - 1
            x = self.body[index][0]
            y = self.body[index][1]
            self.body.append([x, y])
        else:
            self.body.append([1000, 1000])

    def move(self):

        keys = pygame.key.get_pressed()

        for index in range(len(self.body) -1, 0, -1):
            x = self.body[index-1][0]
            y = self.body[index-1][1]
            self.body[index] = [x, y]
        if len(self.body) > 0:
            self.body[0] = [self.x_loc, self.y_loc]
        if self.direction == "right": # if specific constant, keep moving in direction
            self.x_loc += self.velocity
        if self.direction == "left":
            self.x_loc -= self.velocity
        if self.direction == "down":
            self.y_loc += self.velocity
        if self.direction == "up":
            self.y_loc -= self.velocity

    def collision(self, obj):
        return collide(food)


clock = pygame.time.Clock()

def gameOver(snake):

    white = pygame.Color(255, 255, 255)

    display = True
    while display:

        window.fill(white)
        score_font = pygame.font.SysFont("Courier New", 16)
        score_label = score_font.render("Your score was: " + str(len(snake.body) + 1), 1, (0, 0, 0))
        replay_label = score_font.render("To replay, click the mouse button", 1, (0, 0, 0))
        window.blit(score_label, (width/2 - score_label.get_width()/2, 20))
        window.blit(replay_label, (width/2 - replay_label.get_width()/2, 50))
        pygame.display.update()

        for event in pygame.event.get(): # if we hit "x" to close out the game, close out the game.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()

    pygame.quit()
    sys.exit()
    
def collide_food(snake_x, snake_y, obj_x, obj_y):
    distance = math.sqrt((math.pow(snake_x - obj_x, 2)) + (math.pow(snake_y - obj_y, 2)))
    if distance < 20:
        return True
    else:
        return False

def collide_wall(snake_x, snake_y):
    if snake_x > width:
        game_over = True
        return game_over
    if snake_y > height:
        game_over = True
        return game_over
    if snake_x < 0:
        game_over = True
        return game_over
    if snake_y < 0:
        game_over = True
        return game_over


def draw_grid(window, height, width, color):

    grid_blocks = 20

    grid_width = width//grid_blocks
    grid_height = height//grid_blocks

    for i in range(grid_height):
        for j in range(grid_width):
            if (i + j) % 2 == 0:
                square = pygame.Rect((i*grid_blocks, j*grid_blocks), (grid_blocks, grid_blocks))
                pygame.draw.rect(window, (219, 190, 161), square)
            else:
                square2 = pygame.Rect((i*grid_blocks, j*grid_blocks), (grid_blocks, grid_blocks))
                pygame.draw.rect(window, (163, 123, 115), square2)


def display_score():
    score_font = pygame.font.SysFont()

def main():

    score_font = pygame.font.SysFont("comicsans", 32)
    game_over = False

    block_snakes = []

    pygame.init()

    clock = pygame.time.Clock()

    red = pygame.Color(255, 0, 0)
    food_color = pygame.Color(26, 237, 139)
    white = pygame.Color(255, 255, 255)
    black = pygame.Color(0, 0, 0)

    block_size = 20

    randx_green = random.randrange(0, width, 20)
    randy_green = random.randrange(0, height, 20)
    randx_red = random.randrange(0, width, 20)
    randy_red = random.randrange(0, height, 20)

    snake_square = pygame.Surface((block_size, block_size))
    snake_square.fill(black)
    food_square = pygame.Surface((block_size, block_size))
    food_square.fill(food_color)

    snake = Snake(block_size, snake_square, 20, 20) # create snake instance
    food = Food(block_size, food_square, randx_green, randy_green) # create food instance

    def redraw_window():

        draw_grid(window, height, width, black)

    while game_running:

        score_text = score_font.render("Score: {0}".format(str(len(snake.body))), 1, (0, 0, 0))

        clock.tick(10) # time passed between each call 

        redraw_window()

        food.draw(window)

        snake.draw(black, window, block_size)

        window.blit(score_text, (5, 10))

        snake.move()

        for event in pygame.event.get(): # if we hit "x" to close out the game, close out the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and snake.direction != "right"):  # Each of these handles either arrow keys or WASD key events.
                    snake.direction = "left"
                elif (event.key == pygame.K_RIGHT and snake.direction != "left"):
                    snake.direction = "right"
                elif (event.key == pygame.K_UP and snake.direction != "down"):
                    snake.direction = "up"
                elif (event.key == pygame.K_DOWN and snake.direction != "up"):
                    snake.direction = "down"

        keys = pygame.key.get_pressed()

        food_collide = collide_food(snake.x_loc, snake.y_loc, food.x_loc, food.y_loc)
        wall_collide = collide_wall(snake.x_loc, snake.y_loc)

        if food_collide:
            ac_rand_x = random.randrange(0, width, 20) # after collision, random x
            ac_rand_y = random.randrange(0, height, 20) # after collision, random y

            food = Food(block_size, food_square, ac_rand_x, ac_rand_y)
            food.draw(window)

            snake.add_unit()

        if wall_collide:
            gameOver(snake)

        if [snake.x_loc, snake.y_loc] in snake.body[1:]:
            gameOver(snake)

        pygame.display.update()



def main_menu(width, height):

    clock = pygame.time.Clock()
    FPS = 60

    width = width
    height = height

    run = True
    title_font = pygame.font.SysFont("monospace", 16)
    title_font.set_bold(True)
    white = pygame.Color(255, 255, 255)

    while run:
        window.fill(white)
        title_label = title_font.render("Snake Game by Nick Rinaldi ", 1, (0, 0, 0))
        sponser_label = title_font.render("Sponsored by @goodproblemsnyc", 1, (0, 0, 0))
        window.blit(title_label, ((width/2 - title_label.get_width()/2, 320)))
        window.blit(sponser_label, ((width/2 - sponser_label.get_width()/2, 350)))
        pygame.display.update()
        for event in pygame.event.get(): # if we hit "x" to close out the game, close out the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu(width, height)
    