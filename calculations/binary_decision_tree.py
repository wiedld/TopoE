test = "trees are connected"

class Node(object):

    def __init__(self, threshold=None, fuel_type=None, left=None, right=None, msg_id=None):
        assert left is None or isinstance(left, Node)
        assert right is None or isinstance(right, Node)
        self.fuel_type = fuel_type     # what fuel type will be tested
        self.threshold = threshold      # what the threshold is for the test
        self.left = left    # this is the left child
        self.right = right    # this is the right child
        self.msg_id = msg_id

    def testing_condition(self, condition_dict):
        current_node = self
        if current_node.left==None and current_node.right==None: # no children
            return current_node.msg_id
        if condition_dict[current_node.fuel_type] <= current_node.threshold:
            current_node = current_node.left
            current_node.testing_condition(condition_dict)
        if condition_dict[current_node.fuel_type] > current_node.threshold:
            current_node = current_node.right
            current_node.testing_condition(condition_dict)
        return "Error in binary decision tree"


msg_condition_result = {
    1: "Your customers complain about lossing energy on a normal basis, and the electric grid tends to go dark during heat waves.  Also, your company is being charged by the state for failing their renewables target.",
    2: "Your customers lose power during normal days an heat waves, but at least you have made your renewables target to help the environment!",
    3: "Your electric grid doesn't have enough energy to funciton on most days, but has too mush energy durign sunny heat waves -- causes local areas in the grid to melt down (e.g. voltage flux).",
    4: "You definitely keep the lights on for your customers, during both the normal days and the hot ones.  However, your environmental foresight is lackign and your grandchildren have asthma.",
    5: "You have hit your environmental goals, while keeping the lights on during both normal days and heat waves.  Congratulations!  You shoudl apply to be a utility CEO!",
    6: "Your customers have energy most days, and your renewable targets are awesome.   However, durign intense heat waves the excess sunny energy may cause voltage fluctuations.  (Congrats...you have melted your distribution grid.)"
}
