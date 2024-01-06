import queue
import numpy as np
import networkx as nx

### FUNCTIONALITY 1 ###
def funct_1(G,G_name):
    '''
    input
    G: the input graph
    G_name: 'citation' or 'collaboration'
    
    output
    nodes: list of nodes of G
    edges: list of edges of G
    density: float that is the density of G
    average_deg: float that is the average degree of nodes of G
    hubs: list of nodes of G whose degree is more than 95%
    is_sparse: boolean True if G is sparse, False otherwise
    '''
    nodes = list(G.nodes())
    edges = list(G.edges())
    
    n = len(nodes)  #|V(G)|
    m = len(edges)  #|E(G)|
    
    #Case 1: unweighted and directed graph
    if G_name.lower() == 'citation': 
        #since directed
        density = m/(n*(n-1))
                
    #Case 2: weighted and undirected graph
    elif G_name.lower() == 'collaboration':
        #since undirected
        density = 2*m/(n*(n-1))
        
    is_sparse = False
    #we choose that G is sparse iff density<0.5
    #reference https://www.baeldung.com/cs/graphs-sparse-vs-dense
    if density < 0.5:
        is_sparse = True
        
    #from HSL sum(degree(v)) = 2m
    average_deg = 2*m/n
    
    #Hubs (i.e. nodes whose degree is higher than 95% of degree distro)
    degrees = dict(G.degree())
    degree_values = list(degrees.values())
    percentile_95 = np.percentile(degree_values, 95)
    # If the graph is directed, hubs are stored with paper title and "in" and "out" degrees are included
    if G_name.lower() == 'citation':
        # Find nodes whose degree is above the 95th percentile (named "hubs")
        hubs = [(node,G.nodes[node]['title'],degree) for node, degree in degrees.items() if degree > percentile_95]
        degrees_in = dict(G.in_degree())
        degrees_out = dict(G.out_degree())
        return nodes,edges,density,degrees,degrees_in,degrees_out,average_deg,percentile_95,hubs,is_sparse 
    else:
        hubs = [(node,G.nodes[node]['author_name'],degree) for node, degree in degrees.items() if degree > percentile_95]
    
    return nodes,edges,density,degrees,average_deg,percentile_95,hubs,is_sparse

### NODE ID FINDER ###
def id_finder(G,input_str):
    '''
    Finds a node ID given the author's name of the paper's title
    
    input
    G: input graph
    input_str: input author's name or paper's title
    
    output
    ids: a string containing the id(s) of the respective author/paper
    '''
    if nx.is_directed(G):
        # Stores the ids of papers with a specific title
        ids = [x for x,y in G.nodes(data=True) if y['title']==input_str]
    else:
        # Stores the ids of authors with a specific name
        ids = [x for x,y in G.nodes(data=True) if y['author_name']==input_str]
    return ids

### FUNCTIONALITY 2 ###
def funct_2(G,v,G_name):
    '''
    input
    G: input graph
    v: input node
    G_name: string that can be 'citation' or 'collaboration'
    
    output
    betweenness: float that is the betweenness centrality of the node v in G
    pr: float that  is the PageRank centrality of node v in G
    cc: float that is the ClosenessCentrality of node v in G
    dc: float that is the DegreeCentrality of node v in G
    '''
    try:
        #Case 1: unweighted and directed graph
        if G_name.lower() == 'citation':
        
            #Betweenness Centrality
            #we choose k=1000 node samples in order to estimate this centrality
            betweenness = nx.betweenness_centrality(G, k=1000, normalized=True)[v]
        
            # PageRank centrality 
            pr = nx.pagerank(G)[v]
            
            #Closeness Centrality 
            #wf_improved = True means we're using the Wasserman and Faust improved formula for
            #                                         graphs with more than one connected component.
            cc = nx.closeness_centrality(G, v, wf_improved=True)
        
            #Degree Centrality
            #in the directed case we return a tuple (indegree centrality, outdegree centrality)
            in_deg = nx.in_degree_centrality(G)[v]
            out_deg = nx.out_degree_centrality(G)[v]
            dc = [in_deg,out_deg]
        
        #Case 2: weighted and undirected graph
        if G_name.lower() == 'collaboration':
        
            #Betweenness Centrality
            #we choose k=1000 node samples in order to estimate this centrality
            #in the weighted case, as usual, we give also the weights as input
            betweenness = nx.betweenness_centrality(G, k=1000, normalized=True, weight = 'weight')[v]
        
            # PageRank centrality 
            pr = nx.pagerank(G, weight = 'weight')[v]

            #Closeness Centrality has been computed using weighted shortest path
            cc = nx.closeness_centrality(G, v, distance='weight',wf_improved=True)
        
            #Degree Centrality
            dc = nx.degree_centrality(G)[v]

        return betweenness,pr,cc,dc
    except:
        print('There is no node with the specified ID')
        return None
    
