import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 3
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

# Load Assets
bird_img = pygame.image.load("bird.png")  # Use a small bird image or replace with pygame.Rect
bird_img = pygame.transform.scale(bird_img, (40, 30))

# Bird Class
class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = BIRD_Y
        self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))  # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))  # Bottom pipe

    def collide(self, bird):
        if bird.x + 40 > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.height or bird.y + 30 > self.height + PIPE_GAP:
                return True
        return False

# Game Loop
def main():
    bird = Bird()
    pipes = [Pipe(WIDTH + i * 250) for i in range(3)]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.move()
        bird.draw()

        # Pipe Logic
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.collide(bird):
                print("Game Over! Score:", score)
                running = False
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
                print("Score:", score)

        # Remove old pipes & add new ones
        if pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)
            pipes.append(Pipe(WIDTH))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

# Run the Game
main()
