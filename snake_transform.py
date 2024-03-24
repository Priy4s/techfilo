import pygame
import time
import random

pygame.init()

width = 800
height = 600
block_size = 20
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

clock = pygame.time.Clock()

snake_speed = 15
font = pygame.font.SysFont(None, 25)

class PowerUp:
    def __init__(self, power_up_type):
        self.x = round(random.randrange(0, width - block_size) / block_size) * block_size
        self.y = round(random.randrange(0, height - block_size) / block_size) * block_size
        self.color = (0, 0, 0)
        self.power_up_type = power_up_type  # Type of power-up: "speed", "growth", or "invincibility"
        
        if self.power_up_type == "speed":
            self.color = (0, 0, 255)  # Blue for speed power-up
        elif self.power_up_type == "growth":
            self.color = (255, 255, 0)  # Yellow for growth power-up
        elif self.power_up_type == "invincibility":
            self.color = (128, 0, 128)  # Purple for invincibility power-up

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, block_size, block_size])

def handle_power_up_effect(power_up_type, snakeLength):
    global snake_speed

    if power_up_type == "speed":
        snake_speed += 3  # Increase snake speed
    elif power_up_type == "growth":
        snakeLength += 1  # Increase snake length
    
    return snakeLength  # Return the updated snake length

def generate_obstacles():
    obstacles = []
    for _ in range(10):  # You can adjust the number of obstacles
        obstacle_x = round(random.randrange(0, width - block_size) / block_size) * block_size
        obstacle_y = round(random.randrange(0, height - block_size) / block_size) * block_size
        obstacles.append((obstacle_x, obstacle_y))
    return obstacles

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(gameDisplay, white, [obstacle[0], obstacle[1], block_size, block_size])

def snake(block_size, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [width / 6, height / 2])

def gameLoop():
    global snake_speed

    gameExit = False
    gameOver = False
    snake_speed = 10

    lead_x = width / 2
    lead_y = height / 2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX = round(random.randrange(0, width - block_size) / block_size) * block_size
    randAppleY = round(random.randrange(0, height - block_size) / block_size) * block_size

    score = 0  # Initialize score variable

    power_ups = []  # List to store active power-ups

    obstacles = generate_obstacles()  # Generate initial obstacles
    obstacles_changed = False  # Variable to track if obstacles have been changed

    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(black)
            message_to_screen("Game over! Score: " + str(score) + ". Klik op c om opnieuw te starten", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        if lead_x >= width or lead_x < 0 or lead_y >= height or lead_y < 0:
            gameOver = True

        # Check if snake hits an obstacle
        for obstacle in obstacles:
            if lead_x == obstacle[0] and lead_y == obstacle[1]:
                gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])

        # Draw power-ups
        for power_up in power_ups:
            power_up.draw()

        # Check if snake eats a power-up
        for power_up in power_ups:
            if lead_x == power_up.x and lead_y == power_up.y:
                snakeLength = handle_power_up_effect(power_up.power_up_type, snakeLength)
                power_ups.remove(power_up)  # Remove the power-up from the list
                score += 1  # Increment score when power-up is eaten

        # Change obstacles after every 5 points if they haven't already been changed
        if score % 5 == 0 and not obstacles_changed:
            obstacles = generate_obstacles()
            obstacles_changed = True

        # Draw obstacles
        draw_obstacles(obstacles)

        # Generate new power-up randomly
        if random.randrange(0, 100) < 3:  # Adjust the probability as needed
            power_up_type = random.choice(["speed", "growth"])  # Exclude "invincibility"
            power_ups.append(PowerUp(power_up_type))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        pygame.display.update()

        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = round(random.randrange(0, width - block_size) / block_size) * block_size
            randAppleY = round(random.randrange(0, height - block_size) / block_size) * block_size
            snakeLength += 1
            score += 1  # Increment score when apple is eaten
            obstacles_changed = False  # Reset obstacles_changed flag

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()




