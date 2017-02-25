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
                #self.neighbours[str(i) + str(j)] = self.get_neighbours(i,j)
                self.neighbours[9*i+j] = self.get_neighbours(i,j) 
        
    def get_neighbours(self, g_x, g_y):
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


        for x in self.neighbours[var]:
            if compare(x,var) == True:
                return False
        return True
    
    def printSudoku(self, assignment):
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
                
                
    def is_valid(self,assignment,table):
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

#     def print_grid(self,grid):
#         print "-----------------------------------------"
#         for i in range(9):
#             print "|",
#             for j in range(9):
#                 key=str(i)+str(j)
#                 print str(grid[key][0])+"|",
#             print ""
#             print "-------------------------------------"
#         return

    

#########################################################################################
####################################### MAIN ############################################
#########################################################################################

def main():
    sudoku=Sudoku_Problem()
    solver=Solver()
    directory='in'

    grid=Grid('in/100.sudoku')
    assignment,ng=solver.backtracking_search(grid.grid,sudoku,True,grid.table)
    print("Guesses = ",ng)
    #print(assignment)
    #print(sudoku.print_grid(assignment))
    sudoku.printSudoku(assignment)
    print("\n")

    # for filename in os.listdir(directory):
    #     print " ------------------------------------ "+filename+" -------------------------------------"
    #     grid=Grid(os.path.join(directory,filename))
    #     assignment,ng=solver.backtracking_search(grid.grid,sudoku,False)
    #     print "Guesses = ",ng
    #     print sudoku.print_grid(assignment)

if __name__== "__main__":
    main()
