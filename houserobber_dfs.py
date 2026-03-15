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
        
        # make a copy and save the original indexes eg (valuables, size, indx)
        houses2 = []
        for i in range(len(houses)):
            house = houses[i]
            houses2.append((house[0], house[1], i))

        # sort houses by efficiency (best bang/buck)
        houses2.sort(key=lambda x: x[0]/x[1], reverse=True)

        MAX_RATE = houses2[0][0] / houses2[0][1]

        stack = [(0, 0, [], time_limit)]    # state = (current_node, current_score, current_path, remaining_time)

        while not len(stack) == 0:
            node = stack.pop()

            if node[0] == len(houses2):
                # leaf node; save score, path
                
                if node[1] > result[0]:
                    result = (node[1], node[2])
            else:
                # explore node only if it has potential
                # potential = current score + remaining time * best bang/buck house rate we've seen so far
                potential = node[1] + node[3] * MAX_RATE

                # to further speed up the algorithm, we can leverage a smarter local_rate
                local_rate = house[0] / house[1]

                # since array is sorted the current house has the best rate of remaining houses
                potential = node[1] + node[3] * local_rate

                if potential <= result[0]:
                    # it can't beat our best score so far, terminate branch
                    continue

                house = houses2[node[0]]

                child1 = (node[0] + 1, node[1], node[2], node[3])   # skip the current house, score and other states will be same as before
                stack.append(child1)

                if house[1] <= node[3]:   # if time limit permits
                    # calculate new score, time_limit and update path for child2
                    new_score = node[1] + house[0]
                    new_timelimit = node[3] - house[1]
                    new_path = node[2] + [house[2]]

                    child2 = (node[0] + 1, new_score, new_path, new_timelimit)
                    stack.append(child2)
        
        return result







        
        

        
    
