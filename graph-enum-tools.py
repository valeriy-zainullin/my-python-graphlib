import itertools # permutations
import random # randint
import os

def is_connected(num_vertices, edges):
	visited = [False for i in range(num_vertices)]
	def dfs(vertice):
		if visited[vertice]:
			return
		visited[vertice] = True
		for i in range(num_vertices):
			if tuple(sorted([i, vertice])) in edges:
				dfs(i)
	dfs(0)
	if False in visited:
		return False
	return True

def find_cutpoints(num_vertices, edges):
	# Graph is assumed to be connected.
	visited = [False for i in range(num_vertices)]
	time_in = [0 for i in range(num_vertices)]
	min_reachable_time_in = [0 for i in range(num_vertices)]
	global timer
	timer = 0
	cutpoints = set()
	blocks = set()
	# Returns set of edges that were not separated into blocks.
	def dfs(vertice, parent):
		visited[vertice] = True
		global timer
		timer += 1
		time_in[vertice] = timer
		min_reachable_time_in[vertice] = timer
		num_children = 0
		non_separated_edges = set()
		for i in range(num_vertices):
			if tuple(sorted([i, vertice])) in edges:
				if i == parent:
					continue
				if visited[i]:
					min_reachable_time_in[vertice] = min(min_reachable_time_in[vertice], time_in[i])
					continue
				dfs(i, vertice)
				min_reachable_time_in[vertice] = min(min_reachable_time_in[vertice], min_reachable_time_in[i])
				if min_reachable_time_in[i] >= time_in[vertice] and parent != -1:
					cutpoints.add(vertice)
				num_children += 1
		if parent == -1 and num_children > 1:
			cutpoints.add(vertice)
	dfs(0, -1)
	return cutpoints

# https://www.csie.ntu.edu.tw/~hsinmu/courses/_media/dsa_13spring/horowitz_306_311_biconnected.pdf
def find_blocks(num_vertices, edges):
	# Graph is assumed to be connected.
	visited = [False for i in range(num_vertices)]
	time_in = [0 for i in range(num_vertices)]
	min_reachable_time_in = [0 for i in range(num_vertices)]
	global timer
	timer = 0
	blocks = set()
	stack = []
	# Returns set of edges that were not separated into blocks.
	def dfs(vertice, parent):
		visited[vertice] = True
		global timer
		timer += 1
		time_in[vertice] = timer
		min_reachable_time_in[vertice] = timer
		for i in range(num_vertices):
			if tuple(sorted([i, vertice])) in edges:
				if i == parent:
					continue
				stack.append(tuple(sorted([i, vertice])))
				if visited[i]:
					min_reachable_time_in[vertice] = min(min_reachable_time_in[vertice], time_in[i])
					continue
				dfs(i, vertice)
				min_reachable_time_in[vertice] = min(min_reachable_time_in[vertice], min_reachable_time_in[i])
				if min_reachable_time_in[i] >= time_in[vertice]:
					block = set()
					while stack[-1] != tuple(sorted([i, vertice])):
						block.add(stack[-1])
						del stack[-1]
					block.add(stack[-1])
					del stack[-1]
					blocks.add(tuple(sorted(list(block))))
	dfs(0, -1)
	return blocks

	
def are_isomorphic(num_vertices, edges_first, edges_second):
	for permutation in itertools.permutations(list(range(0, num_vertices))):
		wrong_permutation = False
		for edge_first in edges_first:
			if tuple(sorted([permutation[edge_first[0]], permutation[edge_first[1]]])) not in edges_second:
				wrong_permutation = True
				break
		inverse_permutation = [0 for i in range(num_vertices)]
		for i in range(len(permutation)):
			inverse_permutation[permutation[i]] = i
		for edge_second in edges_second:
			if tuple(sorted([inverse_permutation[edge_second[0]], inverse_permutation[edge_second[1]]])) not in edges_first:
				wrong_permutation = True
				break
		if not wrong_permutation:
			# print(permutation)
			return True
	return False

def delete_isomorphic_duplicates(num_vertices, graphs):
	cur_graph = 0
	total_graphs = len(graphs)
	while cur_graph < len(graphs):
		print("\rcur_graph = %d, len(graphs) = %d, done %.0f%%." % (cur_graph, len(graphs), ((total_graphs - len(graphs)) + cur_graph) / total_graphs * 100), end='')
		is_duplicate = False
		for i in range(cur_graph):
			if are_isomorphic(num_vertices, graphs[i], graphs[cur_graph]):
				del graphs[cur_graph]
				is_duplicate = True
				break
		if not is_duplicate:
			# dump_graph("new_3blocks_nonisomorphic.png", num_vertices, graphs[cur_graph])
			# input()
			cur_graph += 1
	print()
	return graphs
				

