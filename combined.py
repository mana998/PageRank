import networkx as nx
import random

def randomsurfer(G, graphSize, dangling, m, limit = 0):

    #initial amount of visited per page
    rank = [0] * graphSize
    #pick starting node
    currentNode = random.randint(0, graphSize - 1)
    rank[currentNode] += 1
    #Outer loop - how many steps to make
    for i in range(10000): #
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
    count = 0
    for key in d2:
        print(key, d2[key]) 
        count += 1
        if (count == limit): break


def pagerank(G, reverseG, graphSize, dangling, branching, m, limit = 0):
    #calculated Sx on the paper
    #create 1dimensional matrix with values 1/graphSize and graphSize number of rows
    Sx = [1/graphSize] * graphSize
    #xk1 = x0
    #the initial approximation of the ranking vector
    xk1 = [1/graphSize] * graphSize
    #Outer loop The next step is to make a loop where each step computes xk+1 from xk. Start by constructing a new variable to hold xk+1
    for i in range(1000):
        #calculate Dx matrix
        Dxk = 0
        for index in dangling:
            Dxk += (1/graphSize) * xk1[index]
        #calculate Ax matrix
        Axk = []
        for node in range(len(G.adj)):
            #print(reverseG.adj[str(i)])
            rank = 0
            #print('node', node)
            for adjecent in (reverseG.adj[str(node)]):
                rank += (1/branching[int(adjecent)])*xk1[int(adjecent)]
            #rank -= int(xk1[node])
            Axk.append(rank)
        #use formula to calculate xk+1
        for index in range(len(xk1)):
            xk1[index] = (1-m)*Axk[index] + (1-m)*Dxk + m*Sx[index]
            #xk+1 = (1-m)Axk + (1-m)Dxk +mSxk 
    #sort and print
    d = {}
    for index in range(len(xk1)):
        d[index] = xk1[index]
    d2 = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
    count = 0
    for key in d2:
        print(key, d2[key]) 
        count += 1
        if (count == limit): break


#read the file
fh=open('./PageRankExampleData/p2p-Gnutella08-mod.txt', 'rb')
G=nx.read_adjlist(fh, create_using=nx.DiGraph())
fh.close()

#get graph size
graphSize = G.number_of_nodes()
#get reversed graph
reverseG = nx.reverse(G, True)

#an array branching such that branching[i] is the number of nodes linked to from node i.
branching = []
dangling = []
for i in range(len(G.adj)): 
    branching.append(len(G.adj[str(i)]))
    #compute a list of the dangling nodes
    if (len(G.adj[str(i)]) == 0):
        dangling.append(i)
m = 0.15

#use to limit output, if not passed or set to 0, everything will be printed
limit = 10
print("Random surfer:")
randomsurfer(G, graphSize, dangling, m, limit)
print("Pagerank:")
pagerank(G, reverseG, graphSize, dangling, branching, m, limit)