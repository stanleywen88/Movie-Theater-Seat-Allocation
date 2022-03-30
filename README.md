### Summary
This algorithm assigns seats within a movie theater to fulfill reservation requests. Assume the movie theater has the seating
arrangement of 10 rows x 20 seats, which is 200 seats in total. This seat assignment program is designed to maximize both customer 
satisfaction and customer safety. For the purpose of public safety, assume that a buffer of three seats and/or one row is required.

### Input Description
You will be given a file that contains one line of input for each
reservation request. The order of the lines in the file reflects the order in
which the reservation requests were received. Each line in the file will be
composed of a reservation identifier, followed by a space, and then the
number of seats requested. The reservation identifier will have the
format: R####.

Example Input File Rows:

R001 2

R002 4

R003 4

R004 3

### Output Description
The program should output a file containing the seating assignments for
each request. Each row in the file should include the reservation number
followed by a space, and then a comma-delimited list of the assigned
seats.

Example Output File Rows:

R001 I1, I2

R002 F16, F17, F18, F19

R003 A1, A2, A3, A4

R004 J4, J5, J6

### Assumption: 
1. the number in reservation identifier determines the order for assigning seat
2. the reservation identifiers are in non-decreasing order
3. all seats cost the same, and the seats are first-come-first-serve
4. each reservation wants to be seated together
5. All requests are under 20 seats, request for more than 20 seats are considering a large group and should inquire separately
6. The algorithm will run until there is no more vacant seats left. 

### Customer Satisfaction
1. Customers from the same group want to sit together and have fun.
2. The rows towards the back of the theater are more desirable

### Customer safety
A buffer of three seats is assigned between each group. If available seats are not enough for a group with buffer seats, 
this group will be assigned to another row.

### Approaches:
This algorithm uses heap to keep track from the back with rows that still have vacant seats. For example, at the beginning, 
the top of the heap will be -10, referring to Row 10 (or Row 'J') in the theater. The heap will be updated each time before
we assign seats for upcoming group. 

The overall seat map will be store as a hash table, with row index being the key, and row seats being the value. For the row
seats, "#" means an empty seat, "buffer" means a buffer seat, and "RXXX" means an occupied seat by that specific "RXXX" group.
The last element of each row seat will be the available seats for that specific row. The row seats and number of available seats
will be updated as we assign seat to the groups. 

### Testing
Using print statement (in the comment) and the print_allocation 

### Ideas for improvement:
1. for a larger theater (not just 10 rows), rows in the very back might not be the optimal seats
2. This algorithm start assigning seat from left to right in a row. Some people might want to sit in the middle. 
   1. Trade-off: start from the middle might increase buffer seats and reduce profits in the theater's stance
3. groups might be willing to be separated to get seated


## How to Implement
1. Open a terminal, move the directory to where this program is located.
2. Make sure the input file is in text format, and it's in the same folder.
3. Make sure the data is formatted as mentioned above (i.e. "R001 3")
4. Make sure there is no extra line or space in the input file
5. Type the following command: python3 SeatAllocation.py your_input_file_name.txt (input.txt in this case)
6. Output file will be created in the same folder as the python program as a text file
