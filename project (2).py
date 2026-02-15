import sys
import math
import sympy
from sympy import pretty


def main():
    values = get_values()  # gets a dict of values for variables
    units = get_units(values)  # get aproriate units
    solved, equation = get_result(values)  # does calculation

    if solved:  # if there is a solution
        print(f"Equation used: {pretty(equation)}")
        for sol in solved:
            print(f"{sol:.2f} {units}")

    else:
        print("No solution found.")


def get_values():
    values = {  # create a dict for values
        "theta": None,
        "vi": None,  # initial velocity total
        "vix": None,  # initial velocity x direction
        "viy": None,  # initial velocity y direction
        "vf": None,  # final velocity total
        "vfx": None,  # final velocity x direction
        "vfy": None,  # final velocity y direction
        "a": None,  # acceleration total
        "ax": None,  # acceleration x direction
        "ay": None,  # acceleration y direction
        "d": None,  # displacement total
        "dx": None,  # displacement x direction
        "dy": None,  # displacement y direction
        "t": None,  # time
        "solve": None
    }
    # ask for user input
    valid_inputs = ("vi", "vf", "vix", "viy", "vfx", "vfy", "a", "ax", "ay", "d", "dx", "dy", "t")
    print("Enter an integer for each quantity and assume SI units")
    print("Don't include units!")
    print("If a quantity is unknown, enter '?' ")
    values["theta"] = input("What is your launch angle (degrees)? ")
    values["vi"] = input("What is your total initial velocity? ")
    values["vix"] = input("What is your x-initial velocity? ")
    values["viy"] = input("What is your y-initial velocity? ")
    values["vf"] = input("What is your total final velocity? ")
    values["vfx"] = input("What is your x-final velocity? ")
    values["vfy"] = input("What is your y-final velocity? ")
    values["a"] = input("What is your total acceleration? ")
    values["ax"] = input("What is your x-acceleration? ")
    values["ay"] = input("What is your y-acceleration? ")
    values["d"] = input("What is your total displacement? ")
    values["dx"] = input("What is your x-displacement? ")
    values["dy"] = input("What is your y-displacement? ")
    values["t"] = input("What is your total time? ")
    values["solve"] = input(f"what are you solving for?\n{valid_inputs} ")

    # checks if the value for solve key is valid
    if values["solve"] not in valid_inputs:
        sys.exit(f"Enter a valid variable to solve for\n{valid_inputs}")
    # convert string inputs to floats
    for key, value in values.items():
        if key == "solve":  # Don't convert the solve variable itself
            continue
        if value != "?":  # if the value is known
            try:
                values[key] = float(value)  # convert the values in each key from str->float
            except ValueError:
                sys.exit(f"Invalid input for {key}")
        elif value == "?":
            values[key] = None
    # checks if Solve is already known
    solvevar = values["solve"]
    if values[solvevar] != None:
        sys.exit(f'You cannot provide a value for {solvevar} if you are solving for it')
    return values


