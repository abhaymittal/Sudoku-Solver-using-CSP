def getNeighbours(self, g_x, g_y):
        ## elements in the same row
        g_x_neighbours = [str(g_x) + str(x) for x in range(0,9) if x != g_y]
        ## elements in the same column
        g_y_neighbours = [str(x) + str(g_y) for x in range(0,9) if x != g_x]
        ## elements in the same box

        box_n = []
        x_base = int(g_x/3) * 3
        y_base = int(g_y/3) * 3
        for i in range(3):
            for j in range(3):
                box_n.append(str(x_base + i) + str(y_base + j))

        box_n.remove(str(g_x) + str(g_y))
        neighbours = list(set(g_x_neighbours + g_y_neighbours + box_n))
        neighbours.sort()

        return neighbours
