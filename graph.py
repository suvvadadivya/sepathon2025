import pygame
import sys
import heapq
import io
from flask import Flask, Response, jsonify, request
from threading import Thread, Lock
import time

app = Flask(__name__)
game_lock = Lock()
current_frame = None
game_state = {
    "current_problem": 0,
    "path": [],
    "game_over": False,
    "running": True,
    "animating": False
}

# Constants from original code
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

# Load and scale images
def load_images():
    global player_img, obstacle_img, exit_img
    player_img = pygame.image.load('player.png')
    obstacle_img = pygame.image.load('obstacle.png')
    exit_img = pygame.image.load('exit.png')
    
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

def run_game():
    global current_frame, game_state
    pygame.init()
    load_images()
    
    screen = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    problems = [create_problem(i) for i in range(3)]
    grid = None
    path = []
    current_step = 0

    def setup_grid(problem):
        nonlocal grid
        config = problems[problem]
        n = config['n']
        grid = Grid(n, n)
        
        grid.start = grid.get_cell(*config['start'])
        grid.exit = grid.get_cell(*config['exit'])
        
        for obstacle in config['obstacles']:
            grid.get_cell(*obstacle).is_obstacle = True
            
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

    setup_grid(0)

    while game_state["running"]:
        with game_lock:
            if game_state["animating"] and current_step < len(game_state["path"]):
                step = game_state["path"][current_step]
                next_cell = grid.get_cell(*step)
                
                if next_cell is None or next_cell.is_obstacle:
                    game_state["game_over"] = True
                    game_state["animating"] = False
                else:
                    screen.fill(WHITE)
                    for row in grid.grid:
                        for cell in row:
                            cell.draw(screen)
                            pygame.draw.rect(screen, BLACK, (cell.x, cell.y, CELL_SIZE, CELL_SIZE), 1)
                    
                    screen.blit(exit_img, (grid.exit.x, grid.exit.y))
                    screen.blit(player_img, (next_cell.x, next_cell.y))
                    current_step += 1
                    
                    if current_step >= len(game_state["path"]):
                        game_state["animating"] = False
            else:
                screen.fill(WHITE)
                for row in grid.grid:
                    for cell in row:
                        cell.draw(screen)
                        pygame.draw.rect(screen, BLACK, (cell.x, cell.y, CELL_SIZE, CELL_SIZE), 1)
                
                screen.blit(player_img, (grid.start.x, grid.start.y))
                screen.blit(exit_img, (grid.exit.x, grid.exit.y))

            img_str = pygame.image.tostring(screen, "RGB")
            current_frame = img_str

        clock.tick(30)

    pygame.quit()

@app.route('/frame')
def get_frame():
    with game_lock:
        if current_frame:
            return Response(current_frame, mimetype='image/rgb')
        return Response(status=204)

@app.route('/start', methods=['POST'])
def start_game():
    with game_lock:
        if not game_state["animating"]:
            config = create_problem(game_state["current_problem"])
            grid = Grid(config['n'], config['n'])
            game_state["path"] = dijkstra(grid, config['start'])
            game_state["animating"] = True
            game_state["game_over"] = False
    return jsonify(success=True)

@app.route('/next', methods=['POST'])
def next_problem():
    with game_lock:
        if game_state["current_problem"] < 2:
            game_state["current_problem"] += 1
            game_state["path"] = []
            game_state["animating"] = False
            game_state["game_over"] = False
    return jsonify(success=True)

@app.route('/state')
def get_state():
    return jsonify(game_state)

if __name__ == '__main__':
    game_thread = Thread(target=run_game)
    game_thread.daemon = True
    game_thread.start()
    app.run(threaded=True, port=5000)