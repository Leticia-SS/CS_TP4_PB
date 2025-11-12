from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, u, v):
        if u in self.graph:
            self.graph[u].append(v)
        else:
            self.graph[u] = [v]

        if v in self.graph:
            self.graph[v].append(u)
        else:
            self.graph[v] = [u]

    def dfs(self, start, end):
        def dfs_helper(current, path, visited):
            if current == end:
                result.append(path[:])
                return

            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs_helper(neighbor, path, visited)
                    path.pop()
                    visited.remove(neighbor)

        if start not in self.graph or end not in self.graph:
            return []

        result = []
        visited = set([start])
        dfs_helper(start, [start], visited)
        return result

    def bfs(self, start, end):
        if start not in self.graph or end not in self.graph:
            return []

        if start == end:
            return [start]

        queue = deque()
        queue.append([start])
        visited = set([start])

        while queue:
            path = queue.popleft()
            node = path[-1]

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    if neighbor == end:
                        return new_path
                    visited.add(neighbor)
                    queue.append(new_path)

        return []


graph = Graph()
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')
graph.add_vertex('D')
graph.add_vertex('E')

graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('B', 'D')
graph.add_edge('C', 'D')
graph.add_edge('C', 'E')
graph.add_edge('D', 'E')

print("DFS de A para D:")
print(graph.dfs('A', 'D'))

print("\nBFS de A para E:")
print(graph.bfs('A', 'E'))