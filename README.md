# 2D KINEMATHICS

## Description:
This project is an interactive physics problem solver for both 1-dimensional and 2-dimensional kinematics. It allows the user to input known quantities (initial velocity, final velocity, acceleration, displacement, and time) in either total magnitudes, component form (x/y directions), or using launch angles. The program then solves for any specified unknown variable.
The program uses **SymPy** to manipulate and solve the standard kinematic equations:
1. $v_f = v_i + at$
2. $d = v_i t + \frac{1}{2}at^2$
3. $v_f^2 = v_i^2 + 2ad$
4. $d = \frac{v_i + v_f}{2}t$

## Features
- Interactive input for all kinematic variables in multiple forms:
  - Total magnitudes (vi, vf, a, d, t)
  - Component form (vix, viy, vfx, vfy, ax, ay, dx, dy)
  - Launch angle (theta) for projectile motion
- Automatic component decomposition when angle is provided
- Validation to detect conflicts between provided values
- Intelligent equation selection based on available information
- Handles multiple solution scenarios, filtering physically valid results
- Provides error handling for invalid inputs or inconsistent values
- Displays results with appropriate SI units
- Includes comprehensive pytest unit tests

## How it works
1. The program asks the user for each variable (vi, vf, a, d, t).
2. If the variable is unknown, input "?".
3. The user specifies the variable to solve.
4. Validation: The program checks for invalid inputs or contradictions.
5. Equation Selection: The solver automatically picks an equation that includes the target variable and known inputs.
6. Computation: Uses SymPy to substitute known values and solve symbolically.
7. Output: Displays the solution and the equation used, with appropriate units.

## Functions
### `get_values()` – Collects input from the user for all kinematic variables
1. Prompts for theta (launch angle in degrees) and all velocity, acceleration, displacement, and time values.
2. If a value is unknown, the user must input "?", which the function stores as `None`.
3. Validates that inputs are either numbers or "?".
4. Validates that the variable to solve for is not already given.
5. Validates that the variable to solve for is in the allowed list: (vi, vf, vix, viy, vfx, vfy, a, ax, ay, d, dx, dy, t).
6. Returns a dictionary containing all user inputs.

### `get_result(values)` – Computes the solution for the target variable
1. **Component Processing:**
   - If theta is provided, decomposes total values (vi, vf, a, d) into x and y components using trigonometry.
   - Uses `validate_assign()` helper function to check for conflicts between calculated components and directly provided components.
   - If theta is not provided or total values are missing, uses direct component inputs.
2. **Dictionary Selection:**
   - Creates three working dictionaries: `xvalues` (x-direction), `yvalues` (y-direction), and `oneDvalues` (1D total values).
   - Selects the appropriate dictionary based on what the user is solving for and which direction has the most information.
3. **Equation Solving:**
   - Defines symbolic variables using SymPy.
   - Iterates through the four kinematic equations to find one with the target variable and all other required variables known.
   - Substitutes known values and solves for the target.
   - Filters out negative or complex time solutions.
4. Returns the solution(s) and the equation used, or `(None, None)` if insufficient information is provided.

### `validate_assign(calc, given, name, source)` – Helper function for conflict detection
1. Compares a calculated component value (from theta decomposition) with a directly provided value.
2. If both exist and differ by more than 0.01, exits with an error message indicating the conflict.
3. Returns the appropriate value to use (prioritizes direct input if calculated value doesn't exist).


### <code>get_units(values)</code> – This function determines the appropriate SI unit for the variable being solved:
- vi or vf → meters per second (m/s)
- a → meters per second squared (m/s²)
- d → meters (m)
- t → seconds (s)
- Returns the corresponding unit as a string, which is used for display in the output.

### <code>main()</code> – main program flow of the solver
1. Calls <code>get_values()</code> to collect and validate user input.
2. Calls <code>get_units()</code> to determine the correct units for the solution.
3. Calls <code>get_result()</code> to compute the solution for the target variable.
4. Prints the equation used and the solution(s) with appropriate units.
5. If <code>get_results</code> returns none, the program prints "No solution Found."

### Files
- project.py – Main solver program.
- test.py – Pytest unit tests for all core functions.
- requirements.txt – Any pip-installable libraries that the project requires (SymPy).
### Requirements
- Python 3.10+
- SymPy 1.14.0
- Pytest (for testing)

