from sets import *
import copy

class Solver:

    def __init__(self):
        return
    
    def backtracking_search(self,assignment,csp,use_mrv, table):
        '''
        Implementation for backtracking search
        ---
        Args:
        @assignment: assignment
        @csp: the constraint satisfaction problem
        '''
        use_mrv = False
        if csp.is_valid(assignment,table):
            return assignment,0

        [var, n_guesses] = self.select_unassigned_variable(assignment,csp,use_mrv,table)

        var_state = self.order_domain_values(var, assignment, csp)

        domain_length = table[var]
        table[var] = 1

        for value in var_state:
            assign_copy = copy.deepcopy(assignment)
            start = 9 * var
            for j in range(9):
                if j == value:
                    assign_copy[start + j] = 0
                else :
                    assign_copy[start + j] = 1
            
            if csp.is_consistent(var,assign_copy,table):

                result,ng=self.backtracking_search(assign_copy,csp,use_mrv,table)

                if result is not False:
                    n_guesses=n_guesses+ng
                    return result,n_guesses

        table[var] = domain_length
        return False,0

            
    def select_unassigned_variable(self,assignment,csp,use_mrv,table):
        '''
        Function to implement Variable Ordering
        ---
        Args:
        @assignment: the current assignment of all variables
        @csp: the constraint satisfaction problem
        '''
        if not use_mrv:
            for i,j in enumerate(table):
                if j >= 2:
                    return [i, j-1]
            return None
        else:
            pass

        # Implement the MRV  heuristic
#             mrv_var=None
#             min_len=csp.max_d_size+1 # min_len can not be more than  max domain size 
#             for var in assignment:
#                 if len(assignment[var])>1 and min_len>len(assignment[var]):
#                     min_len=len(assignment[var])
#                     mrv_var=var
#             return mrv_var

    def order_domain_values(self,var,assignment,csp):
        '''
        Function which returns an ordering of values of variable var according to some heuristic
        ---
        Args:
        @var: The variable whose values have to be ordered
        @assignment: The current assignment
        @csp: The constraint satisfaction problem
        '''
        domain_vals = list()
        start = 9 * var
        for j in range(9):
            if assignment[start + j] == 0:
                domain_vals.append(j)
        return domain_vals            
        #return assignment[var]

    def inference(self,assignment,csp,var):
        '''
        Function to do the inferences over current assignment
        ---
        Args:
        @assignment: The current assignment
        @csp: The constraint satisfaction problem
        @var: The variable to which value was assigned
        '''
        res=self.ac_three(assignment,csp,var) # do ac3
        return res

    def ac_three(self, assignment, csp, var):
        q = set()
        
        for i in csp.neighbours[var]:
            q.add((i, var))

        while len(q)>0:
            v_pair = q.pop()
            if self.revise(csp, v_pair, assignment):
                if len(assignment[v_pair[0]]) == 0:
                    return False
                for xk in csp.neighbours[v_pair[0]]:
                    if xk != v_pair[1]:
                        ### Only add here if xk has domain of size 1
                        q.add((xk,v_pair[0]))
        return True
        
    def revise(self,csp, v_pair, assignment):
        revised = False
        d_j = assignment[v_pair[1]]
        #print "D_j = ",d_j
        if len(d_j) == 1 and d_j[0] in assignment[v_pair[0]]:
            assignment[v_pair[0]].replace(d_j[0],"")
            revised = True
        return revised
                        

