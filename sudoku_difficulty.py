from __future__ import print_function
from grid_tmp import *
from Solver_difficulty import *
import os
import copy

class Sudoku_Problem:
    def __init__(self):
        '''
        Constructor
        '''
        self.neighbours = dict()
        self.add_neighbours()
        self.constraints=[]
        self.generate_constraints()
        self.max_d_size=9

    def add_neighbours(self):
        '''
        Function to generate the neighbor table
        ----
        '''
        for i in range(9):
            for j in range(9):
                self.neighbours[9*i+j] = self.get_neighbours(i,j) 
        
    def get_neighbours(self, g_x, g_y):
        '''
        Function to get the neighbors of a variable
        ---
        Args:
        @g_x: The row number of the variable (0-8)
        @g_y: The column number of the variable (0-8)
        '''
        ## elements in the same row
        g_x_neighbours = [9*g_x + x for x in range(0,9) if x != g_y]
        ## elements in the same column
        g_y_neighbours = [9*x + g_y for x in range(0,9) if x != g_x]
        ## elements in the same box
        box_n = []
        x_base = int(g_x/3) * 3
        y_base = int(g_y/3) * 3
        for i in range(3):
            for j in range(3):
                box_n.append(9*(x_base + i) + y_base + j)

        neighbours = list(set(g_x_neighbours + g_y_neighbours + box_n))
        neighbours.remove(9*g_x + g_y)
        neighbours.sort()
        return neighbours

    def generate_constraints(self):
        '''
        Function to generate all the constraints
        ---
        '''
        
        for x in range(9):
            self.constraints.append([9*x+y for y in range(0,9)])
        for y in range(9):
            self.constraints.append([9*x+y for x in range(0,9)])
        for x in (0,3,6):
            for y in range(0,3,6):
                box_n = []
                x_base = x
                y_base = y
                for i in range(3):
                    for j in range(3):
                        box_n.append(9*(x_base + i) + (y_base + j))
                self.constraints.append(box_n)
        
    def is_consistent(self,var,assignment,table):
        '''
        Function to check if the current assignment to variable var is consistent
        ---
        Args:
        @var: The variable whose consistency needs to be checked
        @assignment: The current assignment
        '''
        ## This function is to be used only when we know that the variable has been fixed to one value
        def check(x,y):
            x_value = -1
            for j in range(0,9):
                if assignment[9*x + j] == 0:
                    x_value = j + 1
                    break

            for j in range(0,9):
                if assignment[9*y + j] == 0:
                    return x_value == j+1
            return False

        def compare(x, y):
            return table[x] == 1 and (check(x,y) == True)

        def remove(x,val):
            if assignment[x*9+val-1]==0:
                assignment[x*9+val-1]=1
                table[x]-=1

        # Get the value assigned to variable var
        var_value=0
        for i in range(9):
            if assignment[var*9+i]==0:
                var_value=i+1
                break

        for x in self.neighbours[var]:
            remove(x,var_value)
            if table[x]==0:
                return False
        return True
    
    def print_sudoku(self, assignment):
        '''
        Function to print the sudoku grid
        ---
        Args:
        @assignment: The current values of the squares
        '''
        
        for i in range(81):
            if i%9 == 0:
                print("\n")
            elif i%3 == 0 :
                print("|", end="")
            if i%27 == 0:
                for k in range(20):
                    print("-",end="")
                print()
            for j in range(9):
                if assignment[9*i +j] == 0:
                    print(str(j+1) + " ", end="")
                    break
        print("")
             

   
    def print_sudoku_debug(self, assignment):
        '''
        Function to print the sudoku grid
        ---
        Args:
        @assignment: The current values of the squares
        '''
        
        for i in range(81):
            if i%9 == 0:
                print("\n")
            elif i%3 == 0 :
                print("|", end="")
            if i%27 == 0:
                for k in range(20):
                    print("-",end="")
                print()
            values = list()
            for j in range(9):
                if assignment[9*i +j] == 0:
                    values.append(j+1)
                    #print(str(j+1) + " ", end="")
            print(''.join([str(x) for x in values]), end="")
            print(" ", end="")
        print("\n------------------------------------------------------------------")
             

                
    def is_valid(self,assignment,table):
        '''
        Function to check if the sudoku assignment is valid
        ---
        Args:
        @assignment: The current assignment
        @table: table containing the lengths of the domains of every variable
        '''
        for constraint in self.constraints:
            used_digits = list() 
            for var in constraint:
                if table[var] > 1:
                    return False

                x_value = 0
                for j in range(0,9):
                    if assignment[9*var + j] == 0:
                        x_value = j + 1
                        break

                if x_value in used_digits:
                    return False
                used_digits.append(x_value)                
        return True

    def get_difficulty(self, inference_count, output_file, puzzle,ng, blank_count):
        output_string = puzzle + " "
        output_string += str(inference_count['ac-three']) + " "
        output_string += str(inference_count['unique-candidate']) + " "
        output_string += str(inference_count['naked-pair']) + " "
        output_string += str(inference_count['hidden-pair']) + " "
        output_string += str(inference_count['x-wing']) 

        output_file.write(output_string + " " + str(ng) + " " + str(blank_count) + "\n")

#########################################################################################
####################################### MAIN ############################################
#########################################################################################

def main():
    sudoku=Sudoku_Problem()
    solver=Solver()
    directory='optional/sudoku'
    is_assigned=[False]*729

    strategies=dict()
    strategies['use_mrv']=True
    strategies['use_ac3']=True
    strategies['use_unique_cand']=True
    strategies['use_naked_pair']=True
    strategies['use_hidden_pair']=True
    strategies['use_waterfall_preprocess']=True
    strategies['use_xwing'] = True

    output_file = open('output', 'w')

    # grid=Grid('in/26.sudoku')
    # solver.ac_three_begin(grid.grid, sudoku, grid.table)
    # solver.onlyPlaceForValue(sudoku, grid.grid, grid.table)
    # assignment,ng=solver.backtracking_search(grid.grid,sudoku,True,grid.table,is_assigned)
    # print("Guesses = ",ng)
    # sudoku.print_sudoku(assignment)
    # print("\n")

    for filename in os.listdir(directory):
        print(" ------------------------------------ "+filename+" -------------------------------------")

        solver.reset()

        grid=Grid(os.path.join(directory,filename))
        
        grid_copy = copy.deepcopy(grid)
        
        blank_count = len([x for x in grid.table if grid.table[x] > 1])

        if strategies['use_waterfall_preprocess']:
            solver.inference(grid.grid, sudoku, grid.table,strategies)
        is_assigned=[False]*729

        assignment,ng=solver.backtracking_search(grid.grid,sudoku,strategies,grid.table,is_assigned)

        print("Guesses = ",ng)

        sudoku.print_sudoku(assignment)

        sudoku.get_difficulty(solver.inference_use_count, output_file, filename, ng, blank_count)
                
    output_file.close()

if __name__== "__main__":
    main()
