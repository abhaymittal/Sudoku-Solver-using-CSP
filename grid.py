class Grid:
    def __init__(self, file):
        self.grid = dict()
        self.neighbours = dict()
        self.parseInputFile(file)
        
    def parseInputFile(self,file):
        i = 0
        f = open(file, 'r')

        for line in f :
            line = line.strip().split(' ')
            j = 0
            for element in line:
                key = str(i) + str(j)
                if element == '-':
                    self.grid[key] = list(range(1,10))
                elif int(element) <= 9 and int(element) > 0:
                    self.grid[key] = [int(element)]
                j = j + 1

            i = i + 1
                
        
grid = Grid("first.sudoku")
