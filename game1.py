import pygame
import base64
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS
import os

# Initialize Pygame in headless mode
# os.environ['SDL_VIDEODRIVER'] = 'dummy'
# pygame.init()

# Constants
WIDTH = 800
HEIGHT = 200
TREE_SPACING = 80
TREE_WIDTH = 60
TREE_HEIGHT = 80
FONT_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (150, 150, 150)

# Problem data
TREE_VALUES = [1, -2, 3, 4, -1, 2, 1, -5, 4]
SOLUTION_INDICES = [2, 3, 4, 5, 6]

app = Flask(__name__)
CORS(app)

class TreeVisualizer:
    def __init__(self):
        self.current_frame = 0
        self.frames = []
        self.solution_shown = False
        
        # Load images or create fallback
        try:
            self.tree_img = pygame.image.load('tree.png')
            self.marked_tree_img = pygame.image.load('marked_tree.png')
        except FileNotFoundError:
            self.tree_img = pygame.Surface((TREE_WIDTH, TREE_HEIGHT))
            self.tree_img.fill(GREEN)
            self.marked_tree_img = pygame.Surface((TREE_WIDTH, TREE_HEIGHT))
            self.marked_tree_img.fill(RED)
            
        self.tree_img = pygame.transform.scale(self.tree_img, (TREE_WIDTH, TREE_HEIGHT))
        self.marked_tree_img = pygame.transform.scale(self.marked_tree_img, (TREE_WIDTH, TREE_HEIGHT))
        
        self.font = pygame.font.Font(None, FONT_SIZE)

    def generate_base_frame(self):
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(WHITE)
        
        # Calculate starting position for centering
        total_width = len(TREE_VALUES) * TREE_SPACING
        start_x = (WIDTH - total_width) // 2
        
        # Draw all trees
        for i, value in enumerate(TREE_VALUES):
            x = start_x + i * TREE_SPACING
            y = (HEIGHT - TREE_HEIGHT) // 2
            surface.blit(self.tree_img, (x, y))
            
            # Draw value
            text = self.font.render(str(value), True, BLACK)
            text_rect = text.get_rect(center=(x + TREE_WIDTH//2, y + TREE_HEIGHT + 20))
            surface.blit(text, text_rect)
            
        return surface

    def generate_solution_frames(self):
        base_surface = self.generate_base_frame()
        frames = []
        
        # Generate animation frames
        for i in range(len(SOLUTION_INDICES) + 1):
            frame = base_surface.copy()
            
            # Mark trees up to current step
            for idx in SOLUTION_INDICES[:i]:
                if 0 <= idx < len(TREE_VALUES):
                    # Calculate position
                    start_x = (WIDTH - len(TREE_VALUES) * TREE_SPACING) // 2
                    x = start_x + idx * TREE_SPACING
                    y = (HEIGHT - TREE_HEIGHT) // 2
                    
                    # Draw marked tree
                    frame.blit(self.marked_tree_img, (x, y))
                    
                    # Redraw value on top
                    text = self.font.render(str(TREE_VALUES[idx]), True, BLACK)
                    text_rect = text.get_rect(center=(x + TREE_WIDTH//2, y + TREE_HEIGHT + 20))
                    frame.blit(text, text_rect)
            
            # Convert to base64
            buffer = BytesIO()
            pygame.image.save(frame, buffer, format="PNG")
            frames.append(base64.b64encode(buffer.getvalue()).decode('utf-8'))
        
        return frames

tree_visualizer = TreeVisualizer()

@app.route('/api/init')
def initialize():
    frame = tree_visualizer.generate_base_frame()
    buffer = BytesIO()
    pygame.image.save(frame, buffer, format="PNG")
    return jsonify({
        'frame': base64.b64encode(buffer.getvalue()).decode('utf-8'),
        'totalTrees': len(TREE_VALUES)
    })

@app.route('/api/solve')
def show_solution():
    if not tree_visualizer.solution_shown:
        tree_visualizer.frames = tree_visualizer.generate_solution_frames()
        tree_visualizer.current_frame = 0
        tree_visualizer.solution_shown = True
    
    return jsonify({
        'frames': tree_visualizer.frames,
        'solution': SOLUTION_INDICES
    })

if __name__ == '__main__':
    app.run(port=5000)