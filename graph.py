import pygame
import heapq
import base64
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS  # Install with pip install flask-cors

# Initialize Pygame in headless mode
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Load images (replace with actual paths)
try:
    player_img = pygame.image.load('player.png')
    obstacle_img = pygame.image.load('obstacle.png')
    exit_img = pygame.image.load('exit.png')
except FileNotFoundError:
    # Fallback to colored rectangles if images missing
    player_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    player_img.fill(BLUE)
    obstacle_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    obstacle_img.fill(RED)
    exit_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    exit_img.fill(GREEN)

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

def dijkstra(grid, start):
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

app = Flask(__name__)
CORS(app)

class GameState:
    def __init__(self):
        self.current_problem = 0
        self.grid = None
        self.path = []
        self.frames = []
        self.game_over = False

state = GameState()

def setup_grid(problem_num):
    config = create_problem(problem_num)
    n = config['n']
    state.grid = Grid(n, n)
    
    # Set start and exit
    state.grid.start = state.grid.get_cell(*config['start'])
    state.grid.exit = state.grid.get_cell(*config['exit'])
    
    # Set obstacles
    for obstacle in config['obstacles']:
        state.grid.get_cell(*obstacle).is_obstacle = True
        
    # Create neighbors
    for row in state.grid.grid:
        for cell in row:
            cell.neighbors = []
            if cell.row > 0:
                neighbor = state.grid.get_cell(cell.row-1, cell.col)
                if neighbor:
                    cell.neighbors.append(neighbor)
            if cell.row < state.grid.rows-1:
                neighbor = state.grid.get_cell(cell.row+1, cell.col)
                if neighbor:
                    cell.neighbors.append(neighbor)
            if cell.col > 0:
                neighbor = state.grid.get_cell(cell.row, cell.col-1)
                if neighbor:
                    cell.neighbors.append(neighbor)
            if cell.col < state.grid.cols-1:
                neighbor = state.grid.get_cell(cell.row, cell.col+1)
                if neighbor:
                    cell.neighbors.append(neighbor)

def generate_frame(highlight=None):
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(WHITE)
    
    # Draw grid
    for row in state.grid.grid:
        for cell in row:
            cell.draw(surface)
            pygame.draw.rect(surface, BLACK, (cell.x, cell.y, CELL_SIZE, CELL_SIZE), 1)
    
    # Draw start and exit
    if state.grid.start:
        surface.blit(player_img, (state.grid.start.x, state.grid.start.y))
    if state.grid.exit:
        surface.blit(exit_img, (state.grid.exit.x, state.grid.exit.y))
    
    # Highlight current path step
    if highlight:
        cell = state.grid.get_cell(*highlight)
        if cell:
            pygame.draw.rect(surface, BLUE, (cell.x, cell.y, CELL_SIZE, CELL_SIZE), 3)
    
    # Convert to base64
    buffer = BytesIO()
    pygame.image.save(surface, buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

@app.route('/api/init')
def initialize():
    setup_grid(state.current_problem)
    return jsonify({
        'frame': generate_frame(),
        'problem': state.current_problem,
        'total_problems': len(create_problem(0))  # Update if you add more problems
    })

@app.route('/api/start')
def start_simulation():
    state.path = dijkstra(state.grid, create_problem(state.current_problem)['start'])
    state.frames = []
    
    # Generate initial state
    state.frames.append(generate_frame())
    
    # Generate animation frames
    for step in state.path:
        state.frames.append(generate_frame(step))
    
    # Add final state
    state.frames.append(generate_frame())
    
    return jsonify({
        'frames': state.frames,
        'path_length': len(state.path) if state.path else 0,
        'success': bool(state.path)
    })

@app.route('/api/next')
def next_problem():
    if state.current_problem < 2:
        state.current_problem += 1
        setup_grid(state.current_problem)
    return jsonify({
        'frame': generate_frame(),
        'problem': state.current_problem
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)