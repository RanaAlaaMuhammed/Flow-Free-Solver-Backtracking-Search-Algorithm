import heapq
import constraints as con
import time
import os
class Nodes:
    def __init__(self, val, i, j):
        self.visited = False
        self.value = val
        self.i = i
        self.j = j 
        self.neighbors = []
        self.Parent = None

    def is_visited(self):
        self.visited = True   
 #####################################################################################################
def maze_reader(filename):
    #read in file
    maze = []
    file = open(filename, "r")
    columns = file.readlines()
    for i, column in enumerate(columns):
        column = column.strip()
        row_nodes = []
        for j, row in enumerate(column):
            for element in row:
                #make each element a node
                newnode = Nodes(element, i, j)
                row_nodes.append(newnode)
        maze.append(row_nodes)
    #give each node knowledge on its neighbors
    for i, row in enumerate(maze):
        for j, element in enumerate(row):
            if j+1 <= len(row)-1:
                element.neighbors.append(maze[i][j+1])
            if j-1 >= 0:
                element.neighbors.append(maze[i][j-1])
            if i-1 >= 0:
                element.neighbors.append(maze[i-1][j])
            if i+1 <= len(maze)-1:
                element.neighbors.append(maze[i+1][j])
    return maze

def maze_printer(maze):
    
    for row in maze:
        for element in row:
            print(element.value, end='')
        print('')
    print()
########################################################################################################
               
class CSP:
    def __init__(self, maze, debug):
        self.domain = []
        self.finish = {}
        self.start = {}
        self.visited_nodes = []
        self.complete_colors = []
        self.debug = ''
        if debug is 'True':
            self.debug = True
        elif debug is 'False':
            self.debug = False
        self.steps = 0
        self.find_start_and_finish(maze)
        print('Solving:')
        maze_printer(maze)
        self.con = con.Constraints(self.start, self.finish, self.debug)




    def find_start_and_finish(self, maze): #find start and finish source to each color
        for row in maze:
            for node in row:
                if node.value is not '_':
                    self.visited_nodes.append(node) #append to visited so their values do not change
                    if node.value not in self.domain:
                        self.domain.append(node.value)
                    if node.value not in self.start:
                        self.start[node.value] = node
                    else:
                        self.finish[node.value] = node
    def dumb_BC(self, assignment): #backtracking with no heuristics
        if self.is_Complete(assignment): #if the assignment is complete, return and print maze
            maze_printer(assignment)
            return assignment 
        node = self.get_node(assignment) #get a node that has not been visited
        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False
        for color in self.get_colors(node): #get all colors that are not complete
            self.steps += 1           
            if self.is_Consistant(color, node, assignment): #if the color we have chosen is legal, use it
                if self.is_Color_completed(color):
                    self.complete_colors.append(color)
                self.visited_nodes.append(node)
                result = self.dumb_BC(assignment) #move on to next node
                if result:
                    return result
                self.visited_nodes.remove(node) #that branch failed, backtrack
                if color in self.complete_colors:
                    self.complete_colors.remove(color)
                node.value = '_'
        return False
    def backtracking(self, assignment): #backtracking with heuristics
        if self.is_Complete(assignment): #if the assignment is complete, return and print maze
            maze_printer(assignment)
            return assignment
        colors, node = self.MRV(assignment) #get a node that has the least amount of available legal moves
        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False
        for color in colors:
            self.steps += 1           
            node.value = color
            self.visited_nodes.append(node)
            if self.is_Color_completed(color):
                self.complete_colors.append(color)
            result = self.backtracking(assignment) #move on to next node
            if result:
                return result
            self.visited_nodes.remove(node) #that branch failed, backtrack
            if color in self.complete_colors:
                self.complete_colors.remove(color)
            node.value = '_'
        return False
    def MRV(self, assignment): #find node with least available legal colors
        variable_values = []
        id = 1 #for unique ID's to break tie breakers
        heapq.heapify(variable_values)
        for row in assignment:
            for node in row:
                if node not in self.visited_nodes:
                    legal_colors = [] 
                    for color in self.domain:
                        if color not in self.complete_colors:
                            if self.is_Consistant(color, node, assignment):
                                node.value = '_'
                                legal_colors.append(color)
                    if len(legal_colors) is 1:
                        return legal_colors, node
                    else:
                        heapq.heappush(variable_values, (len(legal_colors), id, legal_colors, node))
                        id += 1 

        curr_node = heapq.heappop(variable_values)
        return curr_node[2], curr_node[3]

    def get_colors(self, node): #get a color that is not complete
        colors = [] #prioitizes adjacent colors
        for neighbor in node.neighbors:
            if neighbor.value is not '_' and neighbor.value not in colors and neighbor.value not in self.complete_colors:
                colors.append(neighbor.value)
        for color in self.domain:
            if color not in colors and color not in self.complete_colors:
                colors.append(color)
        return colors

    def get_node(self, assignment): #get a node that is not visited
        for row in assignment:
            for node in row:
                if node not in self.visited_nodes: #if node is not visited, return
                    return node

    def is_Complete(self, assignment): #checks to see if assignment is correct
        for color in self.domain:
            if color not in self.complete_colors:
                return False
        print('Complete')
        print('Total Assignments: {}'.format(self.steps))
        return True

    def is_Color_completed(self, color): #checks to see if color is complete
        node = self.start[color]
        path = []
        while node is not self.finish[color]:
            for neighbor in node.neighbors:
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break
                elif neighbor is node.neighbors[-1]:
                    return False
        return True

    def is_Consistant(self, color, node, assignment): #checks to see that color will not violate any constraints
        node.value = color

        #if the node will not cause a zig_zag, the start and finish node only have one child, and we dont corner any other nodes, move on
        for neighbor in node.neighbors:
            if neighbor.value is not '_':
                if self.con.is_Zig_zag(neighbor, color) or self.con.is_Corner(neighbor) or not self.con.near_start(neighbor.value) or not self.con.near_finish(neighbor.value):
                    node.value = '_'
                    return False
        return True

if __name__=='__main__':
    user_input = input("Enter the path of your file: \n")
    assert os.path.exists(user_input), "I did not find the file at, "+str(user_input)
    dumb_maze = maze_reader(user_input)
    Dumb_CSP = CSP(dumb_maze, user_input)
    start_time = time.time()
    Dumb_CSP.dumb_BC(dumb_maze)
    end_time = time.time()
    print("Flow free Dumb search took {} seconds\n".format(end_time - start_time))
    smart_maze = maze_reader(user_input)
    Smart_CSP = CSP(smart_maze, user_input)
    start_time = time.time()
    Smart_CSP.backtracking(smart_maze)
    end_time = time.time()
    print("Flow free Smart search took {} seconds\n".format(end_time - start_time))