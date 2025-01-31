# server.py
import pygame
import base64
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS
import os

# Pygame headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
pygame.font.init()

# Constants and classes remain similar to original code
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
GRAY = (150, 150, 150)

app = Flask(__name__)
CORS(app)

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

class Animator:
    def __init__(self):
        self.example_arrays = [
            [1, 2, 3, 4, 5, 6, 7],
            [4, 10, 15, 20, 25, 30, 35],
            [5, 15, 25, 35, 45, 55, 65]
        ]
        self.current_example = 0
        self.font = pygame.font.SysFont('freesansbold', 30)
        self.leaf_image = self._create_leaf_image()
        
    def _create_leaf_image(self):
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(surf, GREEN, (25, 25), 20)
        pygame.draw.circle(surf, BLACK, (25, 25), 20, 2)
        return surf

    def _draw_tree(self, surface, node):
        if node:
            if node.left:
                pygame.draw.line(surface, BLACK, (node.x, node.y), (node.left.x, node.left.y), 2)
            if node.right:
                pygame.draw.line(surface, BLACK, (node.x, node.y), (node.right.x, node.right.y), 2)
            surface.blit(self.leaf_image, (node.x - 25, node.y - 25))
            text = self.font.render(str(node.val), True, BLACK)
            surface.blit(text, (node.x - 10, node.y - 10))

    def _assign_positions(self, node, x, y, x_offset):
        if node:
            node.x, node.y = x, y
            self._assign_positions(node.left, x - x_offset, y + 60, x_offset // 2)
            self._assign_positions(node.right, x + x_offset, y + 60, x_offset // 2)

    def _sorted_array_to_bst(self, arr):
        if not arr:
            return None
        mid = len(arr) // 2
        root = TreeNode(arr[mid])
        root.left = self._sorted_array_to_bst(arr[:mid])
        root.right = self._sorted_array_to_bst(arr[mid + 1:])
        return root

    def generate_animation_frames(self):
        sorted_arr = sorted(self.example_arrays[self.current_example])
        root = self._sorted_array_to_bst(sorted_arr)
        self._assign_positions(root, WIDTH//2, 50, 200)
        
        frames = []
        queue = [root]
        while queue:
            level_size = len(queue)
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface.fill(WHITE)
            
            # Draw all nodes processed so far
            for node in queue:
                if node:
                    self._draw_tree(surface, node)
            
            # Convert to base64
            buffer = BytesIO()
            pygame.image.save(surface, buffer, format="PNG")
            frames.append(base64.b64encode(buffer.getvalue()).decode('utf-8'))
            
            # Expand queue
            next_level = []
            for node in queue:
                if node:
                    next_level.append(node.left)
                    next_level.append(node.right)
            queue = next_level if any(next_level) else []
        
        return frames

animator = Animator()

@app.route('/api/init')
def initialize():
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(WHITE)
    animator._assign_positions(
        animator._sorted_array_to_bst(sorted(animator.example_arrays[0])), 
        WIDTH//2, 50, 200
    )
    animator._draw_tree(surface, animator._sorted_array_to_bst(sorted(animator.example_arrays[0])))
    
    buffer = BytesIO()
    pygame.image.save(surface, buffer, format="PNG")
    return jsonify({
        'frame': base64.b64encode(buffer.getvalue()).decode('utf-8'),
        'totalExamples': len(animator.example_arrays)
    })

@app.route('/api/start')
def start_animation():
    frames = animator.generate_animation_frames()
    return jsonify({'frames': frames})

@app.route('/api/next')
def next_example():
    if animator.current_example < len(animator.example_arrays) - 1:
        animator.current_example += 1
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(WHITE)
    root = animator._sorted_array_to_bst(sorted(animator.example_arrays[animator.current_example]))
    animator._assign_positions(root, WIDTH//2, 50, 200)
    animator._draw_tree(surface, root)
    
    buffer = BytesIO()
    pygame.image.save(surface, buffer, format="PNG")
    return jsonify({
        'frame': base64.b64encode(buffer.getvalue()).decode('utf-8'),
        'currentExample': animator.current_example
    })

if __name__ == '__main__':
    app.run(port=5000)