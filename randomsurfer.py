import networkx as nx
import random

#read the file
fh=open('./PageRankExampleData/p2p-Gnutella08-mod.txt', 'rb')
G=nx.read_adjlist(fh, create_using=nx.DiGraph())
fh.close()

#get graph size
graphSize = G.number_of_nodes()

dangling = []
for i in range(len(G.adj)): 
    #compute a list of the dangling nodes
    if (len(G.adj[str(i)]) == 0):
        dangling.append(i)
m = 0.15
#initial amount of visited per page
rank = [0] * graphSize
#pick starting node
currentNode = random.randint(0, graphSize - 1)
rank[currentNode] += 1
#Outer loop - how many steps to make
for i in range(10000000): #
    if ((int(currentNode) in dangling) or (random.uniform(0, 1) <= m)):
        currentNode = random.randint(0, graphSize - 1)
    else:
        #get list of adjecent nodes
        key = list(G.adj[str(currentNode)].keys())
        #select random one
        currentNode = key[random.randint(0, len(key)-1)]
    rank[int(currentNode)] += 1
    
d = {}

#sort and print
for index in range(len(rank)):
    d[index] = rank[index]
d2 = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
for key in d2:
    print(key, d2[key]) 