import pygame
import numpy as np
import random
import threading
import cv2

# Screen dimensions
WIDTH, HEIGHT = 800, 800

# Slime parameters
NUM_SLIME = 500
SPEED = 1
SENSOR_DISTANCE = 10
ROTATION_ANGLE = np.pi / 4  # 45 degrees
DEPOSIT_AMOUNT = 1
EVAPORATION_RATE = 0.01
MUTATION_RATE = 0.1
FOOD_ATTRACTION = 0.02
AVOIDANCE_RADIUS = 10

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Slime Simulation')

# Slime class
class Slime:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.angle = random.uniform(0, 2 * np.pi)
        self.food_pheromone = 0

    def move(self):
        self.x += np.cos(self.angle) * SPEED
        self.y += np.sin(self.angle) * SPEED

        # Wrap around the screen edges
        self.x %= WIDTH
        self.y %= HEIGHT

        # Deposit pheromones
        deposit_x = int(self.x)
        deposit_y = int(self.y)
        if 0 <= deposit_x < WIDTH and 0 <= deposit_y < HEIGHT:
            pheromones[deposit_x, deposit_y] += DEPOSIT_AMOUNT

    def sense_and_turn(self):
        left_sensor_x = self.x + np.cos(self.angle - ROTATION_ANGLE) * SENSOR_DISTANCE
        left_sensor_y = self.y + np.sin(self.angle - ROTATION_ANGLE) * SENSOR_DISTANCE

        right_sensor_x = self.x + np.cos(self.angle + ROTATION_ANGLE) * SENSOR_DISTANCE
        right_sensor_y = self.y + np.sin(self.angle + ROTATION_ANGLE) * SENSOR_DISTANCE

        front_sensor_x = self.x + np.cos(self.angle) * SENSOR_DISTANCE
        front_sensor_y = self.y + np.sin(self.angle) * SENSOR_DISTANCE

        left_sensor_value = get_pheromone_value(left_sensor_x, left_sensor_y)
        right_sensor_value = get_pheromone_value(right_sensor_x, right_sensor_y)
        front_sensor_value = get_pheromone_value(front_sensor_x, front_sensor_y)

        if front_sensor_value > left_sensor_value and front_sensor_value > right_sensor_value:
            pass  # Continue straight
        elif left_sensor_value > right_sensor_value:
            self.angle -= ROTATION_ANGLE
        elif right_sensor_value > left_sensor_value:
            self.angle += ROTATION_ANGLE
        else:
            self.angle += random.uniform(-ROTATION_ANGLE, ROTATION_ANGLE)  # Random turn

        # Attraction to food sources
        self.food_pheromone = max(self.food_pheromone - FOOD_ATTRACTION, 0)
        for food_source in food_sources:
            distance = np.sqrt((self.x - food_source.x) ** 2 + (self.y - food_source.y) ** 2)
            if distance < SENSOR_DISTANCE:
                self.food_pheromone += FOOD_ATTRACTION
                self.angle = np.arctan2(food_source.y - self.y, food_source.x - self.x)

        # Avoidance of obstacles and other slimes
        for obstacle in obstacles:
            if obstacle.is_within(self.x, self.y, AVOIDANCE_RADIUS):
                self.angle += np.pi  # Turn around

        for other in slimes:
            if other != self:
                distance = np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < AVOIDANCE_RADIUS:
                    self.angle += np.pi  # Turn around

def get_pheromone_value(x, y):
    x = int(x) % WIDTH
    y = int(y) % HEIGHT
    return pheromones[x, y]

# Obstacle class
class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def is_within(self, x, y, radius):
        return (self.x - radius < x < self.x + self.width + radius and
                self.y - radius < y < self.y + self.height + radius)

# FoodSource class
class FoodSource:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)

def update_slimes(slimes):
    for slime in slimes:
        slime.sense_and_turn()
        slime.move()

# Create slime instances
slimes = [Slime() for _ in range(NUM_SLIME)]

# Obstacle list
obstacles = []

# Create food sources
food_sources = [FoodSource(random.randint(0, WIDTH), random.randint(0, HEIGHT), 5) for _ in range(5)]

# Pheromone grid
pheromones = np.zeros((WIDTH, HEIGHT))

# Initialize video writer with higher quality settings
fps = 30
scale_factor = 2  # Increase resolution
video_writer = cv2.VideoWriter('slime_simulation.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (WIDTH * scale_factor, HEIGHT * scale_factor))

# Main loop
running = True
drawing = False
start_pos = None
drawing_complete = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not drawing_complete:
            drawing = True
            start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = event.pos
            x = min(start_pos[0], end_pos[0])
            y = min(start_pos[1], end_pos[1])
            width = abs(start_pos[0] - end_pos[0])
            height = abs(start_pos[1] - end_pos[1])
            obstacles.append(Obstacle(x, y, width, height))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            drawing_complete = True

    if drawing_complete:
        # Divide slimes into two threads
        mid_index = len(slimes) // 2
        thread1 = threading.Thread(target=update_slimes, args=(slimes[:mid_index],))
        thread2 = threading.Thread(target=update_slimes, args=(slimes[mid_index:],))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        # Evaporate pheromones
        pheromones *= (1 - EVAPORATION_RATE)

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen

    if drawing:
        end_pos = pygame.mouse.get_pos()
        x = min(start_pos[0], end_pos[0])
        y = min(start_pos[1], end_pos[1])
        width = abs(start_pos[0] - end_pos[0])
        height = abs(start_pos[1] - end_pos[1])
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))

    pheromone_surface = pygame.surfarray.make_surface(np.uint8(pheromones * 255))
    screen.blit(pheromone_surface, (0, 0))

    for obstacle in obstacles:
        obstacle.draw(screen)

    for food_source in food_sources:
        food_source.draw(screen)

    if drawing_complete:
        # Add a blur effect
        raw_str = pygame.image.tostring(screen, 'RGB')
        img = np.frombuffer(raw_str, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        img = cv2.GaussianBlur(img, (5, 5), 0)

        # Increase resolution
        img = cv2.resize(img, (WIDTH * scale_factor, HEIGHT * scale_factor), interpolation=cv2.INTER_LINEAR)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        video_writer.write(img)

    pygame.display.flip()

pygame.quit()
video_writer.release()
