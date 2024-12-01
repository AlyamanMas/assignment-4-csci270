import numpy as np
import matplotlib.pyplot as plt


# Define the cost function that represents the production cost
def cost_function(x):
    x1, x2 = x  # Unpack the input parameters (quantities of raw materials)
    # Calculate and return the production cost based on the given formula
    return x1**2 + x2**2 + x1 * x2 - 14 * x1 - 16 * x2 + 50


# Generate a grid of cost function values for visualization
def generate_cost_surface(x_range, y_range):
    # Create a mesh grid for the given ranges
    X1, X2 = np.meshgrid(x_range, y_range)
    # Evaluate the cost function over the grid
    Z = np.zeros_like(X1)
    for i in range(len(x_range)):
        for j in range(len(y_range)):
            Z[j, i] = cost_function([X1[j, i], X2[j, i]])
    return X1, X2, Z  # Return the grid and cost values


# Visualize the cost function surface
def visualize_cost_surface(x_range, y_range):
    # Generate the cost surface
    X1, X2, Z = generate_cost_surface(x_range, y_range)
    plt.figure(figsize=(10, 6))  # Create a new figure
    # Plot filled contours of the cost function
    plt.contourf(X1, X2, Z, levels=50, cmap="viridis")
    plt.colorbar(label="Cost")  # Add a color bar for reference
    plt.xlabel("Raw Material A Quantity (x1)")  # Label the x-axis
    plt.ylabel("Raw Material B Quantity (x2)")  # Label the y-axis
    plt.title("Cost Function Surface")  # Title of the plot
    plt.show()  # Display the plot


# Function to create an initial simplex based on an initial guess
def create_simplex(initial_guess, step_size):
    # Define a simplex around the initial guess
    simplex = np.array(
        [
            initial_guess,  # First vertex is the initial guess
            initial_guess
            + np.array([step_size, 0]),  # Vertex 1, offset by step size in x1
            initial_guess
            + np.array([0, step_size]),  # Vertex 2, offset by step size in x2
        ]
    )
    return simplex  # Return the simplex array


# Set an initial guess and step size for the simplex
initial_guess = np.array([5, 5])  # Starting point for optimization
step_size = 1.0  # Step size for creating the simplex
# Create the initial simplex using the above values
simplex = create_simplex(initial_guess, step_size)

# Print the initial simplex vertices for verification
print("Initial Simplex Vertices:")
print(simplex)  # Display the vertices of the initial simplex


# Nelder-Mead optimization algorithm
def nelder_mead(
    simplex, cost_function, max_iterations=100, alpha=1, gamma=2, rho=0.5, sigma=0.5
):
    for iteration in range(
        max_iterations
    ):  # Loop through a maximum number of iterations
        # Sort the simplex by cost function values
        simplex = sorted(
            simplex, key=cost_function
        )  # Sort vertices based on cost function values

        # Calculate the centroid of the simplex excluding the worst point
        centroid = np.mean(
            simplex[:-1], axis=0
        )  # Compute the centroid of the best vertices

        # Reflect the worst point
        worst_point = simplex[-1]  # Get the worst point in the simplex
        reflected_point = centroid + alpha * (
            centroid - worst_point
        )  # Reflect the point across the centroid

        # Evaluate the cost of the reflected point
        if cost_function(reflected_point) < cost_function(simplex[0]):
            # If the reflected point is better than the best point
            # Expand the simplex
            expanded_point = centroid + gamma * (reflected_point - centroid)  # Expand
            # Replace worst with expanded if it is better
            if cost_function(expanded_point) < cost_function(reflected_point):
                simplex[-1] = expanded_point  # Replace worst with expanded point
            else:
                simplex[-1] = reflected_point  # Replace worst with reflected point
        elif cost_function(reflected_point) < cost_function(simplex[-2]):
            simplex[-1] = reflected_point  # Replace worst with reflected point
        else:
            # If reflected point is worse than second best
            if cost_function(reflected_point) < cost_function(worst_point):
                simplex[-1] = reflected_point  # Replace with reflected point
            # Contract the simplex
            contracted_point = centroid + rho * (worst_point - centroid)  # Contract
            if cost_function(contracted_point) < cost_function(worst_point):
                simplex[-1] = contracted_point  # Replace with contracted point
            else:
                # Shrink the simplex towards the best point
                simplex = simplex[0] + sigma * (
                    simplex - simplex[0]
                )  # Shrink the simplex

        # Print current iteration and the best cost found
        print(
            f"Iteration {iteration + 1}: Best Cost = {round(cost_function(simplex[0]), 2)}"
        )

    return simplex  # Return the optimized simplex vertices


# Function to visualize the simplex movement
def visualize_simplex_movement(simplex_history, cost_function):
    plt.figure(figsize=(10, 6))  # Create a new figure
    # Create a grid for the cost function
    x1, x2 = np.meshgrid(np.linspace(-5, 15, 400), np.linspace(-5, 15, 400))
    Z = cost_function([x1, x2])  # Calculate the cost function over the grid
    plt.contourf(
        x1, x2, Z, levels=50, cmap="viridis"
    )  # Plot filled contours of the cost function

    for simplex in simplex_history:  # Loop through the history of simplex vertices
        plt.plot(simplex[:, 0], simplex[:, 1], "r-")  # Plot the simplex movements
    plt.colorbar(label="Cost")  # Add a color bar for reference
    plt.xlabel("Raw Material A Quantity (x1)")  # Label the x-axis
    plt.ylabel("Raw Material B Quantity (x2)")  # Label the y-axis
    plt.title("Movement of Simplex During Optimization")  # Title of the plot
    plt.show()  # Display the plot


# Store simplex history for visualization
simplex_history = [simplex.copy()]  # Store the initial simplex
# Run the Nelder-Mead algorithm and visualize
optimized_simplex = nelder_mead(simplex, cost_function)  # Run the algorithm
visualize_simplex_movement(
    simplex_history, cost_function
)  # Visualize the movement of the simplex
