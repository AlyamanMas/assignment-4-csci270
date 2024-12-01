import numpy as np
import matplotlib.pyplot as plt
import random

# Define the grid size and locations
grid_size = 10
grid = np.zeros((grid_size, grid_size))

# Define the robot's start position, pickup locations, and packing station
start_pos = (0, 0)  # top-left corner
pickup_locations = [(2, 3), (4, 7), (7, 2), (8, 8)]
packing_station = (9, 9)  # bottom-right corner

# Mark obstacles on the grid
obstacles = [(1, 5), (3, 3), (6, 6), (7, 5)]
for obs in obstacles:
    grid[obs] = -1  # Mark obstacles as -1


# Visualize the initial grid
def visualize_grid(path=None):
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap="gray_r")

    # Mark obstacles
    for obs in obstacles:
        ax.text(obs[1], obs[0], "X", ha="center", va="center", color="red")

    # Mark start, pickup locations, and packing station
    ax.text(start_pos[1], start_pos[0], "S", ha="center", va="center", color="blue")
    for loc in pickup_locations:
        ax.text(loc[1], loc[0], "P", ha="center", va="center", color="green")
    ax.text(
        packing_station[1],
        packing_station[0],
        "D",
        ha="center",
        va="center",
        color="purple",
    )

    # If path is provided, draw the path
    if path is not None:
        x_coords, y_coords = zip(*path)
        ax.plot(y_coords, x_coords, marker="o", color="orange")

    plt.show()


# Visualize the initial grid
visualize_grid()


# Create an initial random path
def generate_initial_path():
    path = [start_pos]
    remaining_pickups = pickup_locations.copy()
    random.shuffle(remaining_pickups)
    path.extend(remaining_pickups)
    path.append(packing_station)
    return path


# Generate and visualize the initial path
initial_path = generate_initial_path()
visualize_grid(initial_path)


# Calculate the Manhattan distance between two points
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Calculate the total travel distance of the path
def calculate_total_distance(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += manhattan_distance(path[i], path[i + 1])
    return total_distance


# Evaluate the initial path
initial_distance = calculate_total_distance(initial_path)
print("Initial Path Distance:", initial_distance)


# Generate neighboring solutions by swapping the order of two pickup locations
def generate_neighbors(path):
    neighbors = []
    # Only swap pickup locations (keep start and packing station fixed)
    for i in range(1, len(path) - 2):
        for j in range(i + 1, len(path) - 1):
            neighbor = path.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors


# Generate neighbors for the initial path
neighbors = generate_neighbors(initial_path)


# Implement hill climbing algorithm
def hill_climbing(initial_path):
    current_path = initial_path
    current_distance = calculate_total_distance(current_path)
    improvement = True

    while improvement:
        improvement = False
        neighbors = generate_neighbors(current_path)

        # Find the best neighbor
        for neighbor in neighbors:
            neighbor_distance = calculate_total_distance(neighbor)
            if neighbor_distance < current_distance:
                current_path = neighbor
                current_distance = neighbor_distance
                improvement = True
                # Visualize current best path
                visualize_grid(current_path)
                break

    return current_path, current_distance


# Run hill climbing and visualize the steps
final_path, final_distance = hill_climbing(initial_path)
print("Final Path:", final_path)
print("Final Distance:", final_distance)

# Run the hill climbing algorithm and visualize the steps
final_path, final_distance = hill_climbing(initial_path)
print("Final Optimized Path:", final_path)  # Print the final optimized path
print(
    "Final Distance:", final_distance
)  # Print the total distance of the optimized path
