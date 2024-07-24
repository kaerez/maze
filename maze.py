import os
import sys
from PIL import Image, ImageDraw
import random

# Maze size
CELL_SIZE = 20
COLS, ROWS = 20, 20

# Image size
IMAGE_WIDTH = COLS * CELL_SIZE + 2 * CELL_SIZE
IMAGE_HEIGHT = ROWS * CELL_SIZE + 2 * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visited = False
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.previous = None

def generate_maze(cells):
    stack = []
    current = cells[0][0]
    current.visited = True
    stack.append(current)

    while stack:
        neighbors = get_unvisited_neighbors(current, cells)
        if neighbors:
            next_cell = random.choice(neighbors)
            remove_wall(current, next_cell)
            next_cell.visited = True
            next_cell.previous = current
            stack.append(next_cell)
            current = next_cell
        else:
            current = stack.pop()

def get_unvisited_neighbors(cell, cells):
    neighbors = []
    if cell.x > 0 and not cells[cell.x - 1][cell.y].visited:
        neighbors.append(cells[cell.x - 1][cell.y])
    if cell.x < COLS - 1 and not cells[cell.x + 1][cell.y].visited:
        neighbors.append(cells[cell.x + 1][cell.y])
    if cell.y > 0 and not cells[cell.x][cell.y - 1].visited:
        neighbors.append(cells[cell.x][cell.y - 1])
    if cell.y < ROWS - 1 and not cells[cell.x][cell.y + 1].visited:
        neighbors.append(cells[cell.x][cell.y + 1])
    return neighbors

def remove_wall(cell1, cell2):
    if cell1.x == cell2.x and cell1.y < cell2.y:
        cell1.walls[2] = False
        cell2.walls[0] = False
    elif cell1.x == cell2.x and cell1.y > cell2.y:
        cell1.walls[0] = False
        cell2.walls[2] = False
    elif cell1.y == cell2.y and cell1.x < cell2.x:
        cell1.walls[1] = False
        cell2.walls[3] = False
    elif cell1.y == cell2.y and cell1.x > cell2.x:
        cell1.walls[3] = False
        cell2.walls[1] = False

def draw_maze(cells, draw):
    for row in cells:
        for cell in row:
            if cell.visited:
                draw.rectangle((cell.x * CELL_SIZE + CELL_SIZE, cell.y * CELL_SIZE + CELL_SIZE, (cell.x + 1) * CELL_SIZE + CELL_SIZE, (cell.y + 1) * CELL_SIZE + CELL_SIZE), fill=WHITE)
            if cell.walls[0]:
                draw.line((cell.x * CELL_SIZE + CELL_SIZE, cell.y * CELL_SIZE + CELL_SIZE, (cell.x + 1) * CELL_SIZE + CELL_SIZE, cell.y * CELL_SIZE + CELL_SIZE), fill=BLACK, width=2)
            if cell.walls[1]:
                draw.line(((cell.x + 1) * CELL_SIZE + CELL_SIZE, cell.y * CELL_SIZE + CELL_SIZE, (cell.x + 1) * CELL_SIZE + CELL_SIZE, (cell.y + 1) * CELL_SIZE + CELL_SIZE), fill=BLACK, width=2)
            if cell.walls[2]:
                draw.line(((cell.x + 1) * CELL_SIZE + CELL_SIZE, (cell.y + 1) * CELL_SIZE + CELL_SIZE, cell.x * CELL_SIZE + CELL_SIZE, (cell.y + 1) * CELL_SIZE + CELL_SIZE), fill=BLACK, width=2)
            if cell.walls[3]:
                draw.line((cell.x * CELL_SIZE + CELL_SIZE, (cell.y + 1) * CELL_SIZE + CELL_SIZE, cell.x * CELL_SIZE + CELL_SIZE, cell.y * CELL_SIZE + CELL_SIZE), fill=BLACK, width=2)

def draw_entrance(draw, entrance):
    dot_radius = 5
    dot_x = entrance.x * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
    dot_y = entrance.y * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
    draw.ellipse((dot_x - dot_radius, dot_y - dot_radius, dot_x + dot_radius, dot_y + dot_radius), fill=GREEN)

def draw_exit(draw, exit):
    dot_radius = 5
    dot_x = exit.x * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
    dot_y = exit.y * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
    draw.ellipse((dot_x - dot_radius, dot_y - dot_radius, dot_x + dot_radius, dot_y + dot_radius), fill=RED)

def draw_path(draw, entrance, exit):
    current = exit
    path = []
    while current is not None:
        path.append(current)
        current = current.previous
    path.reverse()

    for i in range(len(path) - 1):
        cell = path[i]
        next_cell = path[i + 1]
        x1 = cell.x * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
        y1 = cell.y * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
        x2 = next_cell.x * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
        y2 = next_cell.y * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
        draw.line((x1, y1, x2, y2), fill=BLUE, width=1)

def get_available_filename(base_name):
    index = 1
    filename = base_name
    while os.path.exists(filename):
        filename = f"{os.path.splitext(base_name)[0]}{index}{os.path.splitext(base_name)[1]}"
        index += 1
    return filename

def main():
    if any(arg in sys.argv for arg in ["--help", "-help", "help", "--?", "-?"]):
        print("Optional settings:\n[-i] In - Show entry marker\n[-o] Out - Show exit marker\n[-a] Answer - Show answer")
        return

    show_entrance = "-i" in sys.argv
    show_exit = "-o" in sys.argv
    show_answer = "-a" in sys.argv

    cells = [[Cell(x, y) for y in range(ROWS)] for x in range(COLS)]
    generate_maze(cells)
    entrance = cells[0][0]
    exit = cells[COLS - 1][ROWS - 1]

    # Remove the walls at the entrance and exit
    entrance.walls[3] = False  # Remove left wall of entrance
    exit.walls[1] = False  # Remove right wall of exit

    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=WHITE)
    draw = ImageDraw.Draw(img)

    draw_maze(cells, draw)
    if show_entrance:
        draw_entrance(draw, entrance)
    if show_exit:
        draw_exit(draw, exit)
    if show_answer:
        draw_path(draw, entrance, exit)

    base_name = "maze.png"
    filename = get_available_filename(base_name)
    img.save(filename)
    print(f"Saved maze as {filename}")

if __name__ == "__main__":
    main()
