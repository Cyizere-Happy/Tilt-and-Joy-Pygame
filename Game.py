import serial
import pygame

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# -----------------------------
# Window setup
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Joystick + MPU6050 Control")

# -----------------------------
# Character setup
# -----------------------------
CHARACTER_SIZE = 50
CHARACTER_SPEED = 5
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2

# Character colors
BODY_COLOR = (0, 150, 255)   # Blue body
EYE_WHITE = (255, 255, 255)
EYE_BLACK = (0, 0, 0)
MOUTH_COLOR = (200, 50, 50)

# -----------------------------
# Serial setup (adjust COM port if needed)
# -----------------------------
arduino_serial = serial.Serial('COM5', 9600, timeout=1)

# -----------------------------
# Helper: Draw character
# -----------------------------
def draw_character(surface, x, y):
    # Draw body (circle)
    pygame.draw.circle(surface, BODY_COLOR, (x, y), CHARACTER_SIZE)

    # Eyes
    eye_offset_x = 15
    eye_offset_y = -10
    pygame.draw.circle(surface, EYE_WHITE, (x - eye_offset_x, y + eye_offset_y), 12)
    pygame.draw.circle(surface, EYE_WHITE, (x + eye_offset_x, y + eye_offset_y), 12)
    pygame.draw.circle(surface, EYE_BLACK, (x - eye_offset_x, y + eye_offset_y), 5)
    pygame.draw.circle(surface, EYE_BLACK, (x + eye_offset_x, y + eye_offset_y), 5)

    # Mouth (arc-like line)
    mouth_rect = pygame.Rect(x - 20, y + 10, 40, 20)
    pygame.draw.arc(surface, MOUTH_COLOR, mouth_rect, 3.14, 0, 3)

# -----------------------------
# Game loop setup
# -----------------------------
clock = pygame.time.Clock()
running = True

while running:
    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick + MPU6050 data from Arduino
    if arduino_serial.in_waiting > 0:
        try:
            line = arduino_serial.readline().decode().strip()
            print("Raw Data:", line)  # Debugging
            data = line.split(",")
            
            if len(data) == 5:
                # Unpack data
                xValue, yValue, button, pitch, roll = data
                xValue, yValue, button = int(xValue), int(yValue), int(button)
                pitch, roll = float(pitch), float(roll)

                # --- Joystick movement ---
                if xValue < 400:
                    x -= CHARACTER_SPEED
                elif xValue > 600:
                    x += CHARACTER_SPEED

                if yValue < 400:
                    y -= CHARACTER_SPEED
                elif yValue > 600:
                    y += CHARACTER_SPEED

                # --- MPU6050 tilt movement ---
                if pitch < 0.0:      # tilt forward
                    y -= CHARACTER_SPEED
                elif pitch > 0.9:    # tilt backward
                    y += CHARACTER_SPEED

                if roll > 0.6:       # tilt right
                    x += CHARACTER_SPEED
                elif roll < 0.0:     # tilt left
                    x -= CHARACTER_SPEED

                # --- Button action ---
                if button == 0:  # pressed (LOW active)
                    print("Button pressed! (fire/jump)")

        except Exception as e:
            print("Error:", e)

    # Keep character inside window bounds
    x = max(CHARACTER_SIZE, min(WIN_WIDTH - CHARACTER_SIZE, x))
    y = max(CHARACTER_SIZE, min(WIN_HEIGHT - CHARACTER_SIZE, y))

    # Draw everything
    win.fill((30, 30, 30))  # Dark background
    draw_character(win, x, y)
    pygame.display.flip()

    # Control frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
