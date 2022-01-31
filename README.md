# Flow-Free-Solver-Backtracking-Search-Algorithm
Solve flow free game as a Constraint Satisfaction Problem using smart and dumb agents
By using backtracking search, you can solve flow free game as constraint satisfaction problem whereas;

-Variables:which are the variables of the problem and in this case they are the empty nodes.

-Domains: Since there cannot be an empty node, i.e., all nodes
must be filled with color. So the domain of each
node or each variable can be the colors available for
each node.
Di= { R, G, B, Y, C, P, D, C….}

-Constraints: 
1. No zigzag allowed when connecting colors.
2. Cornered State: check that one node don’t corner any other node.
3. No empty cells: meaning that for a complete consistent assignment, all cells have colors in it.
4. Start and finish node have only one child/parent.
5. Pipes cannot intersect with each other.
This code has two different versions of implementation, Smart Agent & Dumb Agent.


