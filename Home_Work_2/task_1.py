from collections import deque, defaultdict

edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),

    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),

    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),

    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),

    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

SOURCE = "Джерело"
SINK = "Сток"
INF = 10**9

graph = defaultdict(list)
capacity = defaultdict(int)
original_capacity = {}

def add_edge(u, v, c):
    graph[u].append(v)
    graph[v].append(u)
    capacity[(u, v)] += c
    capacity[(v, u)] += 0
    original_capacity[(u, v)] = c

add_edge(SOURCE, "Термінал 1", INF)
add_edge(SOURCE, "Термінал 2", INF)

for u, v, c in edges:
    add_edge(u, v, c)

for i in range(1, 15):
    add_edge(f"Магазин {i}", SINK, INF)

def bfs(parent):
    visited = {SOURCE}
    queue = deque([SOURCE])

    while queue:
        u = queue.popleft()

        for v in graph[u]:
            if v not in visited and capacity[(u, v)] > 0:
                visited.add(v)
                parent[v] = u

                if v == SINK:
                    return True

                queue.append(v)

    return False

def edmonds_karp():
    max_flow = 0
    steps = []

    while True:
        parent = {}

        if not bfs(parent):
            break

        path_flow = INF
        v = SINK
        path = []

        while v != SOURCE:
            u = parent[v]
            path_flow = min(path_flow, capacity[(u, v)])
            path.append((u, v))
            v = u

        path.reverse()

        for u, v in path:
            capacity[(u, v)] -= path_flow
            capacity[(v, u)] += path_flow

        max_flow += path_flow
        steps.append((path, path_flow))

    return max_flow, steps

max_flow, steps = edmonds_karp()

print("Максимальний потік:", max_flow)
print("\nКроки алгоритму:")
for i, (path, flow) in enumerate(steps, 1):
    route = " -> ".join([path[0][0]] + [v for _, v in path])
    print(f"{i}. {route}: {flow}")

print("\nФактичні потоки по ребрах:")
for u, v, c in edges:
    used_flow = original_capacity[(u, v)] - capacity[(u, v)]
    print(f"{u} -> {v}: {used_flow}")