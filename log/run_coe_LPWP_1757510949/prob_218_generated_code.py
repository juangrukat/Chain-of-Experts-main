from scipy.optimize import linprog

def prob_218():
    c = [-2.50, -3.55]  # Coefficients of the objective function to minimize (-2.50x1 - 3.55x2)
    A = [[1, 0], [0, 1], [1, 1]]  # Coefficients of the left-hand side of the constraints
    b = [50, 40, 70]  # Right-hand side of the constraints

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

    return round(-res.fun, 2)  # Return the maximum profit