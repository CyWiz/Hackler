import math

''' Challenge link : https://www.hackerrank.com/challenges/kingdom-connectivity'''

n,m = [int(v) for v in raw_input().strip().split()]
graph = {key:[] for key in xrange(1,n+1)}
for i in xrange(m):
	a,b = [int(v) for v in raw_input().strip().split()]
	graph[a].append(b)

# The first idea here is to build a new graph from the SCCs of the old using Tarjan's algorithm. Can be found 
# here : https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm

#book keeping
index = 0
stack = []
index_database = {}  #this will contain the ID of each SCC and the edges. Having the edges will help
					 #us construct the new graph
on_stack = {}

def strongly_connect(v):
	''' modified version of DFS '''
	global index, on_stack, index_database
	index_database[v] = ([index,index], []) #first is index, second is lowling or the component index
	index += 1
	stack.append(v)
	on_stack[v] = True

	for edge in graph[v]:
		if not (edge in index_database):
			strongly_connect(edge)
			index_database[v][0][1] = min(index_database[v][0][1], index_database[edge][0][1])
		elif edge in on_stack and on_stack[edge]:
			index_database[v][0][1] = min(index_database[v][0][1], index_database[edge][0][1])
		index_database[v][1].append(edge)

	if index_database[v][0][0] == index_database[v][0][1]:
		w = None
		while w != v:
			w = stack.pop()
			on_stack[w] = False

for v in graph:
	if not (v in index_database):
		strongly_connect(v)

#what do we need to do now
# Q. Figure out how to construct the new graph G' and what info is going in it (how do we represent SCC)
#
# A: iterate over the keys of the index_database and let the first new SCC be the root.
# 		Every other element from the same SCC will just increment a counter, this way
#		we can check afterwards if the given G' vertex is a cycle or not.
#
# Q. How do we check if an SCC identifier has already been inserted in the graph ?
# A: Using a hash table to keep track of the already used identifiers
#

scc_graph = {}				#will be of the form root : [counter, hash table for the edges?]
already_in_scc = {}			#will be of the form identifier : root
for v in index_database:
	identifier = index_database[v][0][1]
	if identifier in already_in_scc:
		root = already_in_scc[identifier]
		scc_graph[root][0] += 1
		for edge in index_database[v][1]:
			#check to see if the edge is actually in the same SCC
			if index_database[edge][0][1] != identifier:
				scc_graph[root][1].append(edge)
	# we have not yet seen components of that SCC
	else:
		already_in_scc[identifier] = v
		#the counter to check for cycles and the list for the outgoing edges
		scc_graph[v] = [1,[]]