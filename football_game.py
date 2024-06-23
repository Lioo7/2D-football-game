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
PLAYER_A_SPEED = 5
PLAYER_B_SPEED = 3

# Goal settings
GOAL_WIDTH = 100
GOAL_HEIGHT = 200

# Font settings
font = pygame.font.Font(None, 50)

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

# Sound effects (requires 'goal.wav' and 'collision.wav' in 'sounds' directory)
pygame.mixer.init()

goal_sound = None
collision_sound = None

goal_sound_path = os.path.join('sounds', 'goal.wav')
collision_sound_path = os.path.join('sounds', 'collision.wav')
background_music_path = os.path.join('sounds', 'background.wav')

if os.path.isfile(goal_sound_path):
    goal_sound = pygame.mixer.Sound(goal_sound_path)

if os.path.isfile(collision_sound_path):
    collision_sound = pygame.mixer.Sound(collision_sound_path)
    collision_sound.set_volume(0.1)  # Reduce collision sound volume

if os.path.isfile(background_music_path):
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.play(-1)


def handle_player_a_movement(keys, player):
    global PLAYER_A_SPEED, HEIGHT, WIDTH
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= PLAYER_A_SPEED
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += PLAYER_A_SPEED
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PLAYER_A_SPEED
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PLAYER_A_SPEED


def handle_b_movement(ball, player):
    global PLAYER_B_SPEED, HEIGHT
    if ball.y < player.y:
        player.y -= PLAYER_B_SPEED
    elif ball.y > player.y + PLAYER_SIZE:
        player.y += PLAYER_B_SPEED
    player.y = max(0, min(player.y, HEIGHT - PLAYER_SIZE))


def handle_ball_movement(ball, ball_speed_x, ball_speed_y):
    ball.x += ball_speed_x
    ball.y += ball_speed_y


def handle_collisions(ball, ball_speed_x, ball_speed_y, player_a, player_b, goal_a, goal_b):
    global score_a, score_b, collision_sound, goal_sound

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
        reset_ball()
        if goal_sound:
            pygame.mixer.Sound.play(goal_sound)
    if ball.colliderect(goal_b):
        score_a += 1
        reset_ball()
        if goal_sound:
            pygame.mixer.Sound.play(goal_sound)

    # Update global variables
    return ball_speed_x, ball_speed_y


def reset_ball():
    global ball_speed_x, ball_speed_y, ball
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = 5 * random.choice((-1, 1))
    ball_speed_y = 5 * random.choice((-1, 1))


# Game loop
game_over = False
while not game_over:
    screen.blit(bg_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # User controls for Player A
    keys = pygame.key.get_pressed()
    handle_player_a_movement(keys, player_a)

    # Movement for Player B (simulated opponent)
    handle_b_movement(ball, player_b)

    # Ball movement
    handle_ball_movement(ball, ball_speed_x, ball_speed_y)

    # Handle collisions
    ball_speed_x, ball_speed_y = handle_collisions(ball, ball_speed_x, ball_speed_y, player_a, player_b, goal_a, goal_b)

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
        game_over = True

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

# Determine winner
if score_a > score_b:
    winner_text = "Player A wins!"
elif score_b > score_a:
    winner_text = "Player B wins!"
else:
    winner_text = "It's a draw!"

# Display final score and options
final_text = font.render(f"Final Score: {score_a} - {score_b}", True, BLACK)
winner_text_rendered = font.render(winner_text, True, BLACK)

while True:  # Loop for end screen
    screen.blit(bg_image, (0, 0))

    screen.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(winner_text_rendered, (WIDTH // 2 - winner_text_rendered.get_width() // 2, HEIGHT // 2 + 50))

    # Display options: restart or quit
    restart_text = font.render("1. Restart", True, BLACK)
    quit_text = font.render("2. Quit", True, BLACK)

    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 150))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 200))

    pygame.display.flip()

    # Event handling for options
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Restart
                # Reset game state variables
                score_a = 0
                score_b = 0
                start_ticks = pygame.time.get_ticks()
                game_over = False
                reset_ball()
                # Reset player positions if needed
                player_a = pygame.Rect(WIDTH // 4 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
                player_b = pygame.Rect(3 * WIDTH // 4 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
            elif event.key == pygame.K_2:  # Quit
                pygame.quit()
                exit()
