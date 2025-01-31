import pygame
import sys
import random
from time import sleep

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Initialize images with fallback surfaces
try:
    player_img = pygame.image.load('player.png')
    reward_img = pygame.image.load('obstacle.png')
    knapsack_img = pygame.image.load('exit.png')
except pygame.error:
    # Create placeholder surfaces if images not found
    player_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    player_img.fill(BLUE)
    reward_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    reward_img.fill(GREEN)
    knapsack_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    knapsack_img.fill(RED)

# Scale images
player_img = pygame.transform.scale(player_img, (CELL_SIZE, CELL_SIZE))
reward_img = pygame.transform.scale(reward_img, (CELL_SIZE, CELL_SIZE))
knapsack_img = pygame.transform.scale(knapsack_img, (CELL_SIZE, CELL_SIZE))

class Reward:
    def __init__(self, row, col, weight, value):
        self.row = row
        self.col = col
        self.weight = weight
        self.value = value
        self.size = CELL_SIZE + (weight * 5)
        self.image = pygame.transform.scale(reward_img, (self.size, self.size))

    def draw(self, screen):
        screen.blit(self.image, (self.col * CELL_SIZE, self.row * CELL_SIZE))

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.image = player_img
        self.has_knapsack = False
        self.collected_rewards = []

    def draw(self, screen):
        screen.blit(self.image, (self.col * CELL_SIZE, self.row * CELL_SIZE))
        if self.has_knapsack:
            screen.blit(knapsack_img, (self.col * CELL_SIZE, self.row * CELL_SIZE))

def create_problem(problem_num):
    problems = [
        {
            'grid_size': 5,
            'start_pos': (0, 0),
            'exit_pos': (4, 4),
            'rewards': [
                {'pos': (1, 1), 'weight': 2, 'value': 10},
                {'pos': (2, 2), 'weight': 3, 'value': 15},
                {'pos': (3, 3), 'weight': 1, 'value': 7}
            ]
        },
        {
            'grid_size': 6,
            'start_pos': (0, 5),
            'exit_pos': (5, 0),
            'rewards': [
                {'pos': (1, 0), 'weight': 4, 'value': 20},
                {'pos': (2, 1), 'weight': 2, 'value': 10},
                {'pos': (3, 2), 'weight': 3, 'value': 15}
            ]
        },
        {
            'grid_size': 7,
            'start_pos': (3, 3),
            'exit_pos': (6, 6),
            'rewards': [
                {'pos': (0, 0), 'weight': 1, 'value': 5},
                {'pos': (1, 1), 'weight': 2, 'value': 10},
                {'pos': (2, 2), 'weight': 3, 'value': 15}
            ]
        }
    ]
    return problems[problem_num]

def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    
    return selected

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knapsack Problem")
    
    current_problem = 0
    problems = [create_problem(i) for i in range(3)]
    grid = None
    player = None
    rewards = []
    exit_pos = None
    running = True
    game_over = False
    success = False
    
    buttons = {
        'start': pygame.Rect(WIDTH//2 - BUTTON_WIDTH - 10, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT),
        'next': pygame.Rect(WIDTH//2 + 10, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
    }
    
    def setup_problem(problem):
        nonlocal grid, player, rewards, exit_pos
        config = problems[problem]
        grid_size = config['grid_size']
        grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Place player
        player = Player(*config['start_pos'])
        grid[player.row][player.col] = player
        
        # Place exit
        exit_pos = config['exit_pos']
        
        # Place rewards
        rewards = []
        for reward_info in config['rewards']:
            reward = Reward(*reward_info['pos'], reward_info['weight'], reward_info['value'])
            rewards.append(reward)
            grid[reward.row][reward.col] = reward
    
    setup_problem(current_problem)
    
    while running:
        screen.fill(WHITE)
        
        # Draw grid
        if grid:
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    if grid[row][col]:
                        grid[row][col].draw(screen)
                    pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw exit position
        if exit_pos:
            pygame.draw.rect(screen, RED, (exit_pos[1]*CELL_SIZE, exit_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw buttons
        for btn_name, rect in buttons.items():
            pygame.draw.rect(screen, GRAY, rect)
            btn_text = pygame.font.SysFont(None, 30).render(btn_name.capitalize(), True, BLACK)
            screen.blit(btn_text, (rect.x + 25, rect.y + 10))
        
        if game_over:
            game_over_text = pygame.font.SysFont(None, 60).render('GAME OVER', True, RED)
            screen.blit(game_over_text, (WIDTH//2-120, HEIGHT//2-30))
        
        if success:
            success_text = pygame.font.SysFont(None, 60).render('SUCCESS!', True, GREEN)
            screen.blit(success_text, (WIDTH//2-100, HEIGHT//2-30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if buttons['start'].collidepoint(x, y) and not game_over:
                    # Solve Knapsack problem
                    weights = [r.weight for r in rewards]
                    values = [r.value for r in rewards]
                    capacity = 5
                    selected = knapsack(weights, values, capacity)
                    
                    # Animate collection
                    for idx in selected:
                        if idx < len(rewards):
                            reward = rewards[idx]
                            # Clear previous position
                            old_row, old_col = player.row, player.col
                            grid[old_row][old_col] = None
                            
                            # Update player position
                            player.row, player.col = reward.row, reward.col
                            player.collected_rewards.append(reward)
                            grid[player.row][player.col] = player
                            
                            # Update display
                            screen.fill(WHITE)
                            for row in range(len(grid)):
                                for col in range(len(grid[0])):
                                    if grid[row][col]:
                                        grid[row][col].draw(screen)
                                    pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                            pygame.display.flip()
                            sleep(0.5)
                    
                    # Move to exit
                    if exit_pos and player.collected_rewards:
                        old_row, old_col = player.row, player.col
                        grid[old_row][old_col] = None
                        player.row, player.col = exit_pos
                        grid[player.row][player.col] = player
                        success = True
                    
                elif buttons['next'].collidepoint(x, y) and current_problem < len(problems)-1 and not game_over:
                    current_problem += 1
                    setup_problem(current_problem)
                    game_over = False
                    success = False

if __name__ == "__main__":
    main()