num_graphs = 0
	
num_vertices = 6
max_num_edges = num_vertices * (num_vertices - 1) // 2
edges_overset = []
for vert_from in range(num_vertices):
	for vert_to in range(vert_from + 1, num_vertices):
		edges_overset.append((vert_from, vert_to))
assert len(edges_overset) == max_num_edges

def dump_graph(filename, num_vertices, edges):
	with open(filename + ".dot", 'w') as stream:
		stream.write("graph G {\n");
		stream.write("node [shape=circle];\n")
		for edge in edges:
			stream.write("n%d -- n%d\n" % (edge[0], edge[1]))
		stream.write("}\n")
	os.system("dot -T%s %s > %s" % (filename.split('.')[1], filename + ".dot", filename))
	os.system("xdg-open %s" % filename)
def print_adj_matrix(num_vertices, edges):
	adj_vertices = [[0 for i in range(num_vertices)] for j in range(num_vertices)]
	for edge in edges:
		adj_vertices[edge[0]][edge[1]] = 1
		adj_vertices[edge[1]][edge[0]] = 1
	print(adj_vertices)
	
def gen_random_graph(num_vertices, max_num_edges=num_vertices * (num_vertices - 1) // 2):
	num_edges = random.randint(num_vertices, max_num_edges)
	edges = set()
	while len(edges) < num_edges:
		vert_from = random.randint(0, num_vertices - 1)
		vert_to = random.randint(0, num_vertices - 1)
		if vert_from == vert_to:
			continue
		candidate = tuple(sorted([vert_from, vert_to]))
		if candidate in edges:
			continue
		edges.add(candidate)
	return edges
	
def is_eulerian(num_vertices, edges):
	for i in range(num_vertices):
		num_adj_vertices = 0
		for j in range(num_vertices):
			if tuple(sorted([i, j])) in edges:
				num_adj_vertices += 1
		if num_adj_vertices % 2 == 1:
			return False
	if not is_connected(num_vertices, edges):
		return False
	return True

def is_hamiltonian(num_vertices, edges):
	if len(edges) >= 2 + (num_vertices - 1) * (num_vertices - 2) // 2:
		# With this many edges graph is hamiltonian already.
		# https://math.stackexchange.com/questions/1597503/prove-that-a-graph-with-p-vertices-and-2p-1p-2-2-edges-is-hamiltonian
		return True
	global result_path
	result_path = []
	def find_hamiltonian_cycle(path):
		# print(path)
		if len(path) == num_vertices:
			if tuple(sorted([path[-1], path[0]])) in edges:
				global result_path
				result_path = path
				return True
			return False
		for i in range(num_vertices):
			if i not in path and tuple(sorted([i, path[-1]])) in edges:
				if find_hamiltonian_cycle(path + [i]):
					return True
		return False
	return find_hamiltonian_cycle([0])

graphs = []
for edge_mask in range(2 ** max_num_edges):
	edges = []
	for i in range(max_num_edges):
		if edge_mask & (1 << i) != 0:
			edges.append(edges_overset[i])
	if not is_connected(num_vertices, edges):
		continue
	cutpoints = find_cutpoints(num_vertices, edges)
	num_cutpoints = len(cutpoints)
	blocks = find_blocks(num_vertices, edges)
	num_blocks = len(blocks)
	if num_blocks != 3:
		continue
	#if edge_mask % 5 == 0:
	#	dump_graph("3blocks.png", num_vertices, edges)
	#	exit(0)
	graphs.append(edges)
graphs = delete_isomorphic_duplicates(num_vertices, graphs)

print(len(graphs))
for index, graph in enumerate(graphs):
	dump_graph("graph_3blocks_%dcutpoints_%dmaxblock_%d.png" % (len(find_cutpoints(num_vertices, graph)), max(map(len, find_blocks(num_vertices, graph))), index), num_vertices, graph)

num_vertices = 6
edges = gen_random_graph(num_vertices, max_num_edges=8)
while not is_hamiltonian(num_vertices, edges):
	edges = gen_random_graph(num_vertices, max_num_edges=8)
print(find_cutpoints(num_vertices, edges))
print(find_blocks(num_vertices, edges))
dump_graph("random-hamiltonian-graph.png", num_vertices, edges)

num_vertices = 6
max_num_tries = 30
edges = gen_random_graph(num_vertices, max_num_edges=8)
for try_index in range(max_num_tries):
	if not is_eulerian(num_vertices, edges):
		edges = gen_random_graph(num_vertices, max_num_edges=8)
if not is_eulerian(num_vertices, edges):
	print("Couldn't find random eulerian graph.")
else:
	print(find_cutpoints(num_vertices, edges))
	print(find_blocks(num_vertices, edges))
	dump_graph("random-eulerian-graph.png", num_vertices, edges)
