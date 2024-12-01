This repository contains the solution for the three parts of assignment 4 of the CSCI270 course in the College of Charleston. The assignment uses three different optimization algorithms in three different problems.

# Warehouse Navigation System

Part 1 is about the optimization of robotic movement in a warehouse environment. We apply hill climbing methodology to determine the most efficient pathways in grid system. The algorithm implements a Manhattan distance metric and navigates through multiple pickup points. We constantly plot each iteration to show the improvement of our path.

# Traveling Salesman Implementation

In this part, we solve the traveling salesman problem using simulated annealing to try to minimize distance. This allows for some randomness while also making compromises some time to allow us to explore the solutions domain. This works particularly well in cases with many competing local minima.

We use a cooling schedule to maintain a careful balance between exploration and exploitation, gradually going from exploring the solution space with compromises to focusing on local optimization. This approach ensures thorough investigation of the solution space while maintaining computational efficiency.

# Production Process Optimization

In part 3, we use the Nelder-Mead algorithm to optimize parameters of a production chain. This method is great when we are dealing with multi-dimensional data, where other optimization algorithms may struggle. We use simplexes to navigate the cost function, and use geometric transformations to move around the function with the goal of minimizing the cost function.

Starting with an initial guess, the algorithm shows good efficiency in converging toward local optima.

# Running the code

The code is written with the python programming language, and as such, a python runtime environment is needed to run the code. The libraries `numpy` and `matplotlib` are also required to run the code. Each part is in a different file.
