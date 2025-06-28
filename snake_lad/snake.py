import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
FONT_SIZE = 30
DICE_SIZE = 100  # Define the size of the dice display area

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake and Ladder")

# Font setup
font = pygame.font.SysFont(None, FONT_SIZE)

# Snakes and Ladders positions
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Function to convert board position to coordinates
def position_to_coordinates(position):
    row = (position - 1) // COLS
    col = (position - 1) % COLS
    if row % 2 == 1:  # Odd row: left to right
        col = COLS - col - 1
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2
    return x, y

# Function to draw the game board
def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)
            
            # Calculate position number based on the current row and column
            if row % 2 == 0:  # Odd row (left to right)
                pos = (ROWS - row) * COLS - col
            else:  # Even row (right to left)
                pos = (ROWS - row) * COLS - (COLS - col - 1)
                
            text = font.render(str(pos), True, BLACK)
            screen.blit(text, (x + 5, y + 5))

    # Draw ladders
    for start, end in ladders.items():
        start_x, start_y = position_to_coordinates(start)
        end_x, end_y = position_to_coordinates(end)
        pygame.draw.line(screen, GREEN, (start_x, start_y), (end_x, end_y), 5)

    # Draw snakes
    for start, end in snakes.items():
        start_x, start_y = position_to_coordinates(start)
        end_x, end_y = position_to_coordinates(end)
        pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), 5)

# Function to draw the players
def draw_player(position, player_color):
    x, y = position_to_coordinates(position)
    pygame.draw.circle(screen, player_color, (x, y), SQUARE_SIZE // 4)

# Function to roll the dice
def roll_dice():
    return random.randint(1, 6)

# Function to move the player
def move_player(position, dice_roll):
    position += dice_roll
    if position > 100:
        position = 100
    if position in snakes:
        position = snakes[position]
    elif position in ladders:
        position = ladders[position]
    return position

# Function to display the scoreboard
def draw_scoreboard(player_positions, current_player, dice_roll):
    scoreboard_y = HEIGHT - FONT_SIZE * (len(player_positions) + 2)
    screen.fill(WHITE, (0, scoreboard_y, WIDTH, HEIGHT - scoreboard_y))
    
    for i, position in enumerate(player_positions):
        score_text = font.render(f"Player {i + 1}: {position}", True, RED if i == current_player else BLUE)
        screen.blit(score_text, (10, scoreboard_y + i * FONT_SIZE))
    
    dice_text = font.render(f"Dice: {dice_roll}", True, BLACK)
    screen.blit(dice_text, (WIDTH - DICE_SIZE + 10, scoreboard_y + FONT_SIZE))

# Main game loop
def play_game(num_players):
    player_positions = [0] * num_players
    player_colors = [RED, BLUE, GREEN, PURPLE][:num_players]  # Adjust colors based on number of players
    current_player = 0
    dice_roll = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice_roll = roll_dice()
                    player_positions[current_player] = move_player(player_positions[current_player], dice_roll)
                    print(f"Player {current_player + 1} - Dice roll: {dice_roll}, Position: {player_positions[current_player]}")
                    
                    if player_positions[current_player] == 100:
                        print(f"\nCongratulations! Player {current_player + 1} wins the game!")
                        running = False
                        break

                    current_player = (current_player + 1) % num_players

        draw_board()
        for i in range(num_players):
            draw_player(player_positions[i], player_colors[i])
        
        draw_scoreboard(player_positions, current_player, dice_roll)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    num_players = int(input("Enter the number of players (up to 4 for this example): "))
    play_game(num_players)
