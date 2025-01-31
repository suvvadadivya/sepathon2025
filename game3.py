# server.py
import pygame
import base64
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS
import os

# Pygame headless setup
# os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
NODE_SIZE = 60
FONT_SIZE = 24

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"http://localhost:3000"}})

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

class BSTAnimator:
    def __init__(self):
        self.example_arrays = [
            [1, 2, 3, 4, 5, 6, 7],
            [4, 10, 15, 20, 25, 30, 35],
            [5, 15, 25, 35, 45, 55, 65]
        ]
        self.current_example = 0
        self.font = pygame.font.SysFont('freesansbold.ttf', FONT_SIZE)
        self.leaf_img = self._load_leaf_image()
        self.bg_img = self._load_background()

    def _load_leaf_image(self):
        try:
            leaf = pygame.image.load('leaf.png')
            return pygame.transform.scale(leaf, (NODE_SIZE, NODE_SIZE))
        except FileNotFoundError:
            surf = pygame.Surface((NODE_SIZE, NODE_SIZE), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (50, 150, 50), (0, 0, NODE_SIZE, NODE_SIZE))
            pygame.draw.ellipse(surf, BLACK, (0, 0, NODE_SIZE, NODE_SIZE), 2)
            return surf

    def _load_background(self):
        try:
            bg = pygame.image.load('forest_bg.jpg')
            return pygame.transform.scale(bg, (WIDTH, HEIGHT))
        except FileNotFoundError:
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((34, 139, 34))  # Forest green
            return surf

    def _draw_node(self, surface, node):
        if node:
            # Draw connections first
            if node.left:
                pygame.draw.line(surface, (0, 0, 0), (node.x, node.y), 
                               (node.left.x, node.left.y), 3)
            if node.right:
                pygame.draw.line(surface, (0, 0, 0), (node.x, node.y), 
                               (node.right.x, node.right.y), 3)
            
            # Draw leaf image
            leaf_rect = self.leaf_img.get_rect(center=(node.x, node.y))
            surface.blit(self.leaf_img, leaf_rect)
            
            # Draw value text
            text = self.font.render(str(node.val), True, (0, 0, 0))
            text_rect = text.get_rect(center=(node.x, node.y))
            surface.blit(text, text_rect)

    def _assign_positions(self, root):
        # Calculate tree depth to position nodes
        def get_depth(node):
            return 1 + max(get_depth(node.left), get_depth(node.right)) if node else 0
        
        depth = get_depth(root)
        current_level = [(root, WIDTH//2, 100)]
        
        while current_level:
            next_level = []
            x_offset = WIDTH // (2 ** (depth + 1))
            
            for node, x, y in current_level:
                if node:
                    node.x, node.y = x, y
                    next_level.append((node.left, x - x_offset, y + 100))
                    next_level.append((node.right, x + x_offset, y + 100))
            
            current_level = next_level
            depth -= 1

    def generate_animation(self, arr):
        sorted_arr = sorted(arr)
        root = self._sorted_array_to_bst(sorted_arr)
        self._assign_positions(root)
        
        frames = []
        queue = [root]
        
        while queue:
            # Create frame with background
            frame = self.bg_img.copy()
            
            # Draw all nodes processed so far
            for node in queue:
                if node:
                    self._draw_node(frame, node)
            
            # Convert to base64
            buffer = BytesIO()
            pygame.image.save(frame, buffer, "PNG")
            frames.append(base64.b64encode(buffer.getvalue()).decode('utf-8'))
            
            # Expand queue for next level
            next_level = []
            for node in queue:
                if node:
                    next_level.extend([node.left, node.right])
            queue = next_level if any(next_level) else []
        
        return frames

    def _sorted_array_to_bst(self, arr):
        if not arr:
            return None
        mid = len(arr) // 2
        root = TreeNode(arr[mid])
        root.left = self._sorted_array_to_bst(arr[:mid])
        root.right = self._sorted_array_to_bst(arr[mid+1:])
        return root

animator = BSTAnimator()

@app.route('/api/current')
def get_current_state():
    surface = animator.bg_img.copy()
    arr = sorted(animator.example_arrays[animator.current_example])
    root = animator._sorted_array_to_bst(arr)
    animator._assign_positions(root)
    
    # Draw all nodes
    def draw_all(node):
        if node:
            animator._draw_node(surface, node)
            draw_all(node.left)
            draw_all(node.right)
    draw_all(root)
    
    buffer = BytesIO()
    pygame.image.save(surface, buffer, "PNG")
    return jsonify({
        'frame': base64.b64encode(buffer.getvalue()).decode('utf-8'),
        'currentExample': animator.current_example,
        'totalExamples': len(animator.example_arrays)
    })

@app.route('/api/animate')
def start_animation():
    frames = animator.generate_animation(
        animator.example_arrays[animator.current_example]
    )
    return jsonify({'frames': frames})

@app.route('/api/next')
def next_example():
    if animator.current_example < len(animator.example_arrays) - 1:
        animator.current_example += 1
    return get_current_state()

if __name__ == '__main__':
    app.run(port=9500)