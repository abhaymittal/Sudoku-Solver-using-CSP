from sets import *
import copy

class Solver:

    def __init__(self):
        return
    
    def backtracking_search(self,assignment,csp,use_mrv, table,is_assigned):
        '''
        Implementation for backtracking search
        ---
        Args:
        @assignment: assignment
        @csp: the constraint satisfaction problem
        '''
        if csp.is_valid(assignment,table):
            return assignment,0

        [var, n_guesses] = self.select_unassigned_variable(assignment,csp,use_mrv,table,is_assigned)
        # if n_guesses > 0:
        #     csp.print_sudoku_debug(assignment)

        if var is None:
            return False,0
        is_assigned[var]=True

        var_state = self.order_domain_values(var, assignment, csp)

        domain_length = table[var]
        table[var] = 1

        for value in var_state:
            assign_copy = copy.deepcopy(assignment)
            table_copy=copy.deepcopy(table)
            # ia_copy=copy.deepcopy(is_assigned)
            start = 9 * var
            table_copy[var]=1
            for j in range(9):
                if j == value:
                    assign_copy[start + j] = 0
                else :
                    assign_copy[start + j] = 1
            
            if csp.is_consistent(var,assign_copy,table_copy):
                if self.inference(assign_copy,csp,var,table_copy):
                    result,ng=self.backtracking_search(assign_copy,csp,use_mrv,table_copy,is_assigned)
                    n_guesses=n_guesses+ng
                    if result is not False:
                        return result,n_guesses
            # print("Chagne value for ",var)

        is_assigned[var]=False
        table[var] = domain_length
        # print "Backtrack from ",var
        return False,n_guesses

            
    def select_unassigned_variable(self,assignment,csp,use_mrv,table,is_assigned):
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
                if not is_assigned[i]:
                    #print("Return variable with domain size ",i,j)
                    return [i, j-1]
            return None
        else:
        # Implement the MRV  heuristic
            mrv_var=None
            min_len=csp.max_d_size+1 # min_len can not be more than  max domain size
            for i,j in enumerate(table):
                if (not is_assigned[i]) and j < min_len:
                    mrv_var=i
                    min_len=j
            # print("Return variable with domain size ",mrv_var,min_len)
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
        @table: Array containing the domain size of each variable
        '''
        # return True
        changed=True
        while(changed):
            res,changed=self.ac_three(assignment,csp,var,table) # do ac3
            res2,changed2=self.onlyPlaceForValue(csp, assignment, table)
            res3,changed3 = self.pairInConstraint(csp, assignment, table)
            res = res and res2  and res3
            changed=changed or changed2  or changed3
            if not res:
                return False
        return res

    def ac_three(self, assignment, csp, var,table):
        '''
        Function implementing AC3 (MAC version) algorithm
        ---
        Args:
        @assignment: The current assignment
        @csp: The constraint satisfaction problem
        @var: The variable to which value was assigned
        @table: Array containing the domain size of each variable
        '''
        q = set()
        
        for i in csp.neighbours[var]:
            q.add((i, var))
        changed_flag=False
        while len(q)>0:
            v_pair = q.pop()
            if self.revise(csp, v_pair, assignment,table):
                changed_flag=True
                if table[v_pair[0]] == 0:
                    return False,changed_flag
                for xk in csp.neighbours[v_pair[0]]:
                    if xk != v_pair[1]:
                        ### Only add here if xk has domain of size 1
                        q.add((xk,v_pair[0]))
        return True,changed_flag
    
    def ac_three_begin(self, assignment, csp, table):
        '''
        Function implementing AC3 (preprocessing) aglgorithm
        ---
        Args:
        @assignment: The current assignment
        @csp: The constraint satisfaction problem
        @table: Array containing the domain size of each variable
        '''
        q = set()

        for c in csp.constraints:
            for var1 in c:
                for var2 in c:
                    if var1 != var2 :
                        q.add((var1, var2))

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

    def onlyPlaceForValue(self, csp, assignment, table):
        changed_flag=False
        for c in csp.constraints:
            for value in range(9):
                val_placed_in = list()
                for var in c:
                    if assignment[9*var + value] == 0:
                        val_placed_in.append(var)

                if len(val_placed_in) == 1 and table[val_placed_in[0]]>1:
                    table[val_placed_in[0]] = 1
                    changed_flag=True
                    for i in range(9):
                        if i != value:
                            assignment[9*val_placed_in[0] + i] = 1
                    res,chn=self.ac_three(assignment, csp, val_placed_in[0],table)
                    if res == False:
                        return False,changed_flag or chn
        return True,changed_flag
                            
    def pairInConstraint(self, csp, assignment, table):
        ## For each constraint:
        ## Find all variables which have domain size of two : put them in a list
        ## If both the domain are same for a pair, remove the domain from rest of the variables and also from the list
        changed_flag=False
        
        def remove_vars(c, domain, value_pair):
            for var in c:
                if var not in value_pair:
                    if assignment[9* var + domain[0]] == 0:
                        changed_flag=True
                        assignment[9* var + domain[0]] = 1
                        table[var] = table[var] - 1
                    if assignment[9* var + domain[1]] == 0:
                        changed_flag=True
                        assignment[9* var + domain[1]] = 1
                        table[var] = table[var] - 1

        for c in csp.constraints:
            domain_var = dict()
            for var in c:
                key = tuple(self.order_domain_values(var, assignment, table))
                if len(key) == 2:
                    if key not in domain_var :
                        domain_var[key] = list()
                    domain_var[key].append(var)

            for key in domain_var:
                if len(domain_var[key]) == 2:
                    remove_vars(c, key, domain_var[key])
                            
        return True,changed_flag



    # def x_wing(self,csp,assignment,table):
    #     row_constraints=csp.constraints[0:9]
    #     col_constraints=csp.constraints[9:18]
    #     changed_flag=True
    #     #### Search for rectangles in rows
    #     for i in range(9):
    #         for j in range(i+1,9):
    #             val_dict=dict()
    #             rc1=row_constraints[i]
    #             rc2=row_constraints[j]
    #             for digit in range(9):
    #                 val_dict[digit]=list()
    #                 for col in range(9):
    #                     if assignment[rc1[col]*9+digit]==0 and assignment[rc2[col]*9+digit]==0:
    #                         val_dict[digit].append(col)

    #             for digit in val_dict:
    #                 if len(val_dict[digit])==2:
    #                     changed_flag=True
    #                     col1=val_dict[digit][0]
    #                     col2=val_dict[digit][1]
    #                     shared_col_var_11=rc1[col1]
    #                     shared_col_var_12=rc1[col2]
    #                     shared_col_var_21=rc2[col1]
    #                     shared_col_var_22=rc2[col2]
    #                     print("X wing found between row ",rc1,"and ",rc2," and cols ",col1,col2)
    #                     csp.print_sudoku_debug(assignment)
    #                     col1=col_constraints[col1]
    #                     col2=col_constraints[col2]
    #                     for var in col1:
    #                         if var!=shared_col_var_11 and var!=shared_col_var_21:
    #                             if assignment[var*9+digit]==0:
    #                                 if table[var]>1:
    #                                     table[var]-=1
    #                                     assignment[var*9+digit]=1
    #                                 else:
    #                                     table[var]=0
    #                                     print ("return false")
    #                                     return False,changed_flag
    #                     for var in col2:
    #                         if var!=shared_col_var_12 and var!=shared_col_var_22:
    #                             if assignment[var*9+digit]==0:
    #                                 if table[var]>1:
    #                                     table[var]-=1
    #                                     assignment[var*9+digit]=1
    #                                 else:
    #                                     table[var]=0
    #                                     print ("return false")
    #                                     return False,changed_flag




    #     #### Search for rectangles in columns
    #     for i in range(9):
    #         for j in range(i+1,9):
    #             val_dict=dict()
    #             cc1=col_constraints[i]
    #             cc2=col_constraints[j]
    #             for digit in range(9):
    #                 val_dict[digit]=list()
    #                 for row in range(9):
    #                     if assignment[cc1[row]*9+digit]==0 and assignment[cc2[row]*9+digit]==0:
    #                         val_dict[digit].append(row)
                                

    #             for digit in val_dict:
    #                 if len(val_dict[digit]==2):
    #                     changed_flag=True
    #                     row1=val_dict[digit][0]
    #                     row2=val_dict[digit][1]
    #                     shared_row_var_11=cc1[row1]
    #                     shared_row_var_12=cc1[row2]
    #                     shared_row_var_21=cc2[row1]
    #                     shared_row_var_22=cc2[row2]
    #                     print("X wing found between col ",cc1,"and ",cc2," and rows ",row1,row2)
    #                     row1=col_constraints[row1]
    #                     row2=col_constraints[row2]
    #                     for var in row1:
    #                         if var!=shared_row_var_11 and var!=shared_row_var_21:
    #                             if assignment[var*9+digit]==0:
    #                                 if table[var]>1:
    #                                     table[var]-=1
    #                                     assignment[var*9+digit]=1
    #                                 else:
    #                                     table[var]=0
    #                                     return False,changed_flag
    #                     for var in row2:
    #                         if var!=shared_row_var_12 and var!=shared_row_var_22:
    #                             if assignment[var*9+digit]==0:
    #                                 if table[var]>1:
    #                                     table[var]-=1
    #                                     assignment[var*9+digit]=1
    #                                 else:
    #                                     table[var]=0
    #                                     return False,changed_flag

    #     return True,changed_flag
                            
