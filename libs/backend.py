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

### FUNCTIONALITY 2 ### - BIG WIP
def funct_2(G,v,G_name):
    '''
    input
    G: input graph
    v: input node
    G_name: string that can be 'citation' or 'collaboration'
    
    output:
    betweenness: float that is the betweenness centrality of the node v in G
    pr: float that  is the PageRank centrality of node v in G
    cc: float that is the ClosenessCentrality ...
    dc: float that is the DegreeCentrality ...
    '''
    betweenness_centrality_subset(G, sources, targets, normalized=False, weight=None) # WIP - FUNCTION MISSING
    #Case 1: unweighted and directed graph
    if G_name.lower() == 'citation':
        
        #Betweenness Centrality
        #we choose k=1000 node samples in order to estimate this centrality
        betweenness = nx.betweenness_centrality(citation_graph, k=1000, normalized=True)[v]
        
        # PageRank centrality 
        pr = nx.pagerank(collaboration_graph, personalization={node_of_interest: 1})[v]
        
        #Closeness Centrality 
        #wf_improved = True means we're using the Wasserman and Faust improved formula for
        #                                         graphs with more than one connected component.
        cc = nx.closeness_centrality(G, v, wf_improved=True)
        
        #Degree Centrality
        #in the directed case we return a tuple (indegree centrality, outdegree centrality)
        in_deg = nx.in_degree_centrality(G)[v]
        out_deg = nx.out_degree_centrality(G)[v]
        dc = (in_deg,out_deg)

        
    #Case 2: weighted and undirected graph
    if G_name.lower() == 'collaboration':
        
        #Betweenness Centrality
        #we choose k=1000 node samples in order to estimate this centrality
        #in the weighted case, as usual, we give also the weights as input
        betweenness = nx.betweenness_centrality(citation_graph, k=1000, normalized=True, weight = 'weight')[v]
        
        # PageRank centrality 
        pr = nx.pagerank(collaboration_graph, personalization={node_of_interest: 1}, weight = 'weight')[v]

        #Closeness Centrality has been computed using weighted shortest path
        cc = nx.closeness_centrality(G, v, distance='weight',wf_improved=True)
        
        #Degree Centrality
        dc = nx.degree_centrality(G)[v]

    
    
    return cc,dc # WIP - OUTPUT MISSING