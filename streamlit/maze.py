import os
import sys
from PIL import Image, ImageDraw
import random
import streamlit as st
from io import BytesIO
import pyperclip

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
    for x in range(COLS):
        for y in range(ROWS):
            cell = cells[x][y]
            x1, y1 = x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

            if cell.walls[0]:
                draw.line([(x1, y1), (x2, y1)], fill=BLACK)
            if cell.walls[1]:
                draw.line([(x2, y1), (x2, y2)], fill=BLACK)
            if cell.walls[2]:
                draw.line([(x1, y2), (x2, y2)], fill=BLACK)
            if cell.walls[3]:
                draw.line([(x1, y1), (x1, y2)], fill=BLACK)

def draw_entrance(draw, entrance):
    x = entrance.x * CELL_SIZE + CELL_SIZE // 2
    y = entrance.y * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 8
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=GREEN)

def draw_exit(draw, exit):
    x = exit.x * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
    y = exit.y * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 8
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=RED)

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

def copy_image_to_clipboard(image):
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = buffer.getvalue()
    pyperclip.copy(img_str)

def main():
    st.title("Maze Generator")

    show_entrance = st.checkbox('Show entrance marker')
    show_exit = st.checkbox('Show exit marker')
    show_answer = st.checkbox('Show answer')
    generate_button = st.button('Generate Maze')

    if generate_button:
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

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        st.image(img, caption="Generated Maze")
        st.download_button(
            label="Download Maze",
            data=buffer,
            file_name="maze.png",
            mime="image/png"
        )
        
        if st.button('Copy Maze to Clipboard'):
            copy_image_to_clipboard(img)
            st.success('Maze copied to clipboard!')

if __name__ == "__main__":
    main()
