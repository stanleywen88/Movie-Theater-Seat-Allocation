import sys
import heapq

cols = 20
buffer_seat = 3


class TheaterSeatAllocation:

    def __init__(self):
        self.heap = [-i for i in range(10, 0, -1)]
        self.seat = {}
        self.create_theater()
        heapq.heapify(self.heap)

    def create_theater(self):
        """
        This function create an empty theater as a dictionary (key=row, value=seats)
        :return: nothing
        """
        for i in range(1, 11):
            self.seat[i] = ['#'] * cols
            self.seat[i].append(20)

    def seat_allocate(self, reservation_id, requested_seats) -> str:
        """
        This function allocates seats with given params.
        :param reservation_id: reservation identifier of the request
        :param requested_seats: number of requested seat we need to find
        :return: string - allocated seat or message to indicate under full capacity
        """
        # check and update heap each time before searching and assigning
        self.heap_check()

        # all rows are full
        if len(self.heap) == 0:
            return "Capacity Reached! No more seats for this and further group."

        # takes in two key arguments (row index and available seats for a row)
        # print('DEBUG self.heap status', self.heap)
        curr_heap = [i for i in self.heap]
        while curr_heap and self.seat[-curr_heap[0]][-1] < requested_seats:
            # print("DEBUG", self.seat[-curr_heap[0]][-1], curr_heap, requested_seats)
            heapq.heappop(curr_heap)
            # print("DEBUG, curr_heap and self.heap", curr_heap, self.heap)

        # available rows are not able to fulfill this group
        if not curr_heap:
            return "Cannot allocate seats to this reservation!"

        optimal_row_index = curr_heap[0]*-1
        # print('DEBUG, seat_allocate, heap', optimal_row_index)
        seat_row = self.seat[optimal_row_index]
        seats_allocated = ""
        buffers = 0
        buffer_assigned = False

        for seatNumber, seat in enumerate(seat_row):
            # print("DEBUG", reservation_id, requested_seats, buffer_assigned, seatNumber, seat, seats_allocated)
            # terminate for-loop if finish assigning seat and buffer, or reach the end of the row
            if seatNumber == 20 or (buffer_assigned and requested_seats == 0):
                break

            # when seat is empty
            if seat == "#":
                # print("DEBUG, start assigning seat or updating buffer")
                # allocate seat
                if requested_seats > 0:
                    seats_allocated += "{}{} ".format(get_row_name(optimal_row_index), seatNumber+1)
                    seat_row[seatNumber] = reservation_id
                    requested_seats -= 1
                    seat_row[-1] -= 1
                    self.seat[optimal_row_index] = seat_row

                # update buffer after finishing allocating seats
                else:
                    seat_row[seatNumber] = "buffer"
                    buffers += 1
                    seat_row[-1] -= 1
                    self.seat[optimal_row_index] = seat_row

                    # Check if required buffers are filled
                    if buffers == buffer_seat:
                        buffer_assigned = True

            # not an empty seat, keep finding empty seat
            else:
                continue

        return reservation_id + " " + seats_allocated

    def heap_check(self):
        """
        This function remove the row_index with no more vacant seats from the heap
        :return: nothing
        """
        while self.seat[-self.heap[0]][-1] == 0:
            # print('DEBUG, heappop', self.heap[0])
            if len(self.heap) == 1:
                heapq.heappop(self.heap)
                break
            heapq.heappop(self.heap)
        heapq.heapify(self.heap)

    def parse_input(self, f, output_file):
        """
        This function parses the input file and call the seat_allocate function
        :param f: input file with reservation ID and number of requested seat
        :param output_file: output file for allocation results
        :return: nothing
        """
        try:
            for line in f:
                # print("Debug input file", line)
                reservation_id = line.split(" ")[0]  # eg.. 'R001'
                requested_seats = int(line.split(" ")[1])  # 3
                # print("DEBUG, parse_input", reservation_id, requested_seats, validate_input(requested_seats))

                # Check if input is valid
                if verify_input(requested_seats):
                    allocation_result = self.seat_allocate(reservation_id, requested_seats)
                    # print('DEBUG allocation_result', allocation_result)
                    if allocation_result == "Capacity Reached! No more seats for this and further group.":
                        print("{} {}: capacity reached!".format(reservation_id, requested_seats))
                        break
                    elif allocation_result == "Cannot allocate seats to this reservation!":
                        print("{} {}: Cannot allocate seats to this reservation!".format(reservation_id,
                                                                                         requested_seats))
                    else:
                        # Write the returned output
                        # print("DEBUG, writing result to file")
                        write_result(output_file, allocation_result)

            # message when finish assigning
            print("Finish assigning seats. Please check output file for seat allocation results.")
        except Exception as error:
            print("Error: {}".format(error))

    def print_allocation(self):
        """
        This function output the 2D map of the theater seats for debug purpose.
        :return: string containing map of the seats
        """
        seat = ""
        for i in range(1, 11):
            seat += chr(i+64) + str(self.seat[i])
            seat += '\n'
        seat += '\n'
        return seat


def get_row_name(index):
    """
    This function gets the row ID in characters with given integer index
    :param index: row index (1 -> 'A', 10 -> 'J')
    :return: char according to unicode
    """
    return chr(index + 64)


def write_result(output_file, allocation_result):
    """
    This functions writes the seat reservations to the output file
    :param output_file: output file
    :param allocation_result: seat allocation results in string
    :return: nothing
    """
    try:
        output_file.write(allocation_result + "\n")
    except Exception as error:
        print("Error in writing to output file: {}".format(str(error)))


def verify_input(requested_seats):
    """
    This function verifies the seats requested are positive and under maximum capacity.
    :param requested_seats: number of seats requested to be assigned
    :return: False if unable to assign, True if able to assign
    """
    if requested_seats <= 0:  # must be non-negative
        print('Seats requested must be greater than 0.')
        return False
    if requested_seats > 20:  # must be under theater maximum capacity
        print('Seats requested exceed theater maximum capacity.')
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Please execute the script in the following format:\npython3 solution.py <input_file>")

    input_file = sys.argv[1]
    file = ""

    try:
        file = open(input_file, "r")
        output = open("output.txt", "a")
    except IOError:
        sys.exit("Error: File does not appear to exist.")

    output.write("----Testing {} ----\n".format(input_file))

    theater = TheaterSeatAllocation()
    theater.parse_input(file, output)
    output.write(theater.print_allocation())  # if desire clean result without seat map, comment out
