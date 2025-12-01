#Javier Solorzano, A01645642
#Luis Fernando Rojo Valdés, A01640584

import heapq

N = 4
maze = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 1]
]

directions = [
    ('D', 1, 0),
    ('R', 0, 1),
    ('U', -1, 0),
    ('L', 0, -1),
]

def heuristic(x, y):
    return abs(N - 1 - x) + abs(N - 1 - y)


def valid(x, y):
    return (
        0 <= x < N and
        0 <= y < N and
        maze[x][y] == 1
    )

def a_star():
    
    pq = []
    heapq.heappush(pq, (0, 0, 0, 0, "", {(0, 0)}))
    
    results = []
    best_cost = float("inf")

    while pq:
        f, g, x, y, path, visited = heapq.heappop(pq)

        if x == N-1 and y == N-1:
            if g <= best_cost:
                best_cost = g
                results.append(path)
            continue

        for move, dx, dy in directions:
            nx, ny = x + dx, y + dy

            if valid(nx, ny) and (nx, ny) not in visited:
                new_g = g + 1
                h = heuristic(nx, ny)
                new_f = new_g + h

                new_visited = visited.copy()
                new_visited.add((nx, ny))

                heapq.heappush(
                    pq,
                    (new_f, new_g, nx, ny, path + move, new_visited)
                )

    return results

paths = a_star()

for p in paths:
    print(p)