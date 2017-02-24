from grid import *
from Solver import *
import os
class Sudoku_Problem:
    def __init__(self):
        self.neighbours = dict()
        self.add_neighbours()
        self.constraints=[]
        self.generate_constraints()
        self.max_d_size=9

    def add_neighbours(self):
        for i in range(9):
            for j in range(9):
                self.neighbours[str(i) + str(j)] = self.get_neighbours(i,j)
        
    def get_neighbours(self, g_x, g_y):
        ## elements in the same row
        g_x_neighbours = [str(g_x) + str(x) for x in range(0,9) if x != g_y]
        ## elements in the same column
        g_y_neighbours = [str(x) + str(g_y) for x in range(0,9) if x != g_x]
        ## elements in the same box
        box_n = []
        x_base = int(g_x/3) * 3
        y_base = int(g_y/3) * 3
        for i in range(3):
            for j in range(3):
                box_n.append(str(x_base + i) + str(y_base + j))
        box_n.remove(str(g_x) + str(g_y))
        neighbours = list(set(g_x_neighbours + g_y_neighbours + box_n))
        neighbours.sort()
        # print "Neighbors "+str(g_x) + str(g_y)+ " => ",neighbours
        return neighbours

    def generate_constraints(self):
        '''
        Function to generate all the constraints
        '''
        for x in range(9):
            self.constraints.append([str(x) + str(y) for y in range(0,9)])
        for y in range(9):
            self.constraints.append([str(x) + str(y) for x in range(0,9)])
        for x in (0,3,6):
            for y in range(0,3,6):
                box_n = []
                x_base = x
                y_base = y
                for i in range(3):
                    for j in range(3):
                        box_n.append(str(x_base + i) + str(y_base + j))
                self.constraints.append(box_n)
        return
        

    def is_consistent(self,var,assignment):
        '''
        Function to check if the current assignment to variable var is consistent
        ---
        Args:
        @var: The variable whose consistency needs to be checked
        @assignment: The current assignment
        '''
        for x in self.neighbours[var]:
            if assignment[x] == assignment[var]:
                return False
        return True
    
    def is_valid(self,assignment):
        for constraint in self.constraints:
            used_vals=dict()
            for var in constraint:
                if assignment[var]=='-' or len(assignment[var])>1:
                    return False
                if  assignment[var][0] in used_vals and used_vals[assignment[var][0]] is True:
                    return False
                used_vals[assignment[var][0]]=True
                
        return True

    def print_grid(self,grid):
        print "-----------------------------------------"
        for i in range(9):
            print "|",
            for j in range(9):
                key=str(i)+str(j)
                print str(grid[key][0])+"|",
            print ""
            print "-------------------------------------"
        return
                

#########################################################################################
####################################### MAIN ############################################
#########################################################################################

def main():
    sudoku=Sudoku_Problem()
    solver=Solver()
    directory='in'

    grid=Grid('in/10.sudoku')
    assignment,ng=solver.backtracking_search(grid.grid,sudoku,True)
    print "Guesses = ",ng
    print sudoku.print_grid(assignment)
    

    # for filename in os.listdir(directory):
    #     print " ------------------------------------ "+filename+" -------------------------------------"
    #     grid=Grid(os.path.join(directory,filename))
    #     assignment,ng=solver.backtracking_search(grid.grid,sudoku,False)
    #     print "Guesses = ",ng
    #     print sudoku.print_grid(assignment)

if __name__== "__main__":
    main()
