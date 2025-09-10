from scipy.optimize import linprog

def prob_274(first_dose, second_dose):
    c = [20, 60]  # Coefficients of the objective function to minimize gelatine usage
    A = [[30, 65], [-1, 0], [0, -1]]  # Coefficients of the constraints
    b = [35000, -1, -40]  # Right-hand side of the constraints

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

    return int(res.fun)  # Return the minimized amount of gelatine used