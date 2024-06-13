import pygame
import time
import random

# Define colors using RGB tuples
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Define directions as constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Initialize pygame
pygame.init()

# Set screen dimensions
GAME_WIDTH = 400
GAME_HEIGHT = 400
SIDEBAR_WIDTH = 100
SCREEN_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT

# Set block size for the snake and food
BLOCK_SIZE = 20

# Set fonts for various texts
title_font = pygame.font.SysFont("Bungee Inline", 40)
option_font = pygame.font.SysFont("Bungee Inline", 18)
level_font = pygame.font.SysFont("Bungee Inline", 18)
game_over_font = pygame.font.SysFont("Bungee Inline", 30)
score_font = pygame.font.SysFont("Bungee Inline", 26)
play_again_font = pygame.font.SysFont("Bungee Inline", 24)
sidebar_font = pygame.font.SysFont("Bungee Inline", 14)
sidebar_font_bold = pygame.font.SysFont("Bungee Inline", 14)
timer_font = pygame.font.SysFont("Bungee Inline", 100)

# Set up the display
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Python Snake Game')

# Clock for controlling game speed
clock = pygame.time.Clock()

# Define Snake class
class Snake:
    def __init__(self, initial_length):
        # Initialize snake attributes
        self.length = initial_length
        self.positions = [(GAME_WIDTH // 2, GAME_HEIGHT // 2)] * initial_length
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        """Get the position of the snake's head"""
        return self.positions[0]

    def move(self):
        """Move the snake and check for collisions"""
        cur = self.get_head_position()
        x, y = self.direction_move[self.direction]
        new = (((cur[0] + (x * BLOCK_SIZE))), (cur[1] + (y * BLOCK_SIZE)))

        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  # Collision with itself
        elif new[0] < 0 or new[0] >= GAME_WIDTH or new[1] < 0 or new[1] >= GAME_HEIGHT:
            return True  # Collision with border
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return False

    def reset(self, initial_length):
        """Reset the snake to its initial state"""
        self.length = initial_length
        self.positions = [(GAME_WIDTH // 2, GAME_HEIGHT // 2)] * initial_length
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        """Draw the snake on the surface"""
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, self.color, r, border_radius=5)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        """Handle key events to change the snake's direction"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    # Dictionary mapping directions to movement vectors
    direction_move = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0)
    }

# Define Food class
class Food:
    def __init__(self):
        """Initialize food attributes"""
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Randomize food position while avoiding collision with snake"""
        while True:
            new_position = (random.randint(0, (GAME_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                            random.randint(0, (GAME_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self, surface):
        """Draw the food on the surface"""
        r = pygame.Rect((self.position[0], self.position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, r, border_radius=5)
        pygame.draw.rect(surface, BLACK, r, 1)

# Define Obstacle class
class Obstacle:
    def __init__(self):
        """Initialize obstacle attributes"""
        self.position = (0, 0)
        self.color = (255, 165, 0)  # Orange
        self.randomize_position()

    def randomize_position(self):
        """Randomize obstacle position"""
        self.position = (random.randint(0, (GAME_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, (GAME_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

    def draw(self, surface):
        """Draw the obstacle on the surface as a hexagon"""
        x, y = self.position
        points = [
            (x + BLOCK_SIZE // 2, y),
            (x + BLOCK_SIZE, y + BLOCK_SIZE // 4),
            (x + BLOCK_SIZE, y + 3 * BLOCK_SIZE // 4),
            (x + BLOCK_SIZE // 2, y + BLOCK_SIZE),
            (x, y + 3 * BLOCK_SIZE // 4),
            (x, y + BLOCK_SIZE // 4)
        ]
        pygame.draw.polygon(surface, self.color, points)
        pygame.draw.polygon(surface, BLACK, points, 1)  # Outline

# Function to draw score, level, and speed in the sidebar
def draw_score(score):
    """Draw score, level, and speed in the sidebar"""
    score_text = sidebar_font_bold.render(f"SCORE: {score}", True, YELLOW)
    display.blit(score_text, [GAME_WIDTH + 10, 10])

    level_text = sidebar_font_bold.render(f"LEVEL: {score // 5}", True, YELLOW)
    display.blit(level_text, [GAME_WIDTH + 10, 10 + score_text.get_height() + 20])

    speed_text = sidebar_font_bold.render(f"SPEED: {SPEED}", True, YELLOW)
    display.blit(speed_text, [GAME_WIDTH + 10, 10 + (score_text.get_height() + 20) * 2])

# Function to draw the sidebar with borders
def draw_sidebar():
    """Draw the sidebar with borders"""
    pygame.draw.rect(display, WHITE, (-3, -3, GAME_WIDTH + 6, GAME_HEIGHT + 6), 3)
    pygame.draw.rect(display, BLACK, (GAME_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(display, WHITE, (GAME_WIDTH + 3, -3, SIDEBAR_WIDTH - 6, SCREEN_HEIGHT + 6), 3)

# Function to display the start screen
def start_screen():
    """Display the start screen with game name and level options"""
    display.fill(BLACK)
    title_text = title_font.render("PYTHON SNAKE", True, GREEN)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    option_text = level_font.render("CHOOSE LEVEL:", True, RED)
    option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))

    slug_text = level_font.render("SLUG", True, WHITE)
    slug_rect = slug_text.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

    worm_text = level_font.render("WORM", True, WHITE)
    worm_rect = worm_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    python_text = level_font.render("PYTHON", True, WHITE)
    python_rect = python_text.get_rect(center=(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

    display.blit(title_text, title_rect)
    display.blit(option_text, option_rect)
    display.blit(slug_text, slug_rect)
    display.blit(worm_text, worm_rect)
    display.blit(python_text, python_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if slug_rect.collidepoint(x, y):
                    return 1, 3, 0
                elif worm_rect.collidepoint(x, y):
                    return 3, 4, 5
                elif python_rect.collidepoint(x, y):
                    return 5, 5, 10

# Function to display countdown timer
def display_timer():
    """Display a 3-second countdown timer"""
    for i in range(3, 0, -1):
        display.fill(BLACK)
        timer_text = timer_font.render(str(i), True, WHITE)
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        display.blit(timer_text, timer_rect)
        pygame.display.update()
        pygame.time.delay(1000)

# Main function
def main():
    global SPEED  # Declare SPEED as a global variable
    initial_length, SPEED, initial_obstacles = start_screen()  # Show the start screen and get initial settings
    snake = Snake(initial_length)
    food = Food()
    obstacles = [Obstacle() for _ in range(initial_obstacles)]
    game_over = False
    win = False
    score = 0
    level = 1  # Initialize the level variable
    last_obstacle_score = 0

    # Display countdown timer
    display_timer()

    while not game_over:
        display.fill(BLACK)

        # Draw the sidebar and borders
        draw_sidebar()

        # Event handling
        snake.handle_keys()
        game_over = snake.move()

        # Snake eating food
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position(snake.positions + [obstacle.position for obstacle in obstacles])

        # Check if an obstacle should appear
        if score >= 10 and (score - 10) % 5 == 0 and score != last_obstacle_score:
            obstacle = Obstacle()
            while obstacle.position in snake.positions or obstacle.position == food.position:
                obstacle.randomize_position()
            obstacles.append(obstacle)
            last_obstacle_score = score

        # Check for collision with obstacles
        for obstacle in obstacles:
            if snake.get_head_position() == obstacle.position:
                game_over = True

        # Level up and increase speed
        new_level = score // 5 + 1
        if new_level > level:
            level = new_level
            SPEED += 0.5  # Increase speed by 0.5 for each new level

        # Draw snake, food, and obstacles
        snake.draw(display)
        food.draw(display)
        for obstacle in obstacles:
            obstacle.draw(display)

        # Draw score in the sidebar
        draw_score(score)

        # Update display
        pygame.display.update()

        # Control game speed
        clock.tick(SPEED)

    # Display "Game Over" or "You Win"
    display.fill(BLACK)

    # Font styles for different text
    spacing = game_over_font.get_height() + 20

    if win:
        game_over_text = game_over_font.render("YOU WIN!", True, GREEN)
    else:
        game_over_text = game_over_font.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - spacing))
    display.blit(game_over_text, game_over_rect)

    score_text = score_font.render(f"Final Score: {score}", True, GREEN)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    display.blit(score_text, score_rect)

    play_again_text = play_again_font.render("Press SPACE to Play Again", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + spacing))
    display.blit(play_again_text, play_again_rect)

    pygame.display.update()

    # Wait for spacebar to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

# Execute main function
if __name__ == "__main__":
    main()