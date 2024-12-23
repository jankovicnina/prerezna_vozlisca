### Articulation Points in Graphs
This repository contains a Python implementation to determine the articulation points in an undirected and connected graph. An **articulation point** is a vertex that, when removed along with its incident edges, disconnects the graph.

# Problem Description
Given a graph :
- A vertex  is an articulation point if its removal increases the number of connected components in the graph.
- The algorithm uses a depth-first search (DFS) to determine articulation points efficiently.

# Input Format
1. The first line contains two integers,  (number of vertices) and  (number of edges).
2. The next  lines each contain two integers representing an edge between vertices.

# Output Format
- Prints a single line with the labels of all articulation points, sorted in ascending order and separated by spaces.
- If there are no articulation points, prints -1.


## Implementation Details
1. Discovery Time (pre): The time when a vertex is first visited during DFS.
2. Lowest Point Reachable (low): The smallest discovery time reachable from a vertex using back edges.
3. Articulation Point Criteria:
  - A non-root vertex is an articulation point if there exists a child such that parent.pre <= child.low.
  - A root vertex is an articulation point if it has more than one child in the DFS tree.

## Code Structure
1. Graph Class:
  - Manages vertices and edges.
  - Adds vertices and connects them via edges.

2. Vertex Class:
  - Stores neighbors and attributes (pre, low, parent, etc.) for articulation point calculation.
  
3. Iterative DFS:
  - Avoids recursion to handle large inputs efficiently.
  - Computes pre, low values and identifies articulation points.

4. Main Function:
  - Reads input data.
  - Builds the graph and performs DFS.
  - Outputs sorted articulation points or  if none exist.


### Usage
Provide an input through standard input in the specified format. The code will output articulation points sorted in ascending order.

## Example
Input should look like
'5 5
0 1
0 2
0 3
1 4
2 3 '

and the output will be like
'0 1'


## Testing
To test the solution:
1. Place articulation_point.py (solution file) in the same folder as test_runner.py and the Tests folder.
2. Run the command:
'python test_runner.py -script articulation_point.py -test_nb 1'
to test a single test or
'python test_runner.py -script articulation_point.py'
to test all the tests in the Tests file. Of course, based on your computer, use python or python3.
