# Sudoku Solver using Constraint Satisfaction

### Authors: Abhay Mittal and Anirudh Sabnis

## Description of Files
- grid.py: File containing code for a sudoku grid
- sudoku.py: File containing code for defining sudo as a CSP and the MAIN function
- Solver.py: File containing implementations of backtracking search, MRV and inference methods

- grid_tmp.py: This file contains parser for reading the optional dataset grids
- sudoku_optional.py: File containing code for Optional sudoku problem (determining difficulty). Mainly added a get_difficulty() function and changed the main function.
- Solver_optional.py: File containing code for Optional problem. This file contains modifications to inference methods.  Major changes include addition of an inference count which counts the number of domain reductions made by each inference.
- optional_dataset/: The dataset used for optional problem
- in/: The puzzles provided

Note: directory in/ contains all the sudoku inputs

## Steps to run
- Enter in terminal `python sudoku.py`. The program takes puzzles in the in/ directory as input
- For the optional problem, please refer to the files Solver_optional.py, sudoku_optional.py
- To run the optional problem, input `python sudoku_optional.py`
