from __future__ import print_function #have to use this so can print to sys.stderr
import sys
import os
import zlib

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
            print(branches_dict[commit])
                
        else: #is directory
            find_heads_branches(path_temp, nodes, branches_dict, graph, stack_nodes)

def find_parent_nodes(commit): #find IDs of parent nodes
    parents = []
    contents = commit.splitlines()
    for line in contents:
        if ("parent" in line):
            parents.append(line.split()[1])

    return parents


# #TEST CASES===============================================================================================================================
print("TEST SEARCH FOR .git REPO===========================================================================================================")
print(find_git_repo("/u/cs/ugrad/arthurz/Desktop/UCLA CS Classes/CS35L/Assignment6"))
print(find_git_repo("/u/cs/ugrad/arthurz/Desktop/UCLA CS Classes/CS35L"))
print(find_git_repo("/u/cs/ugrad/arthurz/Desktop/UCLA CS Classes/"))
# print(find_git_repo("/u/cs/ugrad/")) #have to comment this out to run everything else or else will exit program

print("\nTEST TO SEARCH FOR HEADS AND BRANCHES=============================================================================================")
path = find_git_repo(os.getcwd()) + "/.git/refs/heads"
nodes = {} #dictionary of all nodes, hash string:node
branches_dict = {} #dictionary of branches, commit hash:list of branch names
graph = {}
stack_nodes = [] #stack of nodes to dfs
find_heads_branches(path, nodes, branches_dict, graph, stack_nodes)

print("\nTEST TO SEARCH FOR PARENTS==========================================================================================================")
cur_hash = stack_nodes.pop()
file = find_git_repo(os.getcwd()) + "/.git/objects/" + cur_hash[:2] + "/" + cur_hash[2:]
file_reader_binary = open(file, 'rb')
