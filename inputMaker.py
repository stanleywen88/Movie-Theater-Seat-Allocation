
# Generates random seat reservation requests for about 200 seats
# requests format in this way:
# R001 2
# R002 4
# R002 4
# R004 3

import random


inputFile = open("input.txt", "w+")
total_seat = 0
n = 1

while total_seat < 200:
    curr_request = random.randint(1, 20)
    total_seat += curr_request
    inputFile.write('{} {}{}'.format("R" + '{:04d}'.format(n), curr_request, '\n'))
    n += 1

inputFile.close()
