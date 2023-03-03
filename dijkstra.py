import numpy as np

def valid_node(node, gridSize):
    if (node[0] < 0 or node[0] >= gridSize) or (node[1] < 0 or node[1] >= gridSize):
        return False
    return True

def up(node):
    return (node[0]-1,node[1])
def down(node):
    return (node[0]+1,node[1])

def left(node):
    return (node[0],node[1]-1)

def right(node):
    return (node[0],node[1]+1)


def backtrack(initial_node, desired_node, distances):
    # idea start at the last node then choose the least number of steps to go back
    # last node
    path = [desired_node]

    gridSize = distances.shape[0]

    while True:
        # check up down left right - choose the direction that has the least distance
        potential_distances = []
        potential_nodes = []

        directions = [up,down,left,right]

        for direction in directions:
            node = direction(path[-1])
            if valid_node(node, gridSize):
                potential_nodes.append(node)
                potential_distances.append(distances[node[0],node[1]])

        least_distance_index = np.argmin(potential_distances)
        path.append(potential_nodes[least_distance_index])

        if path[-1][0] == initial_node[0] and path[-1][1] == initial_node[1]:
            break
    return list(reversed(path))