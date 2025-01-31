import pygame
import sys
import heapq
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

# Load images
player_img = pygame.image.load('player.png')  # Replace with actual image path
obstacle_img = pygame.image.load('obstacle.png')  # Replace with actual image path
exit_img = pygame.image.load('exit.png')  # Replace with actual image path

# Scale images
player_img = pygame.transform.scale(player_img, (CELL_SIZE, CELL_SIZE))
obstacle_img = pygame.transform.scale(obstacle_img, (CELL_SIZE, CELL_SIZE))
exit_img = pygame.transform.scale(exit_img, (CELL_SIZE, CELL_SIZE))

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.is_obstacle = False
        self.neighbors = []
        self.previous = None
        self.distance = float('inf')

    def draw(self, screen):
        if self.is_obstacle:
            screen.blit(obstacle_img, (self.x, self.y))

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.start = None
        self.exit = None

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def reset(self):
        for row in self.grid:
            for cell in row:
                cell.distance = float('inf')
                cell.previous = None

def create_problem(problem_num):
    problems = [
        {
            'n': 5,
            'start': (0, 0),
            'exit': (4, 4),
            'obstacles': [(1, 1), (2, 2), (3, 3)]
        },
        {
            'n': 6,
            'start': (0, 5),
            'exit': (5, 0),
            'obstacles': [(1, 0), (2, 1), (3, 2), (4, 3)]
        },
        {
            'n': 7,
            'start': (3, 3),
            'exit': (6, 6),
            'obstacles': [(0, 0), (1, 1), (2, 2), (4, 4), (5, 5)]
        }
    ]
    return problems[problem_num]

def dijkstra(grid, start, result=True):
    grid.reset()
    start_cell = grid.get_cell(*start)
    start_cell.distance = 0
    queue = [(0, start_cell.row, start_cell.col)]
    
    while queue:
        current_dist, row, col = heapq.heappop(queue)
        current_cell = grid.get_cell(row, col)
        
        if current_cell == grid.exit:
            break
            
        for neighbor in current_cell.neighbors:
            if neighbor.is_obstacle:
                continue
            new_dist = current_dist + 1
            if new_dist < neighbor.distance:
                neighbor.distance = new_dist
                neighbor.previous = current_cell
                heapq.heappush(queue, (new_dist, neighbor.row, neighbor.col))
    
    path = []
    current = grid.exit
    while current:
        path.insert(0, (current.row, current.col))
        current = current.previous
    return path if grid.exit.distance != float('inf') else []

def main(result=True):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dijkstra's Pathfinding")
    
    current_problem = 0
    problems = [create_problem(i) for i in range(3)]
    grid = None
    path = []
    running = True
    game_over = False
    
    start_button = pygame.Rect(
        WIDTH//2 - BUTTON_WIDTH - 10, 
        HEIGHT - BUTTON_HEIGHT - 10, 
        BUTTON_WIDTH, 
        BUTTON_HEIGHT
    )
    next_button = pygame.Rect(
        WIDTH//2 + 10, 
        HEIGHT - BUTTON_HEIGHT - 10, 
        BUTTON_WIDTH, 
        BUTTON_HEIGHT
    )
    
    def setup_grid(problem):
        nonlocal grid
        config = problems[problem]
        n = config['n']
        grid = Grid(n, n)
        
        # Set start and exit
        grid.start = grid.get_cell(*config['start'])
        grid.exit = grid.get_cell(*config['exit'])
        
        # Set obstacles
        for obstacle in config['obstacles']:
            grid.get_cell(*obstacle).is_obstacle = True
            
        # Create neighbors
        for row in grid.grid:
            for cell in row:
                cell.neighbors = []
                if cell.row > 0:
                    neighbor = grid.get_cell(cell.row-1, cell.col)
                    if neighbor:
                        cell.neighbors.append(neighbor)
                if cell.row < grid.rows-1:
                    neighbor = grid.get_cell(cell.row+1, cell.col)
                    if neighbor:
                        cell.neighbors.append(neighbor)
                if cell.col > 0:
                    neighbor = grid.get_cell(cell.row, cell.col-1)
                    if neighbor:
                        cell.neighbors.append(neighbor)
                if cell.col < grid.cols-1:
                    neighbor = grid.get_cell(cell.row, cell.col+1)
                    if neighbor:
                        cell.neighbors.append(neighbor)
    
    setup_grid(current_problem)
    
    while running:
        screen.fill(WHITE)
        
        # Draw grid
        for row in grid.grid:
            for cell in row:
                cell.draw(screen)
                pygame.draw.rect(screen, BLACK, (cell.x, cell.y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw start and exit
        screen.blit(player_img, (grid.start.x, grid.start.y))
        screen.blit(exit_img, (grid.exit.x, grid.exit.y))
        
        # Draw buttons
        pygame.draw.rect(screen, GRAY, start_button)
        start_text = pygame.font.SysFont(None, 30).render('Start', True, BLACK)
        screen.blit(start_text, (start_button.x+25, start_button.y+10))
        
        next_disabled = current_problem >= len(problems)-1
        btn_color = GRAY if next_disabled else GRAY
        pygame.draw.rect(screen, btn_color, next_button)
        next_text = pygame.font.SysFont(None, 30).render('Next', True, BLACK)
        screen.blit(next_text, (next_button.x+25, next_button.y+10))
        
        if game_over:
            game_over_text = pygame.font.SysFont(None, 60).render('GAME OVER', True, RED)
            screen.blit(game_over_text, (WIDTH//2-120, HEIGHT//2-30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button.collidepoint(x, y) and not game_over:
                    path = dijkstra(grid, problems[current_problem]['start'], result)
                    if not result and path:
                        path.append((path[-1][0]+1, path[-1][1]+1))  # Force invalid path
                    
                    # Animate movement
                    current_pos = grid.start
                    for step in path:
                        next_cell = grid.get_cell(*step)
                        if next_cell is None or next_cell.is_obstacle:
                            game_over = True
                            break
                        
                        # Update display
                        screen.fill(WHITE)
                        for r in grid.grid:
                            for cell in r:
                                cell.draw(screen)
                                pygame.draw.rect(screen, BLACK, (cell.x, cell.y, CELL_SIZE, CELL_SIZE), 1)
                        
                        screen.blit(exit_img, (grid.exit.x, grid.exit.y))
                        screen.blit(player_img, (next_cell.x, next_cell.y))
                        pygame.display.flip()
                        sleep(0.5)
                        current_pos = next_cell
                
                elif next_button.collidepoint(x, y) and not next_disabled and not game_over:
                    current_problem += 1
                    setup_grid(current_problem)
                    game_over = False

if __name__ == "__main__":
    result_param = True  # Set this to False for game over scenario
    main(result_param)