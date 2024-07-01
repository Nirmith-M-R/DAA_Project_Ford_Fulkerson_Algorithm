import time
import streamlit as st

path_dfs = []
flow_dfs = []
path_bfs = []
flow_bfs = []

class Graph_DFS:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, c):
        self.adj_matrix[u][v] = c

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dfs(self, s, t, visited=None, path=None):
        if visited is None:
            visited = [False] * self.size
        if path is None:
            path = []

        visited[s] = True
        path.append(s)

        if s == t:
            return path

        for ind, val in enumerate(self.adj_matrix[s]):
            if not visited[ind] and val > 0:
                result_path = self.dfs(ind, t, visited, path.copy())
                if result_path:
                    return result_path

        return None

    def fordFulkerson(self, source, sink):
        max_flow = 0

        path = self.dfs(source, sink)
        while path:
            path_flow = float("Inf")
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                path_flow = min(path_flow, self.adj_matrix[u][v])

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.adj_matrix[u][v] -= path_flow
                self.adj_matrix[v][u] += path_flow

            max_flow += path_flow

            path_names = [self.vertex_data[node] for node in path]
            # print("Path:", " -> ".join(path_names), ", Flow:", path_flow)
            path_dfs.append(" -> ".join(path_names))
            flow_dfs.append(path_flow)

            path = self.dfs(source, sink)

        return max_flow


class Graph_BFS:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, c):
        self.adj_matrix[u][v] = c

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def bfs(self, s, t, parent):
        visited = [False] * self.size
        queue = []  # Using list as a queue
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)  # Pop from the start of the list

            for ind, val in enumerate(self.adj_matrix[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return visited[t]

    def edmonds_karp(self, source, sink):
        parent = [-1] * self.size
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.adj_matrix[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink
            while(v != source):
                u = parent[v]
                self.adj_matrix[u][v] -= path_flow
                self.adj_matrix[v][u] += path_flow
                v = parent[v]

            path = []
            v = sink
            while(v != source):
                path.append(v)
                v = parent[v]
            path.append(source)
            path.reverse()
            path_names = [self.vertex_data[node] for node in path]
            # print("Path:", " -> ".join(path_names), ", Flow:", path_flow)
            path_bfs.append(" -> ".join(path_names))
            flow_bfs.append(path_flow)

        return max_flow
    
st.header("Ford Fulkerson")
with st.expander('Example:'):
	st.image('img.png')

n = st.number_input('Enter number of nodes', value=5, placeholder='Enter a number', min_value=2)
e = st.number_input('Enter number of edges', value=5, placeholder='Enter a number', min_value=1)

g_dfs = Graph_DFS(n)
g_bfs = Graph_BFS(n)

vertex_names = ['']*n
for i in range(n):
    vertex_names[i] = st.text_input(f"Name of Vertex {i}: ")

for i, name in enumerate(vertex_names):
    g_dfs.add_vertex_data(i, name)
    g_bfs.add_vertex_data(i, name)

g = ['']*e
col1, col2, col3 = st.columns(3)
for i in range(e):
    u,v,w = 0,0,0
    with col1:
        u = st.number_input("u:",key = f'1{i}', min_value=0)
    
    with col2:
        v = st.number_input("v:", key = f'2{i}', min_value=0)
    
    with col3:
        w = st.number_input("Flow:", key = f'3{i}', min_value=0)
    
    g[i] = [u,v,w]

src = st.number_input("Enter source node: ",min_value=0, max_value=n-1)
sink = st.number_input("Enter sink node", min_value=0, max_value=n-1)

submit = False
submit = st.button("Enter")
if submit:
    for i in g:
        g_dfs.add_edge(i[0],i[1],i[2])
        g_bfs.add_edge(i[0],i[1],i[2])
    st.header("Using DFS approach :")
    start = time.time()
    st.subheader(f"The maximum possible flow is {g_dfs.fordFulkerson(src, sink)}")
    end = time.time()
    st.write(f"Time taken : {end-start} seconds")
    st.subheader("Path Flow: ")
    for i in range(len(path_dfs)):
        st.write("Path: ",path_dfs[i], " Flow: ",str(flow_dfs[i]))
    st.header("Using BFS approach :")
    start1 = time.time()
    st.subheader(f"The maximum possible flow is {g_bfs.edmonds_karp(src, sink)}")
    end1 = time.time()
    st.write(f"Time taken : {end1-start1} seconds")
    st.subheader("Path Flow: ")
    for i in range(len(path_bfs)):
        st.write("Path: ",path_bfs[i], " Flow: ",str(flow_bfs[i]))

