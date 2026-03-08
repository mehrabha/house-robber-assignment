class HouseRobber:
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

        Returns:
            result (int, list): maximum amount you can steal, list of ideal houses robbed (indexes)
        """

        caches = [[]]

        for i in range(time_limit + 1):
            caches[0].append(0)
            
        for house in houses:
            cache = []

            for i in range(time_limit + 1):
                if i < house[1] :
                    # not enough time to rob this house at the moment, use previous sum
                    cache.append(caches[-1][i])
                else:
                    # compare the max amount of valuables we can rob when we include or skip this house

                    option1 = caches[-1][i]  # skip new house and go with existing sum
                    option2 = house[0] + caches[-1][i - house[1]]   # valuables from this house + max we can rob in the remaining time

                    cache.append(max(option1, option2))
            caches.append(cache)

        if len(caches) > 1:
            houses_robbed = []

            i = len(caches[0]) - 1
            j = len(caches) - 1

            while i > 0 and j > 0:
                house = houses[j - 1]

                if caches[j][i] != caches[j - 1][i]:
                    houses_robbed.append(j - 1)
                    i -= house[1]
                j -= 1


            self.stash += caches[-1][-1]
            return (caches[-1][-1], houses_robbed)
        return (0, [])
    
