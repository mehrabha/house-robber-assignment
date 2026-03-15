class HouseRobberDFS:
    def __init__(self):
        """
        Initializes the house robber
        """

        self.stash = 0  # just to check how much we stole from all the different trips

    def ship_off_goods(self):
        self.stash = 0


    def rob_houses(self, houses: list[tuple[int, int]], time_limit:int) -> tuple[int, list[int]]:
        """
        Calculates the maximum value obtainable from the houses given time limit.
        A house of size x takes x hours to rob

        Args:
            houses list[tuple[int, int]]: A list of houses where each house is a tuple containing [valuables, size]
            time_limit int: number of hours before the police shows up
            indx, robbed: default args used internally within the algoritm

        Returns:
            result (int, list): maximum amount you can steal, list of ideal houses robbed (indexes)
        """

        result = (0, [])

        if len(houses) == 0:
            return result

        stack = [(0, 0, [], time_limit)]    # state = (current_node, current_score, current_path, remaining_time)

        while not len(stack) == 0:
            node = stack.pop()

            if node[0] == len(houses):
                # leaf node; save score, path
                
                if node[1] > result[0]:
                    result = (node[1], node[2])
            else:
                house = houses[node[0]]

                child1 = (node[0] + 1, node[1], node[2], node[3])   # skip the current house, score and other states will be same as before
                stack.append(child1)

                if house[1] <= node[3]:   # if time limit permits
                    # calculate new score, time_limit and update path for child2
                    new_score = node[1] + house[0]
                    new_timelimit = node[3] - house[1]
                    new_path = node[2] + [node[0]]

                    child2 = (node[0] + 1, new_score, new_path, new_timelimit)
                    stack.append(child2)
        
        return result







        
        

        
    
