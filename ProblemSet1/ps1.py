###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import timeit
#I used timeit module in order to obtain more reliable results because
#it takes into account factors that pose the variance among the execution of code, through repeating the execution of script.

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1 (Done!)
def greedy_cow_transport(cows,limit=10):
    """(20/20 done!)
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    answer = []
    cows_copy = sorted(cows.items(), key=lambda x: x[1],reverse=True)
    while len(cows_copy) != 0:
        total_weight = 0
        result = []
        i = 0
        while i < len(cows_copy):
            if (total_weight + cows_copy[i][1]) <= limit :
                total_weight += cows_copy[i][1]
                result.append(cows_copy[i][0])
                del cows_copy[i]
                i -= 1
            i += 1
        answer.append(result)
    return answer
        


# Problem 2 (Done!)
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = sorted(cows.items(), key=lambda x: x[1],reverse=True)
    min_num= None
    temp = 0
    result = []
    for partition in get_partitions(cows_copy):
        for element in partition:
            temp = 0
            for data in element:
                temp += data[1]
                if temp > limit:
                    break
            if temp > limit:
                break
        if temp <= limit and (min_num == None or len(partition) < min_num):
            result = partition
            min_num = len(partition)
    return result
    

# Problem 3 (Done!)
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    best_greedy = None
    best_brute_force = None
    number_of_trips_brute_force = len(brute_force_cow_transport(cows))
    number_of_trips_greedy = len(greedy_cow_transport(cows))
    for i in range(5): #repeating the timing in order to find more accurate result
        start1 = timeit.default_timer()
        greedy_cow_transport(cows)
        timing_greedy = timeit.default_timer()-start1
        
        if best_greedy == None or timing_greedy < best_greedy:
            best_greedy = timing_greedy
        
        start2 = timeit.default_timer()
        brute_force_cow_transport(cows)
        timing_brute_force = timeit.default_timer() - start2
        if best_brute_force == None or timing_brute_force < best_brute_force:
            best_brute_force = timing_brute_force
            
    print("brute-force methot takes approximately",best_brute_force,"""in seconds and number of trips returned by brute force algorithm is""",number_of_trips_brute_force)
    print("greedy algorithm takes approximately",best_greedy,"""in seconds and number of trips returned by greedy algorithm is""", number_of_trips_greedy,"\n")
    print("greedy algorithm is " , best_brute_force/best_greedy , "times faster than brute force algorithm but greedy algorithm does not guarantee to return the global optimum solution in every case\n")
        

"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
print(cows)
compare_cow_transport_algorithms()
print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))