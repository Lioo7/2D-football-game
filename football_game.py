import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2D Football Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Load background image
bg_image_path = os.path.join('images', 'football_pitch.png')  # Path to the background image
try:
    bg_image = pygame.image.load(bg_image_path)
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    pygame.quit()
    exit()

# Player settings
PLAYER_SIZE = 50
PLAYER_A_SPEED = 4
PLAYER_B_SPEED = 4

# Goal settings
GOAL_WIDTH = 100
GOAL_HEIGHT = 200

# Font settings
font = pygame.font.Font(None, 74)

# Initialize player positions
player_a = pygame.Rect(WIDTH // 4 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
player_b = pygame.Rect(3 * WIDTH // 4 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)

# Initialize ball
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = 5 * random.choice((-1, 1))
ball_speed_y = 5 * random.choice((-1, 1))

# Goals
goal_a = pygame.Rect(0, HEIGHT // 2 - GOAL_HEIGHT // 2, 10, GOAL_HEIGHT)
goal_b = pygame.Rect(WIDTH - 10, HEIGHT // 2 - GOAL_HEIGHT // 2, 10, GOAL_HEIGHT)

# Score
score_a = 0
score_b = 0

# Timer
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

# Sound effects
pygame.mixer.init()

# Check if sound files exist
goal_sound_path = os.path.join('sounds', 'goal.wav')
collision_sound_path = os.path.join('sounds', 'collision.wav')
background_music_path = os.path.join('sounds', 'background.wav')

goal_sound = None
collision_sound = None

if os.path.isfile(goal_sound_path):
    goal_sound = pygame.mixer.Sound(goal_sound_path)

if os.path.isfile(collision_sound_path):
    collision_sound = pygame.mixer.Sound(collision_sound_path)
    collision_sound.set_volume(0.1)  # Reduce the collision sound volume

if os.path.isfile(background_music_path):
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.play(-1)

# Game loop
running = True
while running:
    screen.blit(bg_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # User controls for Player A
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_a.left > 0:
        player_a.x -= PLAYER_A_SPEED
    if keys[pygame.K_RIGHT] and player_a.right < WIDTH:
        player_a.x += PLAYER_A_SPEED
    if keys[pygame.K_UP] and player_a.top > 0:
        player_a.y -= PLAYER_A_SPEED
    if keys[pygame.K_DOWN] and player_a.bottom < HEIGHT:
        player_a.y += PLAYER_A_SPEED

    # Movement for Player B (simulated opponent)
    if ball.y < player_b.y:
        player_b.y -= PLAYER_B_SPEED
    elif ball.y > player_b.y + PLAYER_SIZE:
        player_b.y += PLAYER_B_SPEED

    # Clamp Player B to screen edges
    player_b.y = max(0, min(player_b.y, HEIGHT - PLAYER_SIZE))

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        if collision_sound:
            pygame.mixer.Sound.play(collision_sound)

    # Ball collision with left/right walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
        if collision_sound:
            pygame.mixer.Sound.play(collision_sound)

    # Ball collision with players
    if ball.colliderect(player_a):
        ball_speed_x = -ball_speed_x
        ball_speed_y = random.randint(-5, 5)
        if collision_sound:
            pygame.mixer.Sound.play(collision_sound)
    if ball.colliderect(player_b):
        ball_speed_x = -ball_speed_x
        ball_speed_y = random.randint(-5, 5)
        if collision_sound:
            pygame.mixer.Sound.play(collision_sound)

    # Ball collision with goals
    if ball.colliderect(goal_a):
        score_b += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 5 * random.choice((-1, 1))
        ball_speed_y = 5 * random.choice((-1, 1))
        if goal_sound:
            goal_sound.stop()  # Stop the current sound if it exists
            pygame.mixer.Sound.play(goal_sound)
    if ball.colliderect(goal_b):
        score_a += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 5 * random.choice((-1, 1))
        ball_speed_y = 5 * random.choice((-1, 1))
        if goal_sound:
            goal_sound.stop()  # Stop the current sound if it exists
            pygame.mixer.Sound.play(goal_sound)

    # Draw players, ball, and goals
    pygame.draw.rect(screen, RED, player_a)
    pygame.draw.rect(screen, BLUE, player_b)
    pygame.draw.ellipse(screen, BLACK, ball)
    pygame.draw.rect(screen, BLACK, goal_a)
    pygame.draw.rect(screen, BLACK, goal_b)

    # Display score
    score_text = font.render(f"{score_a} - {score_b}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Timer
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    if seconds >= 90:
        running = False
    timer_text = font.render(str(90 - seconds), True, BLACK)
    screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 50))

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

pygame.quit()
