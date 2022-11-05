import networkx as nx

#read the file
fh=open('./PageRankExampleData/pg.txt', 'rb')
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
for i in range(10000): #
    Dxk = 0
    #xk1 = x0
    for index in dangling:
        Dxk += (1/graphSize) * xk1[index]
    #Dxk = len(dangling)/graphSize * xk
    #xk1 = x0
    Axk = []
    for node in range(len(G.adj)):
        #print(reverseG.adj[str(i)])
        rank = 0
        #print('node', node)
        for adjecent in (reverseG.adj[str(node)]):
            #print('adjecent',adjecent)
            #print('value',branching[int(adjecent)])
            #print(len(reverseG.adj[str(adjecent)]))
            rank += (1/branching[int(adjecent)])*xk1[int(adjecent)]
            #rank += 1/len(reverseG.adj[str(adjecent)])
            #print('RANK',rank)
        Axk.append(rank)
        #print('ORANK',rank)
    for index in range(len(xk1)):
        xk1[index] = (1-m)*Axk[index] + (1-m)*Dxk + m*Sx[index]
        #xk+1 = (1-m)Axk + (1-m)Dxk +mSxk 
d = {}
sum = 0
for index in range(len(xk1)):
    sum += xk1[index]
print(sum)
for index in range(len(xk1)):
    d[index] = xk1[index]
d2 = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
arr1 = []
for key in d2:
    print(key, d2[key]) 
    arr1.append(key)
pr = nx.pagerank(G, 0.15, None, 10000)
pr = dict(sorted(pr.items(), key=lambda item: item[1], reverse=True))
print('\n')
arr2 = []
for key in pr:
    print(key, pr[key]) 
    arr2.append(key)
for i in range(len(arr1)):
    if (int(arr1[i]) != int(arr2[i])):
        print('nope', i)
        break