### BFS ALGRITHM TO FIND THE SHORTEST PATH  - NEEDED FOR FUNCTIONALITY 3###
def shortest_path(G,starting_node,finish_node):
    #First check: if the two nodes are not in the graph, we raise an error
    if starting_node not in G.nodes() or finish_node not in G.nodes():
        print("Nodes not in the graph")
        return 1
    #Check if the two nodes are in the same connected component
    #Otherwise we return 1 and print a Error Message
    
    # First of all we find all connected components in the graph
    connected_components = list(nx.connected_components(G))
    
    # Then we search among all these components
    for component in connected_components:
        if starting_node in component and finish_node in component:
            break
    else:
        #Error
        print(f"There is no such path between node {starting_node} and {finish_node}.")
        return [],[]
     
    explored = {}
    previous = {}
    
    for node in G.nodes():
        explored[node] = False
        
    explored[starting_node] = True  
    previous[starting_node] = -1 #just a technical condition
    
    Q = queue.Queue()
    
    #Enque the first node
    Q.put(starting_node)
    
    found_finish_node = False #technical condition
    
    while not Q.empty() and not found_finish_node:
        v = Q.get()
        
        #Go through the neighbors of v
        for u in list(nx.neighbors(G, v)):
            if not explored[u]:
                previous[u] = v
                explored[u] = True
                Q.put(u)
                #If reached the last node of the path, termine the BFS
                if u == finish_node:
                    found_finish_node = True
                    break
    
    #Initialize the shortest path
    path = [finish_node]
    
    #Initialize the paper list    
    papers = []
    
    #Now we iterate through the previous node from the last one
    #to the starting node and store them in a list
    while previous[finish_node] != -1:  #the technical condition above
        #Append the previous node in the list
        path.append(previous[finish_node])
        
        #Append the paper link in the list
        edge_paper = G.get_edge_data(finish_node, previous[finish_node])['paper']
        papers.append(edge_paper)
        
        finish_node = previous[finish_node]
    
    #Return the inverted list, so that we get from the first one (starting_node)
    #to the last one (finish_node)
    return path[::-1],papers[::-1]

### FUNCTIONALITY 3 ###
def funct_3(G,a,a1,an,N):
    '''
    input
    G: the graph data
    a: list that is a sequence of authors [a2,a3,...,an-1]
    a1: starting node
    an: finish node
    N: numerosity of top authors by degree to consider
    
    output
    path: WIP
    papers: WIP
    '''
    #Compute the subgraph of G induced by the top N nodes by degree
    degrees = dict(G.degree())
    sorted_nodes = [k for k, v in sorted(degrees.items(), key=lambda x: x[1], reverse = True)]
    G = G.subgraph(sorted_nodes[:N])
    
    #We add a1 and an in the list to make a complete list of authors
    authors = [a1]
    authors.extend(a)
    authors.append(an)
    
    #Check if all the nodes are in the subgraph
    for node in authors:
        if node not in G.nodes():
            print(f"Node {node} not in the induced subgraph")
            return [],[]
    
    #Initialize the total path list and the total papers list
    path = []
    papers = []
    
    #Call the previous function for each pair sequence in authors list
    for i in range(len(authors)-1):
        pair_path,pair_papers = shortest_path(G,authors[i],authors[i+1])

        #If a pair of authors is not connected
        #End the functionality with error message
        if pair_path == [] or pair_papers == []:
            #print(f"There is no such path between node {authors[i]} and {authors[i+1]}.")
            return [],[]
        #Otherwise we append the previous pair path and pair papers to the corresponding complete lists
        else:
            #To deal with repetitions
            if i == 0:
                path.extend(pair_path)  
            else:    
                path.extend(pair_path[1:]) #It starts from 1 instead of 0 to avoid repetitions
            papers.extend(pair_papers)
    
    return path,papers