class Constraints:

    def __init__(self, start, finish, debug):
        self.start = start
        self.finish = finish
        self.debug = debug

    def is_Zig_zag(self, node, color): #checks to see that no adjacent nodes are zig_zaging
        if node.value is color:
            count = 0
            for neighbor in node.neighbors:
                if neighbor.value is color:
                    count += 1

                if node is self.start[color] or node is self.finish[color]:
                    if count >= 2: #source zigzag
                        
                        return True

                elif count > 2: #nonsource zigzag
                    
                    return True
        return False

    def is_Corner(self, node): #checks to see that node is not cornered
        color = node.value

        if node is self.finish[color] or node is self.start[color]:
            return False #no corner

        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.finish[color] or neighbor is self.start[color]:
                    return False
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]: #if neighbor is the parent of the current node
                    for neighbor in node.neighbors:
                        if neighbor.value is '_':
                            return False
                    
                    return True
        
        return True

    def near_start(self, color): #checks whether color is part complete
        node = self.start[color]
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.finish[color]:
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node) #no intersection
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]: 
                    for neighbor in node.neighbors:
                        if neighbor.value is '_':
                            return True
                    
                    return False
        
        return False

    def near_finish(self, color):
        node = self.finish[color]
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.start[color]:
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    for neighbor in node.neighbors:
                        if neighbor.value is '_':
                            return True
                    
                    return False
        
        return False
