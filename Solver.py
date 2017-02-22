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

    
                        
