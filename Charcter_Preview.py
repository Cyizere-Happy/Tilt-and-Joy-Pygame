import pygame
import sys

# -----------------------------
# Constants
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
CHARACTER_SIZE = 50
BODY_COLOR = (255, 200, 0)      # Yellow
EYE_WHITE = (255, 255, 255)
EYE_BLACK = (0, 0, 0)
MOUTH_COLOR = (255, 0, 0)       # Red

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Character Preview")
clock = pygame.time.Clock()

# -----------------------------
# Character drawing function
# -----------------------------
def draw_character(surface, x, y):
    # Draw body
    pygame.draw.circle(surface, BODY_COLOR, (x, y), CHARACTER_SIZE)

    # Eyes
    eye_offset_x = 15
    eye_offset_y = -10
    pygame.draw.circle(surface, EYE_WHITE, (x - eye_offset_x, y + eye_offset_y), 12)
    pygame.draw.circle(surface, EYE_WHITE, (x + eye_offset_x, y + eye_offset_y), 12)
    pygame.draw.circle(surface, EYE_BLACK, (x - eye_offset_x, y + eye_offset_y), 5)
    pygame.draw.circle(surface, EYE_BLACK, (x + eye_offset_x, y + eye_offset_y), 5)

    # Mouth (arc)
    mouth_rect = pygame.Rect(x - 20, y + 10, 40, 20)
    pygame.draw.arc(surface, MOUTH_COLOR, mouth_rect, 3.14, 0, 3)

# -----------------------------
# Main loop
# -----------------------------
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2

running = True
while running:
    win.fill((0, 0, 50))  # Dark blue background

    draw_character(win, x, y)

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
