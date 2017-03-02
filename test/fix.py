f = open('sudokus', 'r')
i = 0
output_file = open('0', 'w')

for line in f:
    line = line.strip()
    if "Grid" in line:
        i = i + 1
        output_file.close()
        output_file = open(str(i) , 'w')
    else :
        output_file.write(line + "\n")
    
        
