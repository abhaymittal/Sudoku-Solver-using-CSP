from __future__ import print_function
from grid import *
from Solver import *
import os

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
        Function to check if the current assignment to variable var is consistent. It also does forward checking for the variable
        ---
        Args:
        @var: The variable whose consistency needs to be checked
        @assignment: The current assignment
        '''

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

        # Remove the assigned value from the neighbors
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
        Function to print the sudoku grid in its intermediate state
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
    

#########################################################################################
####################################### MAIN ############################################
#########################################################################################

def main():
    print_sudoku=False
    sudoku=Sudoku_Problem()
    solver=Solver()
    directory='in'
    is_assigned=[False]*729

    strategies=dict()
    strategies['use_mrv']=True
    strategies['use_ac3']=True
    strategies['use_unique_cand']=True
    strategies['use_naked_pair']=True
    strategies['use_hidden_pair']=False
    strategies['use_waterfall_preprocess']=True
    strategies['use_xwing']=True

    ############ PLAIN BACKTRACK ################
    print("PLAIN BACKTRACK")
    print("Puzzle # | #Guesses")
    strategies['use_mrv']=False
    strategies['use_ac3']=False
    strategies['use_unique_cand']=False
    strategies['use_naked_pair']=False
    strategies['use_hidden_pair']=False
    strategies['use_waterfall_preprocess']=False
    strategies['use_xwing']=False
    for filename in os.listdir(directory):
        grid=Grid(os.path.join(directory,filename))
        is_assigned=[False]*729
        assignment,ng=solver.backtracking_search(grid.grid,sudoku,strategies,grid.table,is_assigned)
        print(filename, " | ",ng)
        if print_sudoku:
            sudo.print_sudoku(assignment)

    ############ MRV ONLY #######################
    print("________________________________________________________________")
    print ("MRV Heuristic")
    print("Puzzle # | #Guesses")
    strategies['use_mrv']=True
    strategies['use_ac3']=False
    strategies['use_unique_cand']=False
    strategies['use_naked_pair']=False
    strategies['use_hidden_pair']=False
    strategies['use_waterfall_preprocess']=False
    strategies['use_xwing']=False
    for filename in os.listdir(directory):
        grid=Grid(os.path.join(directory,filename))
        is_assigned=[False]*729
        assignment,ng=solver.backtracking_search(grid.grid,sudoku,strategies,grid.table,is_assigned)
        print(filename, " | ",ng)
        if print_sudoku:
            sudo.print_sudoku(assignment)

    ############# AC-3 + MRV (No preprocessing) #####
    print("________________________________________________________________")
    print ("AC3 + MRV")
    print("Puzzle # | #Guesses")
    strategies['use_mrv']=True
    strategies['use_ac3']=True
    strategies['use_unique_cand']=False
    strategies['use_naked_pair']=False
    strategies['use_hidden_pair']=False
    strategies['use_waterfall_preprocess']=False
    strategies['use_xwing']=False
    for filename in os.listdir(directory):
        grid=Grid(os.path.join(directory,filename))
        is_assigned=[False]*729
        assignment,ng=solver.backtracking_search(grid.grid,sudoku,strategies,grid.table,is_assigned)
        print(filename, " | ",ng)
        if print_sudoku:
            sudo.print_sudoku(assignment)

    #


    ############ WATERFALL ##########################
    print("________________________________________________________________")
    print ("Waterfall - AC3 + MRV + Unique Candidate + Hidden Pair + X-Wing")
    print("Puzzle # | #Guesses")
    strategies['use_mrv']=True
    strategies['use_ac3']=True
    strategies['use_unique_cand']=True
    strategies['use_naked_pair']=False
    strategies['use_hidden_pair']=True
    strategies['use_waterfall_preprocess']=True
    strategies['use_xwing']=True
    for filename in os.listdir(directory):
        grid=Grid(os.path.join(directory,filename))
        is_assigned=[False]*729
        assignment,ng=solver.backtracking_search(grid.grid,sudoku,strategies,grid.table,is_assigned)
        print(filename, " | ",ng)
        if print_sudoku:
            sudo.print_sudoku(assignment)    

if __name__== "__main__":
    main()
