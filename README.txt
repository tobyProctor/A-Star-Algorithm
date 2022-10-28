                                         A* Algorithm Implementation
                                                 Toby Proctor

                                                 How to run:
usage: a_star.py [-h] [--visualise] [--randomise] {41x41,61x31,81x81}

positional arguments:
  {41x41,61x31,81x81}  Map/Maze

optional arguments:
  -h, --help           show this help message and exit
  --visualise          Visualise A* algorithm, requires pygame module
  --randomise          Randomises the X coord for the start and end points, requires random module

                                                Examples:
python3 a_star.py 81x81
^
This will read in the 81x81.txt and astar_config.yaml from ./assignment and solve it. Resultant 
solution will be outputted to the txt file 81x81_solution.txt and path length printed to terminal.
Required modules for this base command are: time, yaml, argplus

python3 a_star.py 61x31 --visualise
^
This will also read in the 61x31.txt and astar_config.yaml from ./assignment and solve it. Resultant 
solution will be outputted to the txt file 61x31_solution.txt and path length printed to terminal. But 
the switch --visualise will visualise the solution, note that this requires the pygame module if you 
use this switch.
Required modules for this command are: time, yaml, argplus, random

python3 a_star.py 41x41 --randomise
^ 
This will also read in the 41x41.txt and astar_config.yaml from ./assignment but will randomise the
start and end points on the map on the X-Axis before solving it. No solution will be outputted to a 
text file, but instead "Path Found!" will be printed to the terminal.
Required modules for this command are: time, yaml, argplus, random, pygame

                                                Outputs:
After running the following files will be generated:
- 81x81_solution.txt
- 61x31_solution.txt
- 41x41_solution.txt
The path found from start to end will be marked with the character 'M'.

                                          How to run unit tests:
python3 test_a_star.py
^
This will verify that the base requirements for the assignment were met and randomise 100 times the
start and end points for each map size. Output looks like:
----------------------------------------------------------------------
Ran 6 tests in 1.964s

OK

                                          Directory Structure:
Toby_Proctor_assignment_solution
             │   a_star.py
             │   README.txt
             │   test_a_star.py
             │   tree.txt
             │
             └───assignment <== 'assignment' directory required here for the script to read input files
                     41x41.txt
                     61x31.txt
                     81x81.txt
                     astar_config.yaml
                     README.txt                                          
