from sets import *
import copy

class Solver:

    def __init__(self):
        return
    
    def backtracking_search(self,assignment,csp,use_mrv):
        '''
        Implementation for backtracking search
        ---
        Args:
        @assignment: assignment
        @csp: the constraint satisfaction problem
        '''
        if csp.is_valid(assignment):
            return assignment,0

        var=self.select_unassigned_variable(assignment,csp,use_mrv)
        n_guesses=len(assignment[var])-1
        for value in self.order_domain_values(var,assignment,csp):
            var_domain=assignment[var]
            assignment[var]=[value]
            if csp.is_consistent(var,assignment):
                assign_copy=copy.deepcopy(assignment)
                inf_result=self.inference(assignment,csp,var)
               # print "Inference = ",inf_result
                if inf_result:
                    result,ng=self.backtracking_search(assignment,csp,use_mrv)
                    if result is not False:
                        n_guesses=n_guesses+ng
                        return result,n_guesses
                assignment = assign_copy
            assignment[var]=var_domain
        return False,0

            
    def select_unassigned_variable(self,assignment,csp,use_mrv):
        '''
        Function to implement Variable Ordering
        ---
        Args:
        @assignment: the current assignment of all variables
        @csp: the constraint satisfaction problem
        '''
        if not use_mrv:
            for var in assignment:
                if len(assignment[var])>1:
                    return var
            return None
        else:
        # Implement the MRV  heuristic
            mrv_var=None
            min_len=csp.max_d_size+1 # min_len can not be more than  max domain size 
            for var in assignment:
                if len(assignment[var])>1 and min_len>len(assignment[var]):
                    min_len=len(assignment[var])
                    mrv_var=var
            return mrv_var

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
        q = Set()
        
        for i in csp.neighbours[var]:
            q.add((i, var))

        while len(q)>0:
            v_pair = q.pop()
            if self.revise(csp, v_pair, assignment):
                if len(assignment[v_pair[0]]) == 0:
                    return False
                for xk in csp.neighbours[v_pair[0]]:
                    if xk != v_pair[1]:
                        q.add((xk,v_pair[0]))
        return True
        
    def revise(self,csp, v_pair, assignment):
        revised = False
        d_j = assignment[v_pair[1]]
        #print "D_j = ",d_j
        if len(d_j) == 1 and d_j[0] in assignment[v_pair[0]]:
            assignment[v_pair[0]].remove(d_j[0])
            revised = True
        return revised
                        