def get_result(values):
    vix = viy = vfx = vfy = None  # intialize
    dx = dy = ax = ay = None

    # helper function checks discrepancies between given values and theta calculated values
    def validate_assign(calc, given, name, source):
        if given is not None:
            if abs(given - calc) > 0.01:  # allow rounding
                sys.exit(f"Conflict: Given {name}={given} doesn't match "
                         f"calculated {name}={calc:.2f} from {source}")
                return given
        return calc

    # if there is a theta, calculate components
    if values["theta"] is not None:
        theta_rad = math.radians(values["theta"])  # convert theta into rad
        if values["vi"] is not None:
            vix_calc = values["vi"] * math.cos(theta_rad)
            viy_calc = values["vi"] * math.sin(theta_rad)
            # check if calculated components match given components
            vix = validate_assign(vix_calc, values["vix"], "vix", "vi and theta")
            viy = validate_assign(viy_calc, values["viy"], "viy", "vi and theta")
        else:
            vix = values["vix"]
            viy = values["viy"]

        if values["vf"] is not None:
            vfx_calc = values["vf"] * math.cos(theta_rad)
            vfy_calc = values["vf"] * math.sin(theta_rad)
            # check if calculated components match given components
            vfx = validate_assign(vfx_calc, values["vfx"], "vfx", "vf and theta")
            vfy = validate_assign(vfy_calc, values["vfy"], "vfy", "vf and theta")
        else:
            vfx = values["vfx"]
            vfy = values["vfy"]

        if values["d"] is not None:
            dx_calc = values["d"] * math.cos(theta_rad)
            dy_calc = values["d"] * math.sin(theta_rad)
            dx = validate_assign(dx_calc, values["dx"], "dx", "d and theta")
            dy = validate_assign(dy_calc, values["dy"], "dy", "d and theta")

        else:
            dx = values["dx"]
            dy = values["dy"]

        if values["a"] is not None:
            ax_calc = values["a"] * math.cos(theta_rad)
            ay_calc = values["a"] * math.sin(theta_rad)
            ax = validate_assign(ax_calc, values["ax"], "ax", "a and theta")
            ay = validate_assign(ay_calc, values["ay"], "ay", "a and theta")
        else:
            # Use direct component values if provided
            ax = values["ax"]
            ay = values["ay"]

    # If no theta, use the given component values
    else:
        vix = values["vix"]
        viy = values["viy"]
        vfx = values["vfx"]
        vfy = values["vfy"]
        dx = values["dx"]
        dy = values["dy"]
        ax = values["ax"]
        ay = values["ay"]

    xvalues = {
        "vi": vix,
        "vf": vfx,
        "a": ax,
        "d": dx,
        "t": values["t"], }
    yvalues = {
        "vi": viy,
        "vf": vfy,
        "a": ay,
        "d": dy,
        "t": values["t"], }
    oneDvalues = {
        "vi": values["vi"],
        "vf": values["vf"],
        "a": values["a"],
        "d": values["d"],
        "t": values["t"], }

    vi, vf, a, d,  = sympy.symbols("vi vf a d")  # define objects
    t = sympy.symbols("t", positive=True)
    # dict that maps string to the objects.
    variable_symbols = {"vi": vi, "vf": vf, "a": a, "t": t, "d": d}

    # decide whether to use x or y dicts
    if values["solve"] in ["vix", "vfx", "ax", "dx"]:
        workingvalues = xvalues
        solvevar = values["solve"][:-1]  # remove "x", go from "vix" -> "vi"
    elif values["solve"] in ["viy", "vfy", "ay", "dy"]:
        workingvalues = yvalues
        solvevar = values["solve"][:-1]  # remove the 'y
    elif values["solve"] == "t":
        # compare which direction has fewer unknowns
        nonevalues = None
        allvaluesx = list(xvalues.values())
        allvaluesy = list(yvalues.values())
        allvalues = list(oneDvalues.values())
        nonecountx = allvaluesx.count(nonevalues)
        nonecounty = allvaluesy.count(nonevalues)
        nonecount1D = allvalues.count(nonevalues)

        if nonecount1D <= nonecountx and nonecount1D <= nonecounty:
            workingvalues = oneDvalues
        elif nonecountx < nonecounty:
            workingvalues = xvalues
        else:
            workingvalues = yvalues
        solvevar = "t"
    else:
        # For 1D variables without x/y
        workingvalues = oneDvalues
        solvevar = values["solve"]
    # define equationss
    one = sympy.Eq(d, vi*t+0.5*a*t**2)
    two = sympy.Eq(vf, vi + a*t)
    three = sympy.Eq(vf**2, vi**2+2*a*d)
    four = sympy.Eq(d, (vi+vf)/2*t)
    equations = [one, two, three, four]  # create a list with equations
    target = variable_symbols[solvevar]  # convert the string variable ur solving for into symbol
    print(f"Working values: {workingvalues}")
    print(f"Solving for: {solvevar}")

    for equation in equations:  # for each eqauation
        if target in equation.free_symbols:  # if target is in the equation
            # If all values are present, for each symbol in the equation (except for target)
            if all(workingvalues[str(s)] is not None for s in equation.free_symbols if s != target):
                sub = {}  # substitute values floats into variable_symnols
                for key, value in workingvalues.items():
                    if key in variable_symbols and value is not None:
                        sub[variable_symbols[key]] = value
                solved = sympy.solve(equation.subs(sub), target)
                if target == t:
                    solved = [s for s in solved if s.is_real and s >= 0]
                return solved, equation
            else:
                continue
    return (None, None)


def get_units(values):
    match values["solve"]:
        case "a" | "ax" | "ay":
            return "m/s^2"
        case "vf" | "vfx" | "vfy":
            return "m/s"
        case "vi" | "vix" | "viy":
            return "m/s"
        case "d" | "dx" | "dy":
            return "m"
        case "t":
            return "s"
        case _:
            return "NONE"


if __name__ == "__main__":
    main()
