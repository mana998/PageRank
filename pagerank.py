import networkx as nx

#read the file
fh=open('./PageRankExampleData/medium.txt', 'rb')
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
#calculated Sx on the paper
#create 1dimensional matrix with values 1/graphSize and graphSize number of rows
Sx = [1/graphSize] * graphSize
#xk1 = x0
#the initial approximation of the ranking vector
xk1 = [1/graphSize] * graphSize
#Outer loop The next step is to make a loop where each step computes xk+1 from xk. Start by constructing a new variable to hold xk+1
for i in range(10000):
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
for key in d2:
    print(key, d2[key]) 