import streamlit as st
from collections import defaultdict
import time

class Graph:

	def __init__(self, graph):
		self.graph = graph 
		self. ROW = len(graph)
		

	def BFS(self, s, t, parent):

		visited = [False]*(self.ROW)
		queue = []
		queue.append(s)
		visited[s] = True
		while queue:

			u = queue.pop(0)
			for ind, val in enumerate(self.graph[u]):
				if visited[ind] == False and val > 0:
					queue.append(ind)
					visited[ind] = True
					parent[ind] = u
					if ind == t:
						return True

		return False

	def FordFulkerson(self, source, sink):
		parent = [-1]*(self.ROW)

		max_flow = 0 
		while self.BFS(source, sink, parent) :
			path_flow = float("Inf")
			s = sink
			while(s != source):
				path_flow = min (path_flow, self.graph[parent[s]][s])
				s = parent[s]

			max_flow += path_flow

			v = sink
			while(v != source):
				u = parent[v]
				self.graph[u][v] -= path_flow
				self.graph[v][u] += path_flow
				v = parent[v]

		return max_flow

st.header("Ford Fulkerson")
with st.expander('Example:'):
	st.image('img.png')

n = st.number_input('Enter number of nodes', value=5, placeholder='Enter a number', min_value=2)
e = st.number_input('Enter number of edges', value=5, placeholder='Enter a number', min_value=1)
graph = [[] for i in range(n)]
for i in range(n):
	text = st.text_input(f"Enter weight of each edge from node _{i}_: ",key=i, value="0 "*n)
	if text:
		graph[i] = list(map(int, text.split()))


if graph:
    g = Graph(graph)
    src = st.number_input("Enter source node: ",min_value=0, max_value=n-1)
    sink = st.number_input("Enter sink node", min_value=0, max_value=n-1)
    start = time.time()
    st.subheader(f"The maximum possible flow is {g.FordFulkerson(src, sink)}")
    end = time.time()
    st.write(f"Time taken : {end-start} seconds")
	
