import numpy as np
import matplotlib.pyplot as plt
import math

# Generate random coordinates for 10 cities
num_cities = 10
cities = np.random.rand(num_cities, 2) * 100  # Coordinates of cities in a 100x100 grid


# Function to calculate Euclidean distance between two cities
def euclidean_distance(city1, city2):
    return np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Visualize cities
def visualize_cities(cities):
    plt.scatter(cities[:, 0], cities[:, 1], color="blue")
    for i, city in enumerate(cities):
        plt.text(city[0], city[1], f"City {i}")
    plt.title("Cities on 2D Plane")
    plt.show()


visualize_cities(cities)  # Show the initial city layout


# Function to generate a random initial path (a random permutation of cities)
def generate_initial_path():
    return np.random.permutation(num_cities)


# Function to calculate the total distance of a given path
def calculate_total_distance(path, cities):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += euclidean_distance(cities[path[i]], cities[path[i + 1]])
    # Add distance to return to the starting city
    total_distance += euclidean_distance(cities[path[-1]], cities[path[0]])
    return total_distance


# Generate a random initial path and calculate its distance
initial_path = generate_initial_path()
initial_distance = calculate_total_distance(initial_path, cities)
print(f"Initial Path: {initial_path}")
print(f"Initial Distance: {initial_distance}")


# Function to generate a neighboring solution by swapping two cities
def generate_neighbor(path):
    new_path = path.copy()
    idx1, idx2 = np.random.randint(0, num_cities, size=2)
    new_path[idx1], new_path[idx2] = new_path[idx2], new_path[idx1]
    return new_path


# Simulated Annealing Algorithm
def simulated_annealing(cities, initial_path, initial_temp, cooling_rate, min_temp):
    # initialize variables
    current_path = initial_path.copy()
    current_distance = calculate_total_distance(current_path, cities)
    temperature = initial_temp

    # track the best solution found
    best_path = current_path.copy()
    best_distance = current_distance

    # continue until the system cools
    while temperature > min_temp:
        # generate neighbor solution
        neighbor_path = generate_neighbor(current_path)
        neighbor_distance = calculate_total_distance(neighbor_path, cities)

        # calculate difference in distances
        distance_diff = neighbor_distance - current_distance

        # decide if we accept the neighbor solution
        if distance_diff < 0:  # if neighbor is better, always accept
            accept = True
        else:
            # accept worse solutions with a probability depending on temperature
            probability = math.exp(-distance_diff / temperature)
            accept = np.random.random() < probability

        # update current solution if accepted
        if accept:
            current_path = neighbor_path.copy()
            current_distance = neighbor_distance

            # update best solution if current solution is better
            if current_distance < best_distance:
                best_path = current_path.copy()
                best_distance = current_distance
                # Visualize the current best path
                visualize_path(best_path, cities)

        # cool down the temperature
        temperature *= cooling_rate

    return best_path, best_distance


# Visualization of the path
def visualize_path(path, cities):
    plt.plot(cities[path, 0], cities[path, 1], "ro-", label="Path")
    plt.plot(
        [cities[path[-1], 0], cities[path[0], 0]],
        [cities[path[-1], 1], cities[path[0], 1]],
        "ro-",
    )
    plt.title(f"Current Path (Distance: {calculate_total_distance(path, cities):.2f})")
    plt.show()


# Run simulated annealing
best_path, best_distance = simulated_annealing(
    cities, initial_path, initial_temp=10000, cooling_rate=0.995, min_temp=0.1
)
print(f"Best Path: {best_path}")
print(f"Best Distance: {best_distance}")
