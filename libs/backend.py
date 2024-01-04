import numpy as np

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
    # Find nodes whose degree is above the 95th percentile (named "hubs")
    hubs = [(node,degree) for node, degree in degrees.items() if degree > percentile_95]
    
    # If the graph is directed, also "in" and "out" degrees are returned
    if G_name.lower() == 'citation':
        degrees_in = dict(G.in_degree())
        degrees_out = dict(G.out_degree())
        return nodes,edges,density,degrees,degrees_in,degrees_out,average_deg,percentile_95,hubs,is_sparse 
    
    return nodes,edges,density,degrees,average_deg,percentile_95,hubs,is_sparse
