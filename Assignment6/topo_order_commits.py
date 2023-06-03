# from __future__ import print_function #have to use this so can print to sys.stderr
import sys
import os
import zlib

#strace: ran the code with the command strace -f python3 topo_order_commits.py to make sure no git commands were invoked. The output was directed to 
#grep 'execve\("\/usr\/local\/cs\/bin' to make sure nothing called git

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

def find_git_repo(path):
    while (path): #if path is empty it's false
        files = os.listdir(path)
        if ('.git' in files):
            return path
        prev_slash = path.rfind('/')
        path = path[0:prev_slash] #thank you physics 4AL for teaching me this
    
    print("Not inside a Git repository", file = sys.stderr)
    exit(1)

def find_heads_branches(path, nodes, branches_dict, graph, stack_nodes): #dfs recursive search for heads and populate branches
    files = os.listdir(path)
    for head in files:
        path_temp = path + "/" + head
        if (os.path.isfile(path_temp)): #is file
            commit = open(path_temp).read().strip() #opens and reads file
            stack_nodes.append(commit)
            cur_node = CommitNode(commit)
            cur_node_temp = CommitNode(commit)
            nodes[commit] = cur_node
            graph[commit] = cur_node_temp

            branch_name = path_temp[path_temp.index('heads') + 6: ]
            if (commit in branches_dict): #add branch names if they aren't in dictionary
                if (branch_name not in branches_dict[commit]):
                    branches_dict[commit].append(branch_name)
            else: #add commit hash
                branches_dict[commit] = [branch_name]
            # print(branches_dict[commit])
        else: #is directory
            find_heads_branches(path_temp, nodes, branches_dict, graph, stack_nodes)

def find_parent_nodes(commit): #find IDs of parent nodes
    parents = []
    contents = commit.splitlines()
    for line in contents:
        if ("parent" in line):
            parents.append(line.split()[1])

    return parents

def build_graph(path, nodes, visited_nodes, branches_dict, graph, stack_nodes):
    find_heads_branches(path + "/.git/refs/heads", nodes, branches_dict, graph, stack_nodes)
    
    #build graph
    while (stack_nodes):
        cur_hash = stack_nodes.pop()
        # print("cur_hash: " + cur_hash)
        if (cur_hash in visited_nodes):
            continue
        visited_nodes.add(cur_hash)
        cur_node = nodes[cur_hash]
        cur_node_clone = graph[cur_hash] #backup copy
        
        file = path + "/.git/objects/" + cur_hash[:2] + "/" + cur_hash[2:]
        # print("file: " + file)
        fr_binary = open(file, 'rb')
        commit_contents = (zlib.decompress(fr_binary.read())).decode('utf-8')
        parents = find_parent_nodes(commit_contents)
        fr_binary.close()

        #initialize parent nodes and update child/parent relations
        if (parents): 
            for p in parents: # p is a commit_hash
                parent_node = None
                parent_node_temp = None
                if (p in nodes):
                    parent_node = nodes[p]
                    parent_node_temp = graph[p]
                else:
                    parent_node = CommitNode(p)
                    parent_node_temp = CommitNode(p)
                    nodes[p] = parent_node
                    graph[p] = parent_node_temp

                if (p not in visited_nodes):
                    stack_nodes.append(p)

                parent_node.children.add(cur_hash)
                parent_node_temp.children.add(cur_hash)
                cur_node.parents.add(p)
                cur_node_clone.parents.add(p)

def topo_sort(nodes, graph):
    topo_sorted = []
    node_sinks = [] #node hash strings with no outgoing edges

    for node in graph:
        if (len(graph[node].children) == 0):
            node_sinks.append(node)
        
    while (node_sinks):
        cur_hash = node_sinks.pop(0)
        cur_node = graph[cur_hash]
        topo_sorted.append(cur_hash)

        for parent_hash in cur_node.parents:
            parent_node = graph[parent_hash]
            parent_node.children.remove(cur_hash)
            if (len(parent_node.children) == 0):
                node_sinks.append(parent_hash)
    
    if (len(topo_sorted) < len(nodes)):
        raise Exception("Cycle detected")
        # print("Cycle detected", file = sys.stderr)
        exit(1)

    return topo_sorted

def print_graph(nodes, branches_dict, sorted_graph):
    jump = False

    for i in range(len(sorted_graph)):
        cur_hash = sorted_graph[i]
        cur_node = nodes[cur_hash]

        if jump:
            jump = False
            if (cur_node.children == None):
                sticky_end = ''.join(cur_node.children)
            else:
                sticky_end = ' '.join(cur_node.children)
            print(f"={sticky_end}")

        if cur_hash in branches_dict:
            branch_names = sorted(branches_dict[cur_hash])
            print(cur_hash + (' ' + ' '.join(branch_names)))
        else:
            print(cur_hash)

        if (i + 1 < len(sorted_graph)):
            next_hash = sorted_graph[i + 1]
            if (next_hash not in cur_node.parents):
                jump = True
                sticky_start = ' '.join(cur_node.parents)
                print(f"{sticky_start}=\n")

# #TEST CASES===============================================================================================================================
# print("TEST SEARCH FOR .git REPO===========================================================================================================")
# print(find_git_repo("/u/cs/ugrad/arthurz/Desktop/UCLA CS Classes/CS35L/Assignment6"))
# print(find_git_repo("/u/cs/ugrad/arthurz/Desktop/UCLA CS Classes/CS35L"))
# print(find_git_repo("/u/cs/ugrad/arthurz/Desktop/UCLA CS Classes/"))
# # print(find_git_repo("/u/cs/ugrad/")) #have to comment this out to run everything else or else will exit program

# print("\nTEST TO SEARCH FOR HEADS AND BRANCHES=============================================================================================")
# path = find_git_repo(os.getcwd()) + "/.git/refs/heads"
# nodes = {} #dictionary of all nodes, hash string:node
# branches_dict = {} #dictionary of branches, commit hash:list of branch names
# graph = {}
# stack_nodes = [] #stack of nodes to dfs
# find_heads_branches(path, nodes, branches_dict, graph, stack_nodes)

# print("\nTEST TO SEARCH FOR PARENTS==========================================================================================================")
# cur_hash = stack_nodes.pop()
# file = find_git_repo(os.getcwd()) + "/.git/objects/" + cur_hash[:2] + "/" + cur_hash[2:]
# file_reader_binary = open(file, 'rb')
# commit_contents = (zlib.decompress(file_reader_binary.read())).decode('utf-8')
# parents = find_parent_nodes(commit_contents)
# print(parents)
# file_reader_binary.close()

path = find_git_repo(os.getcwd())
git_refs_heads_path = path + "/.git/refs/heads"
nodes = {} #dictionary of all nodes, hash string:node
visited_nodes = set() #sets dont have dupes
branches_dict = {} #dictionary of branches, commit hash:list of branch names
graph = {}
stack_nodes = [] #stack of nodes to dfs

find_heads_branches(git_refs_heads_path, nodes, branches_dict, graph, stack_nodes)
build_graph(path, nodes, visited_nodes, branches_dict, graph, stack_nodes)
sorted_graph = topo_sort(nodes, graph)
print_graph(nodes, branches_dict, sorted_graph)