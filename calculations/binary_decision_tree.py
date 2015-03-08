test = "trees are connected"


#######################################################################

# SCENARIO RESULTS -- tied to the leaves of the binary decision tree.

msg_condition_results = {
    1: "Your customers complain about lossing energy on a normal basis, and the electric grid tends to go dark during heat waves.  Also, your company is being charged by the state for failing their renewables target.",
    2: "Your customers lose power during normal days and heat waves, but at least you have made your renewables target to help the environment!",
    3: "Your electric grid doesn't have enough energy to function on most days, but has too much energy during sunny heat waves -- causing local areas in the grid to melt down (e.g. voltage flux).",
    4: "You definitely keep the lights on for your customers, during both the normal days and the hot ones.  However, your environmental foresight is lacking and your grandchildren have asthma.",
    5: "You have hit your environmental goals, while keeping the lights on during both normal days and heat waves.  Congratulations!  You should apply to be a utility CEO!",
    6: "Your customers have energy most days, and your renewable targets are awesome.   However, during intense heat waves the excess sunny energy may cause voltage fluctuations.  (Congrats...you have melted your distribution grid.)"
}


####################################################################

# MAKE NODES for the binary decision tree.


class Node(object):

    def __init__(self, left=None, right=None, threshold=None, fuel_type=None, msg=None):
        assert left is None or isinstance(left, Node)
        assert right is None or isinstance(right, Node)
        self.fuel_type = fuel_type     # what fuel type will be tested
        self.threshold = threshold      # what the threshold is for the test
        self.left = left    # this is the left child
        self.right = right    # this is the right child
        self.msg = msg


    def __repr__(self):
        """Return debugging-friendly representation of node."""
        return "<BDT_Node.  msg: %s >" % (self.msg)


    def testing_condition(self, condition_dict):
        current_node = self
        if current_node.left==None and current_node.right==None: # no children
            # print "hit line 35. \n  node:", current_node
            return current_node.msg
        if condition_dict[current_node.fuel_type] <= current_node.threshold:
            # print "hit line 38. \n  node:", current_node
            current_node = current_node.left
            return current_node.testing_condition(condition_dict)
        if condition_dict[current_node.fuel_type] > current_node.threshold:
            # print "hit line 42. \n  node:", current_node
            current_node = current_node.right
            return current_node.testing_condition(condition_dict)


        ## LESSON LEARNED.  recursion makes another instance of this function, and pauses (yield?) the original function.  Will return to the original function afterwards.
        ##  so using this return below, will overwrite the return current_node.msg above.  Since return in recursion just ends the current recursive function, but DOES NOT END earlier versions of this function called!
        # return "Error in binary decision tree"

        ## LESSON LEARNED.  since recursive functions which return the result (self.msg), then return to continue the idled functions started earlier....the return result will be overwritten.  therefore, need to call the recursive function be "return recursive_function(self,params)".  so final return function, returns to the previos function which was puased, which returns to the previos function pasued, etc up the tree.


##################################################################

# BUILD THE TREE!

# leaves are the resultant decisions.  msg is pulled from dict of msg_condition_results.
bdt_leaf_1 = Node(msg=msg_condition_results[1])
bdt_leaf_2 = Node(msg=msg_condition_results[2])
bdt_leaf_3 = Node(msg=msg_condition_results[3])
bdt_leaf_4 = Node(msg=msg_condition_results[4])
bdt_leaf_5 = Node(msg=msg_condition_results[5])
bdt_leaf_6 = Node(msg=msg_condition_results[6])


# leaves 1&2 and 4&5 all undergo the renewables-target-test, to see if above 30% threshold
bdt_renewables_target_test1 = Node(left=bdt_leaf_1, right=bdt_leaf_2, threshold=30, fuel_type="renewables_total", msg="renewables target test 1 (left)")
bdt_renewables_target_test2 = Node(left=bdt_leaf_4, right=bdt_leaf_5, threshold=30, fuel_type="renewables_total", msg="renewables target test 2 (right)")

# the parent of 1&2 (renewable node test1 above), and the leaf 3, undergo the solar density test if above 35% threshold.
bdt_solar_density_test1 = Node(left=bdt_renewables_target_test1, right=bdt_leaf_3, threshold=35, fuel_type="solar", msg="solar density test 1 (left)")

# the parent of 4&5 (renewable node test2 above), and the leaf 6, undergo the solar density test if above 35% threshold.
bdt_solar_density_test2 = Node(left=bdt_renewables_target_test2, right=bdt_leaf_6, threshold=35, fuel_type="solar", msg="solar density test 2 (right)")

# for both solar_density_test nodes, they are children of the root.
##   root has a test if the baseload % is above 60.
#  (This 70% is highly abstracted.  Actual grid reliability could be maintained with a higher % renewables if we simply had a TON of total MWs.  So the MWs needed for baseload would be there as a smaller % of a larger MW total.)
bdt_root_test = Node(left=bdt_solar_density_test1, right=bdt_solar_density_test2, threshold=60, fuel_type="baseload_total", msg="baseload test")


###################################################################

# when this moodule gets imported into the server.py, it auto-runs and creates the bdt, and dictionary of message results.

# then this specific function below, gets only called on the specific frontend data.

def bdt_on_user_input(user_input_dict, bdt_root_test=bdt_root_test):
    results_dict = {}

    for county,condition in user_input_dict.items():

        # enter into condition dict, the two additional values used in the decision tree
        user_input_dict[county]["renewables_total"] = int(user_input_dict[county]["solar"]) + int(user_input_dict[county]["wind"]) + int(user_input_dict[county]["hydro"])
        user_input_dict[county]["baseload_total"] = int(user_input_dict[county]["gas"]) + int(user_input_dict[county]["coal"]) + int(user_input_dict[county]["nuclear"])

        # run condition through the decision tree, and assign result to dict per county
        results_dict[county] = bdt_root_test.testing_condition(condition)

    return results_dict


###################################################################

# #  TEST THE DECISION TREE!

# fuel_mix_test = {
#   "Alameda": {"gas":30, "coal":20, "solar":14, "wind":20, "nuclear": 30, "hydro":30, "other":14},
#   "Alpine": {"gas":16, "coal":14, "solar":40, "wind":14, "nuclear": 14, "hydro":14, "other":14},
#   "Amador": {"gas":30, "coal":40, "solar":14, "wind":0, "nuclear": 14, "hydro":0, "other":14},
#   "Butte": {"gas":16, "coal":14, "solar":14, "wind":14, "nuclear": 14, "hydro":14, "other":14}
#   }
#   # alameda should be all good.
#   # alpine should have too litte norm, and too much solar
#   # amador should be good on norm and heat, and missing renewables target.
#   # but has too little on norm and heat waves, but at least made renewable target


# print bdt_on_user_input(fuel_mix_test)

