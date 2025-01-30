import pygame
import random
import time

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balanced BST Animation")
pygame.display.set_caption("Binary Search Tree Balancing")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
GRAY = (150, 150, 150)

# Load images (replace with your image paths)
BG_IMAGE = pygame.transform.scale(pygame.image.load("green_background.jpg"), (WIDTH, HEIGHT))
LEAF_IMAGE = pygame.transform.scale(pygame.image.load("leaf.png"), (50, 50))  # 40x40 leaf image

# Fonts
font = pygame.font.Font(None, 30)

# Tree Node class
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

# Build initial unbalanced (right-skewed) tree
def build_unbalanced_tree(arr):
    if not arr:
        return None
    node = TreeNode(arr[0])
    node.right = build_unbalanced_tree(arr[1:])
    return node

# Convert to Balanced BST
def sorted_array_to_bst(arr):
    if not arr:
        return None
    mid = len(arr) // 2
    root = TreeNode(arr[mid])
    root.left = sorted_array_to_bst(arr[:mid])
    root.right = sorted_array_to_bst(arr[mid + 1:])
    return root

# Position nodes in the screen
def assign_positions(node, x, y, x_offset):
    if node:
        node.x, node.y = x, y
        assign_positions(node.left, x - x_offset, y + 60, x_offset // 2)
        assign_positions(node.right, x + x_offset, y + 60, x_offset // 2)

# Draw the tree on screen
def draw_tree(node):
    if node:
        if node.left:
            pygame.draw.line(screen, BLACK, (node.x, node.y), (node.left.x, node.left.y), 2)
        if node.right:
            pygame.draw.line(screen, BLACK, (node.x, node.y), (node.right.x, node.right.y), 2)
        screen.blit(LEAF_IMAGE, (node.x - 20, node.y - 20))  # Center leaf image
        text = font.render(str(node.val), True, BLACK)
        screen.blit(text, (node.x - 10, node.y - 10))  # Center text on leaf
        draw_tree(node.left)
        draw_tree(node.right)

# Animation function using BFS to show levels incrementally
def animate_balancing(old_root, sorted_array):
    balanced_root = sorted_array_to_bst(sorted_array)
    assign_positions(balanced_root, WIDTH // 2, 50, 200)
    steps = []
    
    # BFS traversal to collect nodes level by level
    queue = [balanced_root]
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            if not queue:
                break
            node = queue.pop(0)
            if node:
                steps.append(node)
                queue.append(node.left)
                queue.append(node.right)
    
    # Animate each level
    for i in range(len(steps)):
        screen.blit(BG_IMAGE, (0, 0))
        current_nodes = steps[:i+1]
        # Draw nodes and connections
        for node in current_nodes:
            if node:
                # Draw lines to children if they are in current_nodes
                if node.left and node.left in current_nodes:
                    pygame.draw.line(screen, BLACK, (node.x, node.y), (node.left.x, node.left.y), 2)
                if node.right and node.right in current_nodes:
                    pygame.draw.line(screen, BLACK, (node.x, node.y), (node.right.x, node.right.y), 2)
                screen.blit(LEAF_IMAGE, (node.x-20, node.y-20))  # Center leaf image
                text = font.render(str(node.val), True, BLACK)
                screen.blit(text, (node.x - 10, node.y - 10))  # Center text on leaf
            
        pygame.display.update()
        time.sleep(0.5)
    return balanced_root

# Main
running = True
example_arrays = [
    [1, 2, 3, 4, 5, 6, 7],
    [4, 10, 15, 20, 25, 30, 35],
    [5, 15, 25, 35, 45, 55, 65]
]
current_example = 0
array = example_arrays[current_example].copy()
array.sort()
root = build_unbalanced_tree(array)
assign_positions(root, WIDTH // 2, 50, 200)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 50, 100, 40)
next_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 50, 100, 40)
balanced = False

while running:
    screen.blit(BG_IMAGE, (0, 0))  # Green background

    draw_tree(root)
    
    # Draw buttons
    pygame.draw.rect(screen, GREEN if not balanced else GRAY, start_button)
    start_text = font.render("Start", True, BLACK)
    screen.blit(start_text, (start_button.x + 25, start_button.y + 10))
    
    next_disabled = current_example >= len(example_arrays) - 1
    pygame.draw.rect(screen, GRAY if next_disabled else GREEN, next_button)
    next_text = font.render("Next", True, BLACK)
    screen.blit(next_text, (next_button.x + 25, next_button.y + 10))
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if start_button.collidepoint(x, y) and not balanced:
                sorted_arr = example_arrays[current_example].copy()
                sorted_arr.sort()
                root = animate_balancing(root, sorted_arr)
                balanced = True
            elif next_button.collidepoint(x, y) and not next_disabled:
                current_example += 1
                array = example_arrays[current_example].copy()
                array.sort()
                root = build_unbalanced_tree(array)
                assign_positions(root, WIDTH // 2, 50, 200)
                balanced = False

pygame.quit()