from time import sleep
import yaml
import argparse

# Dont fail if this module is not installed
try:
    import random
except ImportError:
    pass
try:
    import pygame
except ImportError:
    pass

# Colors for map visualiser
YELLOW = (255, 255, 0)
BLUE = (0 , 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (124,252,0)
WHITE = (255, 255, 255)

def extract_yaml(filename):
    with open(filename, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def extract_map_file(filename):
    map_data = []
    with open(filename) as file:
        for line in file:
            map_data.append(line)
    return map_data

def get_char_location(search_char, map):
    # Note that top left is coords 1,1
    y = 1
    x = 1

    for line in map:
        if search_char in line:
            break
        else:
            y += 1
    for char in map[y-1]:
        if search_char in char:
            break
        else:
            x += 1
    return [x, y]

class Map_Manager:
    def __init__(self, map, width, height, wall_char, start_coords, end_coords):
        pygame.init()

        self.map = map
        self.width = width
        self.height = height
        self.wall_char = wall_char
        self.start = start_coords
        self.end = end_coords   
        self.screen = pygame.display.set_mode([width*10, height*10])
        
        self.draw_map()

    # Create the screen and visualise the map
    def draw_map(self):
        # Background set to white
        self.screen.fill(WHITE)

        # Draw the walls
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == self.wall_char:  
                    pygame.draw.circle(self.screen, BLACK, ((x+1)*10, (y+1)*10), 4)

        # Draw start point
        pygame.draw.circle(self.screen, GREEN, (self.start[0]*10, self.start[1]*10), 6)
        # Draw end point
        pygame.draw.circle(self.screen, RED, (self.end[0]*10, self.end[1]*10), 6)
        # Update the screen
        pygame.display.flip()

    # Add a new point to the map screen
    def add_point_marker(self, coords, colour):
        pygame.draw.circle(self.screen, colour, (coords[0]*10, coords[1]*10), 4)
        # Update the screen
        pygame.display.flip()
    
# Score is the distance between n1 and n2 using the Euclidean distance algorithm
def calc_score(n1_coords, n2_coords):
    x1 = n1_coords[0]
    y1 = n1_coords[1]
    x2 = n2_coords[0]
    y2 = n2_coords[1]
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Randomises just the X coord value of the start and end location
def randomise_start_end_coords(map_data, astar_config, map_title):
    # Find the current start and end coordinates
    start_location = get_char_location(astar_config[map_title]['begin'], map_data)
    end_location   = get_char_location(astar_config[map_title]['end'], map_data)
    coords = [start_location, end_location]

    passage_char = astar_config[map_title]['passage']

    map_width = int(map_title.split('x')[0])

    # Remove the old begin and end markers from the map
    new_map = map_data
    for coord in coords:
        for y, row in enumerate(new_map):
            if y == coord[1]-1:
                x = coord[0]-1
                new_map[y] = row[:x] + passage_char + row[x+1:]

    # Randomise new start and end X coords
    start_location[0] = random.randrange(2, map_width-1)
    end_location[0] = random.randrange(2, map_width-1)

    # Write the begin back to the map
    begin_char = astar_config[map_title]['begin']
    for y, row in enumerate(new_map):
        if y == start_location[1]-1:
            x = start_location[0]-1
            new_map[y] = row[:x] + begin_char + row[x+1:]

    # Write the end back to the map
    end_char = astar_config[map_title]['end']
    for y, row in enumerate(new_map):
        if y == end_location[1]-1:
            x = end_location[0]-1
            new_map[y] = row[:x] + end_char + row[x+1:]

    return new_map, start_location, end_location

class Point:
    wall_char = ''
    map = []

    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.coords = coords
        self.fScore = 0
        self.hScore = 0
        self.gScore = 0

    # Enables sorted() to sort array of point class by fScore
    def __lt__(self, other):
        return self.fScore < other.fScore

    # Determine and return valid neighbours
    def find_neighbours(self):
        new_neighbours = []
        possible_neighbours = []
        
        # Cannot move diagonally 
        possible_neighbours.append([self.coords[0]-1, self.coords[1]])
        possible_neighbours.append([self.coords[0], self.coords[1]-1])
        possible_neighbours.append([self.coords[0]+1, self.coords[1]])
        possible_neighbours.append([self.coords[0], self.coords[1]+1])

        for possible_neighbour in possible_neighbours:
            x = possible_neighbour[0]
            y = possible_neighbour[1]

            # Walls are not valid neighbours
            if Point.wall_char not in Point.map[y-1][x-1]:
                new_neighbours.append(possible_neighbour)

        return(new_neighbours)

# Write found solution to file
def write_solution(solution_path, map_data, map_name):
    final_map = map_data
    point_marker = 'M'

    for coord in solution_path:
        for y, row in enumerate(map_data):
            if y == coord[1]-1:
                x = coord[0]-1
                final_map[y] = row[:x] + point_marker + row[x+1:]

    with open(f'{map_name}_solution.txt', 'w') as f:
        for row in final_map:
            f.write(row)

    print(f"Written solution for file {map_name}_solution.txt.")

def find_shortest_route(start_location, end_location, visualiser_on, map, map_manager, map_title, map_width, map_height, wall_char, randomise_start_end):
    # Set static variables for the Point class
    Point.map = map
    Point.wall_char = wall_char

    # Set up first Point class at starting location
    # Point class will be used to track F, H & G scores on each point in the map
    start = Point(start_location)
    start.gScore = 0
    start.fScore = calc_score(start_location, end_location)

    # Store active points
    openSet = []
    openSet.append(start)

    # Store closed/explored points so they are not revisited
    closedSet = []

    # comeFrom array is used to track the optimal path from start to end
    comeFrom = [[0 for _ in range(map_height+1)] for _ in range(map_width+1)] 
    
    # Set the start to current
    current = start

    solved_maze = False

    while len(openSet):
        closedSet.append(current.coords)
        current = sorted(openSet)[0]

        if visualiser_on:
            # Update map with current coords
            map_manager.add_point_marker(current.coords, BLUE)
            # Check to see if the user has quit
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

        # Break from loop once the end has been reached
        if current.coords == end_location:
            print("Path Found!")
            # Reconstruct and visualise optimal path
            reconstruct_path(comeFrom, start_location, end_location, map_manager, map, map_title, randomise_start_end)
            # Indicate that we have found a solution
            solved_maze = True
            break

        openSet.remove(current)
        for neighbour in current.find_neighbours():
            new_neighbour = Point(neighbour)

            # Set the cost to move from current to neighbouring point low so it moves towards the goal faster
            potential_gScore = current.gScore + 0.1
            potential_fScore = potential_gScore + calc_score(new_neighbour.coords, end_location)

            # Calculate new nighbours scores
            new_neighbour.gScore = calc_score(start_location, new_neighbour.coords)
            new_neighbour.hScore = calc_score(new_neighbour.coords, end_location)
            new_neighbour.fScore = new_neighbour.gScore + new_neighbour.hScore

            if potential_fScore < new_neighbour.fScore:
                new_neighbour.gScore = potential_gScore
                new_neighbour.fScore = potential_gScore + calc_score(new_neighbour.coords, end_location)
                
                # Don't re-explore points or add duplicate points to openSet
                if new_neighbour not in openSet and new_neighbour.coords not in closedSet:
                    # Add to comeFrom to trace the optimal path
                    comeFrom[new_neighbour.coords[0]][new_neighbour.coords[1]] \
                      = current.coords
                    openSet.append(new_neighbour)

        # Delay by 10ms to visualise A* algorithm
        if visualiser_on:
            sleep(0.01)

    return solved_maze

# Trace backwards through comeFrom to reconstruct and visualise the optimal path
def reconstruct_path(comeFrom, start_coords, end_coords, map_manager, map_data, map_name, randomise_start_end):
    coords = comeFrom[end_coords[0]][end_coords[1]]

    yellow_brick_road = []
    yellow_brick_road.append(coords)

    done = False
    while not done:
        coords = comeFrom[coords[0]][coords[1]]

        if map_manager:
            map_manager.add_point_marker(coords, YELLOW)

        if coords == start_coords:
            done = True

        yellow_brick_road.append(coords)
    
    print(f"Size of optimal path is {len(yellow_brick_road)}.")

    if not randomise_start_end:
        write_solution(yellow_brick_road, map_data, map_name)

def main(map_title, visualiser_on, randomise_start_end):

    map_width = int(map_title.split('x')[0])
    map_height = int(map_title.split('x')[1])

    # Extract map information based on map name
    astar_config = extract_yaml('assignment/astar_config.yaml')
    wall_char = astar_config[map_title]['wall']
    map = extract_map_file(f'assignment/{map_title}.txt')

    if randomise_start_end:
        # Randomise start and end locations and update the map
        map, start_location, end_location = randomise_start_end_coords(map, astar_config, map_title)
    else:
        # Find the start and end coordinates
        start_location = get_char_location(astar_config[map_title]['begin'], map)
        end_location   = get_char_location(astar_config[map_title]['end'], map)

    # Initialise map visualiser
    if visualiser_on:
        map_manager = Map_Manager(map, map_width, map_height, wall_char, start_location, end_location)
    else:
        map_manager = False
    
    solved_maze = find_shortest_route(start_location, \
                        end_location, \
                        visualiser_on, \
                        map, \
                        map_manager, \
                        map_title, \
                        map_width, \
                        map_height, \
                        wall_char, \
                        randomise_start_end)

    # Keep visualiser open after a solution has been found
    if visualiser_on:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

    return solved_maze

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("map", type=str, choices=["41x41", "61x31", "81x81"], help="Map/Maze")
    parser.add_argument("--visualise", help="Visualise A* algorithm, requires pygame module", action="store_true")
    parser.add_argument("--randomise", help="Randomises the X coord for the start and end points, requires random module", action="store_true")

    args = parser.parse_args()

    main(args.map, args.visualise, args.randomise)