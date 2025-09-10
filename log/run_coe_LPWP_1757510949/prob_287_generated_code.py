from scipy.optimize import linprog

def prob_287():
    c = [820, 550]  # Coefficients of the objective function to minimize total cost
    A = [[-20, -15], [1, 1], [0, -0.6]]  # Coefficients of the constraints
    b = [-320, 0, 0]  # Right-hand side of the constraints

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

    return res.fun