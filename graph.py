import pygame
import heapq
import base64
from io import BytesIO
from flask import Flask, jsonify

# Initialize Pygame in headless mode
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

# Constants and images remain the same as original
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40
# ... [keep all constants and images from original code]

app = Flask(__name__)

class GameState:
    def __init__(self):
        self.current_problem = 0
        self.grid = None
        self.path = []
        self.frames = []
        self.current_step = 0
        self.game_over = False

state = GameState()

def create_problem(problem_num):
    # Same as original create_problem function
    # ...

def setup_grid(problem_num):
    config = create_problem(problem_num)
    n = config['n']
    state.grid = Grid(n, n)
    # ... [rest of grid setup from original code]

def generate_frame():
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
    
    # Convert to base64
    buffer = BytesIO()
    pygame.image.save(surface, buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

@app.route('/api/init')
def initialize():
    setup_grid(state.current_problem)
    return jsonify({'frame': generate_frame(), 'problem': state.current_problem})

@app.route('/api/start')
def start_simulation():
    state.path = dijkstra(state.grid, create_problem(state.current_problem)['start'])
    state.frames = []
    
    # Generate animation frames
    for step in state.path:
        cell = state.grid.get_cell(*step)
        if cell and not cell.is_obstacle:
            # Create frame with player at current step
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface.fill(WHITE)
            
            # Draw grid
            for row in state.grid.grid:
                for c in row:
                    c.draw(surface)
                    pygame.draw.rect(surface, BLACK, (c.x, c.y, CELL_SIZE, CELL_SIZE), 1)
            
            # Draw exit and player at current position
            surface.blit(exit_img, (state.grid.exit.x, state.grid.exit.y))
            surface.blit(player_img, (cell.x, cell.y))
            
            # Convert to base64
            buffer = BytesIO()
            pygame.image.save(surface, buffer, format="PNG")
            state.frames.append(base64.b64encode(buffer.getvalue()).decode('utf-8'))
    
    return jsonify({'frames': state.frames})

@app.route('/api/next')
def next_problem():
    if state.current_problem < 2:
        state.current_problem += 1
        setup_grid(state.current_problem)
    return jsonify({'frame': generate_frame(), 'problem': state.current_problem})

if __name__ == '__main__':
    app.run(port=5000)