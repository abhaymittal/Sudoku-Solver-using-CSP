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
        if csp.is_valid(assignment,table):
            return assignment,0

        [var, n_guesses] = self.select_unassigned_variable(assignment,csp,use_mrv,table)

        var_state = self.order_domain_values(var, assignment, csp)

        domain_length = table[var]
        table[var] = 1

        for value in var_state:
            assign_copy = copy.deepcopy(assignment)
            table_copy=copy.deepcopy(table)
            start = 9 * var
            table_copy[var]=1
            for j in range(9):
                if j == value:
                    assign_copy[start + j] = 0
                else :
                    assign_copy[start + j] = 1
            
            if csp.is_consistent(var,assign_copy,table_copy):
                if self.inference(assign_copy,csp,var,table_copy):
                    result,ng=self.backtracking_search(assign_copy,csp,use_mrv,table_copy)
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
        ---
        Returns:
        Desired variable
        Number of guesses
        '''
        if not use_mrv:
            for i,j in enumerate(table):
                if j >= 2:
                    return [i, j-1]
            return None
        else:
        # Implement the MRV  heuristic
            mrv_var=None
            min_len=csp.max_d_size+1 # min_len can not be more than  max domain size
            for i,j in enumerate(table):
                if j>1 and j < min_len:
                    mrv_var=i
                    min_len=j
            return mrv_var,min_len-1

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

    def inference(self,assignment,csp,var,table):
        '''
        Function to do the inferences over current assignment
        ---
        Args:
        @assignment: The current assignment
        @csp: The constraint satisfaction problem
        @var: The variable to which value was assigned
        '''
        res=self.ac_three(assignment,csp,var,table) # do ac3
        return res

    def ac_three(self, assignment, csp, var,table):
        q = set()
        
        for i in csp.neighbours[var]:
            q.add((i, var))
        
        while len(q)>0:
            v_pair = q.pop()
            if self.revise(csp, v_pair, assignment,table):
                if table[v_pair[0]] == 0:
                    return False
                for xk in csp.neighbours[v_pair[0]]:
                    if xk != v_pair[1]:
                        ### Only add here if xk has domain of size 1
                        q.add((xk,v_pair[0]))
        return True
        
    def revise(self,csp, v_pair, assignment,table):
        revised = False
        d_j = assignment[v_pair[1]]
        start_1=v_pair[1]*9
        start_0=v_pair[0]*9
        if table[v_pair[1]]==1:
            for i in range(9):
                if assignment[start_0+i] == 0 and assignment[start_1+i]==0:
                    assignment[start_0+i]=1
                    table[v_pair[0]]=table[v_pair[0]]-1
                    revised=True
        return revised
                        

