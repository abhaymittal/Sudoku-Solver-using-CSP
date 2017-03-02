from sets import *
import copy

class Solver:

    def __init__(self):
        self.inference_use_count = dict()
        self.reset()

    def reset(self):
        self.inference_use_count['ac-three'] = 0
        self.inference_use_count['unique-candidate'] = 0
        self.inference_use_count['naked-pair'] = 0
        self.inference_use_count['hidden-pair'] = 0
        self.inference_use_count['x-wing'] = 0
   
    def backtracking_search(self,assignment,csp,strategies, table,is_assigned):
        '''
        Implementation for backtracking search
        ---
        Args:
        @assignment: assignment
        @csp: the constraint satisfaction problem
        '''
        if csp.is_valid(assignment,table):
            return assignment,0

        [var, n_guesses] = self.select_unassigned_variable(assignment,csp,strategies,table,is_assigned)

        if var is None:
            return False,0

        is_assigned[var]=True

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
                if self.inference(assign_copy,csp,table_copy,strategies):
                    result,ng=self.backtracking_search(assign_copy,csp,strategies,table_copy,is_assigned)
                    n_guesses=n_guesses+ng

                    if result is not False:
                        return result,n_guesses

        is_assigned[var]=False
        table[var] = domain_length

        return False,n_guesses

            
    def select_unassigned_variable(self,assignment,csp,strategies,table,is_assigned):
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
        if not strategies['use_mrv']:
            for i,j in enumerate(table):
                if not is_assigned[i]:
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

    def inference(self,assignment,csp,table,strategies):
        '''
        Function to do the inferences over current assignment
        ---
        Args:
        @assignment: The current assignment
        @csp: The constraint satisfaction problem
        @var: The variable to which value was assigned
        @table: Array containing the domain size of each variable
        '''

        changed=True
        while(changed):
            if strategies['use_ac3']:
                res,changed=self.ac_three_begin(assignment,csp,table) # do ac3
            else:
                res=True
                changed=False

            if strategies['use_unique_cand']:
                res2,changed2=self.unique_candidate(csp, assignment, table)
            else:
                res2=True
                changed=False

            if strategies['use_naked_pair']:
                res3,changed3 = self.naked_pair(csp, assignment, table)
            else:
                res3=True
                changed3=False

            if strategies['use_hidden_pair']:
                res4, changed4 = self.hidden_pair(csp, assignment, table)
            else:
                res4=True
                changed4=False
                
            if strategies['use_xwing']:
                res5,changed5=self.x_wing(csp,assignment,table)
            else:
                res5=True
                changed5=False

            res = res and res2  and res3 and res4 and res5
            changed=changed or changed2  or changed3 or changed4 or changed5

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

            [res, count] = self.revise(csp, v_pair, assignment,table)

            if res == True:
                changed_flag=True

                if table[v_pair[0]] == 0:
                    return False,changed_flag

                self.inference_use_count['ac-three'] += count

                for xk in csp.neighbours[v_pair[0]]:
                    if xk != v_pair[1]:
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
        domain_changed = False
        q = set()

        for c in csp.constraints:
            for var1 in c:
                for var2 in c:
                    if var1 != var2 :
                        q.add((var1, var2))

        while len(q)>0:
            v_pair = q.pop()

            [res, count] = self.revise(csp, v_pair, assignment,table)

            if res == True:
                domain_changed = True

                if table[v_pair[0]] == 0:
                    return False, domain_changed

                self.inference_use_count['ac-three'] += count

                for xk in csp.neighbours[v_pair[0]]:
                    if xk != v_pair[1]:
                        q.add((xk,v_pair[0]))

        return True, domain_changed
    

    def revise(self,csp, v_pair, assignment,table):
        changed_count = 0

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
                    changed_count += 1

        return revised, changed_count

    def unique_candidate(self, csp, assignment, table):
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
                    self.inference_use_count['unique-candidate'] += 1

                    for i in range(9):
                        if i != value:
                            assignment[9*val_placed_in[0] + i] = 1

                    res,chn=self.ac_three(assignment, csp, val_placed_in[0],table)

                    if res == False:
                        return False,changed_flag or chn

        return True,changed_flag

    def hidden_pair(self, csp, assignment, table):
        ## In every constraint
        ## For every pair of values, if they are allowed in only two cells
        ## Reduce the domain of the two cells to the two values
        ## And Call other domain reduction strategies, this should be taken care of in the waterfall
        domain_reduced = False

        def getVariables(c, val):
            var_list = []
            for var in c:
                if assignment[var*9 + val] == 0:
                    var_list.append(var)
            return var_list

        def remove(vars, val1, val2):
            for val in range(9):
                if val != val1 and val != val2:
                    for var in vars:
                        if assignment[9*var + val] == 0:
                            assignment[9*var + val] = 1
                            table[var] = table[var] - 1
                            domain_reduced = True
                            self.inference_use_count['hidden-pair'] += 1

        for c in csp.constraints:
            for val1 in range(9):
                val1_variables = getVariables(c, val1)

                for val2 in range(val1 + 1, 9):
                    val2_variables = getVariables(c, val2)
                    intersection = []

                    if val1_variables == val2_variables and len(val1_variables) == 2:
                        intersection = val1_variables

                    if len(intersection) == 2:
                        remove(intersection, val1, val2)

        return True,domain_reduced
                    
    def naked_pair(self, csp, assignment, table):
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
                        self.inference_use_count['naked-pair'] += 1

                    if assignment[9* var + domain[1]] == 0:
                        changed_flag=True
                        assignment[9* var + domain[1]] = 1
                        table[var] = table[var] - 1
                        self.inference_use_count['naked-pair'] += 1

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


    def x_wing(self,csp,assignment,table):
        '''
        Function implementing the X Wing strategy
        ---
        Args:
        @csp: The sudoku csp
        @assignment: The current assignment to variables
        @table: A list containing the domain size of all variables
        '''
        row_constraints=csp.constraints[0:9]
        col_constraints=csp.constraints[9:18]
        changed_flag=False

        
        #### Search for rectangles in rows
        for i in range(9):
            for j in range(i+1,9):
                val_dict=dict()
                rc1=row_constraints[i]
                rc2=row_constraints[j]
                for digit in range(9):
                    val_dict[digit]=list()
                    occ_row1=0
                    occ_row2=0
                    for col in range(9):
                        if assignment[rc1[col]*9+digit]==0:
                            occ_row1+=1
                        if assignment[rc2[col]*9+digit]==0:
                            occ_row2+=1
                    if occ_row1==2 and occ_row2==2:
                        for col in range(9):
                            if assignment[rc1[col]*9+digit]==0 and assignment[rc2[col]*9+digit]==0:
                                val_dict[digit].append(col)

                for digit in val_dict:
                    if len(val_dict[digit])==2:

                        col1=val_dict[digit][0]
                        col2=val_dict[digit][1]
                        shared_col_var_11=rc1[col1]
                        shared_col_var_12=rc1[col2]
                        shared_col_var_21=rc2[col1]
                        shared_col_var_22=rc2[col2]
                        col1=col_constraints[col1]
                        col2=col_constraints[col2]
                        for var in col1:
                            if var!=shared_col_var_11 and var!=shared_col_var_21:
                                if assignment[var*9+digit]==0:
                                    if table[var]>1:
                                        changed_flag=True
                                        table[var]-=1
                                        assignment[var*9+digit]=1
                                        self.inference_use_count['x-wing'] += 1
                                    else:
                                        table[var]=0
                                        return False,changed_flag
                        for var in col2:
                            if var!=shared_col_var_12 and var!=shared_col_var_22:
                                if assignment[var*9+digit]==0:
                                    if table[var]>1:
                                        changed_flag=True
                                        table[var]-=1
                                        assignment[var*9+digit]=1
                                        self.inference_use_count['x-wing'] += 1
                                    else:
                                        table[var]=0
                                        return False,changed_flag




        #### Search for rectangles in columns
        for i in range(9):
            for j in range(i+1,9):
                val_dict=dict()
                cc1=col_constraints[i]
                cc2=col_constraints[j]
                for digit in range(9):
                    val_dict[digit]=list()
                    occ_col1=0
                    occ_col2=0
                    for row in range(9):
                        if assignment[cc1[row]*9+digit]==0:
                            occ_col1+=1
                        if assignment[cc2[row]*9+digit]==0:
                            occ_col2+=1
                    if occ_col1==2 and occ_col2==2:
                        for row in range(9):
                            if assignment[cc1[row]*9+digit]==0 and assignment[cc2[row]*9+digit]==0:
                                val_dict[digit].append(row)
                                

                for digit in val_dict:
                    if len(val_dict[digit])==2:
                        row1=val_dict[digit][0]
                        row2=val_dict[digit][1]
                        shared_row_var_11=cc1[row1]
                        shared_row_var_12=cc1[row2]
                        shared_row_var_21=cc2[row1]
                        shared_row_var_22=cc2[row2]
                        row1=row_constraints[row1]
                        row2=row_constraints[row2]
                        for var in row1:
                            if var!=shared_row_var_11 and var!=shared_row_var_21:
                                if assignment[var*9+digit]==0:
                                    if table[var]>1:
                                        changed_flag=True
                                        table[var]-=1
                                        assignment[var*9+digit]=1
                                        self.inference_use_count['x-wing'] += 1
                                    else:
                                        table[var]=0
                                        return False,changed_flag
                        for var in row2:
                            if var!=shared_row_var_12 and var!=shared_row_var_22:
                                if assignment[var*9+digit]==0:
                                    if table[var]>1:
                                        changed_flag=True
                                        table[var]-=1
                                        assignment[var*9+digit]=1
                                        self.inference_use_count['x-wing'] += 1
                                    else:
                                        table[var]=0
                                        return False,changed_flag

        return True,changed_flag
                            
                            
                            
