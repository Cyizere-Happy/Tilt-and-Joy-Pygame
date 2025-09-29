import serial
import pygame
import random
import os
import time

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
pygame.mixer.init()

# -----------------------------
# Window setup
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Joystick + MPU6050 Game with Audio")

# -----------------------------
# Character setup
# -----------------------------
CHARACTER_SIZE = 50
CHARACTER_SPEED = 5
JUMP_HEIGHT = 120
GRAVITY = 8
x, y = WIN_WIDTH // 2, WIN_HEIGHT - CHARACTER_SIZE
y_velocity = 0
on_ground = True

# Colors
BODY_COLOR = (0, 150, 255)
EYE_WHITE = (255, 255, 255)
EYE_BLACK = (0, 0, 0)
MOUTH_COLOR = (200, 50, 50)
bg_color = (30, 30, 30)
COIN_COLOR = (255, 215, 0)

# -----------------------------
# Particle effect
# -----------------------------
particles = []
def spawn_particles(px, py, color=(255,255,50)):
    for _ in range(12):
        particles.append({
            'x': px + random.randint(-10,10),
            'y': py + random.randint(-10,10),
            'dx': random.uniform(-3,3),
            'dy': random.uniform(-5,0),
            'size': random.randint(3,6),
            'color': color
        })

def update_particles():
    for p in particles[:]:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['dy'] += 0.3
        p['size'] -= 0.1
        if p['size'] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(win, p['color'], (int(p['x']), int(p['y'])), int(p['size']))

# -----------------------------
# Audio setup
# -----------------------------
jump_sound = pygame.mixer.Sound("jump.wav") if os.path.exists("jump.wav") else None
winning_sound = pygame.mixer.Sound("winning.wav") if os.path.exists("winning.wav") else None
failing_sound = pygame.mixer.Sound("failing.wav") if os.path.exists("failing.wav") else None
collecting_sound = pygame.mixer.Sound("collect.wav") if os.path.exists("collect.wav") else None

# -----------------------------
# Serial setup
# -----------------------------
arduino_serial = serial.Serial('COM11', 9600, timeout=1)

# -----------------------------
# Coins setup
# -----------------------------
coins = []
for _ in range(5):
    coins.append({
        'x': random.randint(50, WIN_WIDTH-50),
        'y': random.randint(50, WIN_HEIGHT-50),
        'radius': 15
    })
score = 0
target_score = 50
font = pygame.font.SysFont(None, 36)

# -----------------------------
# Timer setup
# -----------------------------
TOTAL_TIME = 60
start_time = time.time()
game_over = False
win_game = False

# -----------------------------
# Helper: Draw character
# -----------------------------
def draw_character(surface, x, y):
    pygame.draw.circle(surface, BODY_COLOR, (x, y), CHARACTER_SIZE)
    eye_offset_x = 15
    eye_offset_y = -10
    pygame.draw.circle(surface, EYE_WHITE, (x - eye_offset_x, y + eye_offset_y), 12)
    pygame.draw.circle(surface, EYE_WHITE, (x + eye_offset_x, y + eye_offset_y), 12)
    pygame.draw.circle(surface, EYE_BLACK, (x - eye_offset_x, y + eye_offset_y), 5)
    pygame.draw.circle(surface, EYE_BLACK, (x + eye_offset_x, y + eye_offset_y), 5)
    mouth_rect = pygame.Rect(x - 20, y + 10, 40, 20)
    pygame.draw.arc(surface, MOUTH_COLOR, mouth_rect, 3.14, 0, 3)

# -----------------------------
# Game loop
# -----------------------------
clock = pygame.time.Clock()
running = True
GROUND_Y = WIN_HEIGHT - CHARACTER_SIZE

while running:
    current_bg = bg_color
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, TOTAL_TIME - elapsed_time)

    if remaining_time == 0 and score < target_score and not game_over:
        game_over = True
        if failing_sound:
            failing_sound.play()
    if score >= target_score and not win_game:
        win_game = True
        if winning_sound:
            winning_sound.play()

    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -----------------------------
    # Sensor controls
    # -----------------------------
    if not game_over and not win_game:
        if arduino_serial.in_waiting > 0:
            try:
                line = arduino_serial.readline().decode().strip()
                data = line.split(",")
                if len(data) == 5:
                    joyX, joyY, button, pitch, roll = data
                    joyX, joyY, button = int(joyX), int(joyY), int(button)
                    pitch, roll = float(pitch), float(roll)

                    # Joystick movement
                    if joyX < 400: x -= CHARACTER_SPEED
                    elif joyX > 600: x += CHARACTER_SPEED
                    if joyY < 400: y -= CHARACTER_SPEED
                    elif joyY > 600: y += CHARACTER_SPEED

                    # MPU6050 tilt (scaled)
                    x += int(roll * CHARACTER_SPEED)
                    y += int(pitch * CHARACTER_SPEED)

                    # Jump
                    if button == 0 and on_ground:
                        y_velocity = -JUMP_HEIGHT
                        on_ground = False
                        spawn_particles(x, y)
                        if jump_sound:
                            jump_sound.play()
            except Exception as e:
                print("Serial read error:", e)

    # -----------------------------
    # Gravity and jump
    # -----------------------------
    if not on_ground:
        y += y_velocity * 0.1  # smooth movement
        y_velocity += GRAVITY
        if y >= GROUND_Y:
            y = GROUND_Y
            y_velocity = 0
            on_ground = True

    # -----------------------------
    # Keep character inside window
    # -----------------------------
    x = max(CHARACTER_SIZE, min(WIN_WIDTH - CHARACTER_SIZE, x))
    y = max(CHARACTER_SIZE, min(WIN_HEIGHT - CHARACTER_SIZE, y))

    # -----------------------------
    # Coin collection
    # -----------------------------
    for coin in coins[:]:
        dist = ((x - coin['x'])**2 + (y - coin['y'])**2)**0.5
        if dist < CHARACTER_SIZE + coin['radius']:
            coins.remove(coin)
            score += 10
            spawn_particles(coin['x'], coin['y'], color=(255, 215, 0))
            if collecting_sound:
                collecting_sound.play()
            coins.append({
                'x': random.randint(50, WIN_WIDTH-50),
                'y': random.randint(50, WIN_HEIGHT-50),
                'radius': 15
            })

    # -----------------------------
    # Draw everything
    # -----------------------------
    win.fill(current_bg)
    draw_character(win, x, y)
    for coin in coins:
        pygame.draw.circle(win, COIN_COLOR, (coin['x'], coin['y']), coin['radius'])
    update_particles()

    # Score and timer
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    timer_text = font.render(f"Time: {remaining_time}", True, (255,255,255))
    win.blit(score_text, (10,10))
    win.blit(timer_text, (10,50))

    # Win/lose messages
    if win_game:
        win_text = font.render("YOU WIN!", True, (0,255,0))
        win.blit(win_text, (WIN_WIDTH//2 - 80, WIN_HEIGHT//2 - 20))
    elif game_over:
        lose_text = font.render("GAME OVER!", True, (255,0,0))
        win.blit(lose_text, (WIN_WIDTH//2 - 100, WIN_HEIGHT//2 - 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
