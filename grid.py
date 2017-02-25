class Grid:
    def __init__(self, file):
        self.grid = [0] * 729 #81 * 9
        self.table = [0] * 81
        self.parseInputFile(file)
        
    def parseInputFile(self,file):
        i = 0
        f = open(file, 'r')

        for line in f :
            line = line.strip().split(' ')
            j = 0
            for element in line:
                if element == '-':
                    self.table[9*i+j] = 9
                elif int(element) <= 9 and int(element) > 0:
                    start = 81 * i + 9 * j
                    self.table[9*i+j] = 1
                    for k in range(0,9):
                        if k != int(element) - 1:
                            self.grid[start + k] = 1
                j = j + 1

            i = i + 1
                
    def test(self):
        for loc in self.grid:
            #print(loc,"->",self.grid[loc])
            pass
        return


