import streamlit as st
import pyperclip
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# Dummy function to generate a maze image for demonstration purposes
def generate_maze(entrance_marker, exit_marker, solution):
    maze = np.random.rand(10, 10)
    plt.imshow(maze, cmap='binary')
    plt.title('Maze' + (' with Solution' if solution else ''))
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(False)

    if entrance_marker:
        plt.scatter(0, 0, color='red', label='Entrance Marker')
    if exit_marker:
        plt.scatter(9, 9, color='blue', label='Exit Marker')

    if solution:
        # Draw a simple solution path for demonstration
        x = np.linspace(0, 9, 100)
        y = x
        plt.plot(x, y, color='green', label='Solution')

    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Streamlit app layout
st.title("Maze Generator")

# Create checkboxes
entrance_marker = st.checkbox("Entrance marker")
exit_marker = st.checkbox("Exit marker")
solution = st.checkbox("Solution")

# Generate button
if st.button("Generate"):
    # Generate maze with the selected options
    buf = generate_maze(entrance_marker, exit_marker, solution)
    img = Image.open(buf)

    st.image(img, caption='Generated Maze', use_column_width=True)

    # Copy to clipboard button
    if st.button("Copy to Clipboard"):
        pyperclip.copy(img)
        st.success("Image copied to clipboard!")

    # Download button
    st.download_button(
        label="Download Image",
        data=buf,
        file_name="maze.png",
        mime="image/png"
    )

    if solution:
        # Generate maze without the solution for comparison
        buf_without_solution = generate_maze(entrance_marker, exit_marker, False)
        img_without_solution = Image.open(buf_without_solution)

        st.image(img_without_solution, caption='Maze without Solution', use_column_width=True)

        # Copy to clipboard button for maze without solution
        if st.button("Copy Maze without Solution to Clipboard"):
            pyperclip.copy(img_without_solution)
            st.success("Image without solution copied to clipboard!")

        # Download button for maze without solution
        st.download_button(
            label="Download Maze without Solution",
            data=buf_without_solution,
            file_name="maze_without_solution.png",
            mime="image/png"
        )
