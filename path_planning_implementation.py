import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Environment settings
size = 20  # Environment size
n_obstacles = 40  # Number of obstacles
obstacles = set()

# Generate random obstacles
while len(obstacles) < n_obstacles:
    obstacles.add((random.randint(0, size-1), random.randint(0, size-1)))

# Start position for the robot
start_pos = (random.randint(0, size-1), random.randint(0, size-1))
while start_pos in obstacles:
    start_pos = (random.randint(0, size-1), random.randint(0, size-1))

# Directions the robot can move
directions = [(1,0), (-1,0), (0,1), (0,-1)]

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1, size)
ax.set_ylim(-1, size)

# Plot obstacles
for obstacle in obstacles:
    ax.scatter(obstacle[0], obstacle[1], color='red', s=100, marker='s')  # Use square markers for obstacles

# Initialize the path plot
line, = ax.plot([], [], lw=2, color='blue', marker='o', markersize=8, linestyle='-', markerfacecolor='green')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    xdata, ydata = line.get_data()
    next_pos = frame
    xdata.append(next_pos[0])
    ydata.append(next_pos[1])
    line.set_data(xdata, ydata)
    return line,

def move_robot(start_pos, ax):
    visited = set([start_pos])
    path = [start_pos]
    current_pos = start_pos
    
    for _ in range(100):  # Limit the steps to avoid infinite loop
        possible_moves = [(current_pos[0] + d[0], current_pos[1] + d[1]) for d in directions if (current_pos[0] + d[0], current_pos[1] + d[1]) not in visited]
        possible_moves = [move for move in possible_moves if 0 <= move[0] < size and 0 <= move[1] < size and move not in obstacles]

        # Sort possible moves by the number of unvisited neighbors they have, preferring moves that lead to more exploration
        possible_moves.sort(key=lambda move: -sum(1 for d in directions if (move[0]+d[0], move[1]+d[1]) not in visited and 0 <= move[0]+d[0] < size and 0 <= move[1]+d[1] < size and (move[0]+d[0], move[1]+d[1]) not in obstacles))
        
        if not possible_moves:  # If there are no unvisited moves left, stop moving
            break
        
        current_pos = possible_moves[0]  # Choose the move leading to the most unvisited neighbors
        visited.add(current_pos)
        path.append(current_pos)
        
    return path

# Generate the robot's path
path = move_robot(start_pos, ax)

# Creating the animation with a slower movement
ani = FuncAnimation(fig, update, frames=path, init_func=init, blit=True, interval=500)  # Increased interval to slow down the animation

plt.grid(True)
plt.show()

