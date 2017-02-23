from queue import *

class Solver:

    def __init__(self):
        return
    
    def backtracking_search(self,assignment,csp):
        '''
        Implementation for backtracking search
        ---
        Args:
        @assignment: assignment
        @csp: the constraint satisfaction problem
        '''
        if csp.is_valid(assignment):
            return assignment
        

        var=self.select_unassigned_variable(assignment,csp)

        for value in self.order_domain_values(var,assignment,csp):
            var_domain=assignment[var]
            assignment[var]=[value]
            if csp.is_consistent(var,assignment):
                self.ac_three(assignment, csp, var)
                result=self.backtracking_search(assignment,csp)
                if result is not False:
                    return result
            assignment[var]=var_domain
        return False

            
    def select_unassigned_variable(self,assignment,csp):
        '''
        Function to implement Variable Ordering
        ---
        Args:
        @assignment: the current assignment of all variables
        @csp: the constraint satisfaction problem
        '''

        for var in assignment:
            if len(assignment[var])>1:
                return var
        return None
    
        # Implement the MRV heuristic
        # mrv_var=None
        # min_len=csp.max_d_size+1 # min_len can not be more than  max domain size 
        # for var in assignment:
        #     if len(assignment[var])>1 and min_len>len(assignment[var]):
        #         min_len=len(assignment[var])
        #         mrv_var=var

        # return mrv_var

    def order_domain_values(self,var,assignment,csp):
        '''
        Function which returns an ordering of values of variable var according to some heuristic
        ---
        Args:
        @var: The variable whose values have to be ordered
        @assignment: The current assignment
        @csp: The constraint satisfaction problem
        '''

        return assignment[var]

    def ac_three(self, assignment, csp, var):
        q = Queue()
        
        for i in csp.neighbours[var]:
            q.put((var, i))

        while q.empty() == False:
            v_pair = q.get()
            if self.revise(csp, v_pair, assignment) == True:
                if len(assignment[v_pair[0]]) == 0:
                    return False                
        return True
        
    def revise(self,csp, v_pair, assignment):
        revised = False
        d_j = assignment[v_pair[1]]
        if len(d_j) == 1 and d_j[0] in assignment[v_pair[0]]:
            assignment[v_pair[0]].remove(d_j[0])
            revised = True
        return revised
                        
