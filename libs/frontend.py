from .backend import *
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import networkx as nx
from IPython.display import display
from itables import show

### FUNCTIONALITY 1 VISUALIZATION ###
def visual_1(G,k):
    '''
    Prints two tables, showing informations about the graph and the list of the hub nodes. 
    One or two plots are displayed, based on the type of graph:
    - If the graph chosen is "collaboration", one plot with the top k authors by number of collaborations is displayed
    - If the graph chosen is "citation", the distributions of the "in" and "out" degrees are displayed in two separate plots
    
    input
    G: the input graph
    k: number of top authors to display in plots. Defaults to 20.
    
    output
    None
    ''' 
    # --- First two tables ---
    # Case 1: unweighted and directed graph
    if nx.is_directed(G):
        G_name = 'citation'
        # Apply functionality 1 to retrieve needed data
        n, e, dens, degs, degs_in, degs_out, avg_deg, perc_95, hubs, is_sparse = funct_1(G, G_name)
        # Store hubs info in pandas dataframe
        degs_in_df = pd.DataFrame(degs_in.items(), columns = ['ID', 'In Degree'])
        degs_out_df = pd.DataFrame(degs_out.items(), columns = ['ID', 'Out Degree'])
        degs_in_out_df = degs_in_df.merge(degs_out_df, how = 'inner', on = 'ID')
        hubs_df = pd.DataFrame(hubs, columns = ['ID', 'Title','Degree'])
        hubs_info = degs_in_out_df.merge(hubs_df, how = 'inner', on = 'ID').sort_values('Degree', ascending = False)
        hubs_info = hubs_info.reindex(['ID', 'Title','Degree','In Degree','Out Degree'], axis=1)
        
    # Case 2: weighted and undirected graph - "in" and "out" degree are included in the analysis
    else:
        G_name = 'collaboration'
        # Apply functionality 1 to retrieve needed data
        n, e, dens, degs, avg_deg, perc_95, hubs, is_sparse = funct_1(G, G_name)
        # Store hubs info in pandas dataframe
        hubs_info = pd.DataFrame(hubs, columns = ['ID', 'Name', 'Degree']).sort_values('Degree', ascending = False)
    
    # Store graph info in pandas dataframe
    colnames = ['Number of Nodes', 'Number of Edges', 'Density', 'Average Degree', 'Is Sparse']
    graph_info = pd.DataFrame(np.array([[len(n), len(e), round(dens,4), round(avg_deg,3), is_sparse]]), columns = colnames)
    graph_info['Is Sparse'] = graph_info['Is Sparse'].astype('bool') 
    
    # Change dataframes style to display prettier tables
    graph_info_stl = graph_info.style\
    .set_caption(G_name.capitalize() + ' Graph Properties')\
    .set_properties(**{'text-align':'center'})\
    .map(lambda x: 'color: green;' if x == True else 'color: red;',subset = ['Is Sparse'])\
    .set_table_styles([{
     'selector': 'caption',
     'props': 'caption-side: top; font-size: 24px; text-align: center; color: black; font-weight: bold'
     },{
     'selector': 'th',
     'props': 'font-size: 14px; text-align: center'
     },{
     'selector': 'td',
     'props': 'font-size: 14px'
     }], overwrite = False)\
    .format(
      {
        'Number of Nodes':'{:,.0f}',
        'Number of Edges':'{:,.0f}',
        'Density':'{:.3f}',
        'Average Degree':'{:.3f}'
      }
    )\
    .hide(axis = 'index')
    
    hubs_info_stl = hubs_info.style\
    .set_caption(G_name.capitalize() + ' Graph Hubs')\
    .set_properties(**{'text-align':'center'})\
    .set_table_styles([{
     'selector': 'caption',
     'props': 'caption-side: top; font-size: 24px; text-align: center; color: black; font-weight: bold'
     },{
     'selector': 'th',
     'props': 'font-size: 14px; text-align: center'
     },{
     'selector': 'td',
     'props': 'font-size: 14px'
     }], overwrite = False)\
    .hide(axis = 'index')
    
    display(graph_info_stl)
    print('\n\n\n')
    display(hubs_info_stl)
    print('\n\n\n')
    
    # --- Degree distribution plots ---
    # Case 1: unweighted and directed graph, plot "in" and "out" degree distributions
    if nx.is_directed(G):
        fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (12,6))
        axes[0].hist(list(degs_out.values()), color = 'darkorange', edgecolor = 'black')
        axes[0].set_title('Citations Given Distribution')
        axes[0].set_xlabel('Number of Citations')
        axes[0].set_ylabel('Frequency')
        axes[0].set_axisbelow(True)
        axes[0].grid(zorder = 0)
        
        axes[1].hist(list(degs_in.values()), color = 'purple', edgecolor = 'black')
        axes[1].set_title('Citations Received Distribution')
        axes[1].set_xlabel('Number of Citations')
        axes[1].set_ylabel('Frequency')
        axes[1].set_axisbelow(True)
        axes[1].grid(zorder = 0)
    # Case 2: weighted and undirected graph, plot the top k authors by degree 
    else:
        fig, ax = plt.subplots(figsize = (12,6))
        ax.bar(hubs_info.Name[:k], hubs_info.Degree[:k], color = 'royalblue', edgecolor = 'black')
        ax.set_title('Number of collaborations\nTop '+str(k)+' authors')
        ax.set_xlabel('Author')
        ax.set_ylabel('Number of collaborations')
        ax.set_xticks(range(k), hubs_info.Name[:k], rotation = -45, ha='left', rotation_mode='anchor')
        ax.set_axisbelow(True)
        ax.grid(zorder = 0)
        
    return None

### NODE ID FINDER VISUALIZATION###
def visual_id_finder(G,input_str):
    '''
    Prints a node ID given the author's name of the paper's title
    
    input
    G: input graph
    input_str: input author's name or article's title
    
    output
    None
    '''
    # Use the ID finder
    ids = id_finder(G,input_str)
    
    # Handle cases in which there is no node with the typed name/title
    if ids == []:
        print('There is no such node')
        return None
    
    ids_df = pd.DataFrame(np.array([ids]), columns = ['ID'])
    
    # Change dataframes style to display prettier table
    ids_df_stl = ids_df.style\
    .set_caption('Node(s) ID(s)')\
    .set_properties(**{'text-align':'center'})\
    .set_table_styles([{
     'selector': 'caption',
     'props': 'caption-side: top; font-size: 24px; text-align: center; color: black; font-weight: bold'
     },{
     'selector': 'th',
     'props': 'font-size: 14px; text-align: center'
     },{
     'selector': 'td',
     'props': 'font-size: 14px'
     }], overwrite = False)\
    .hide(axis = 'index')
    
    display(ids_df_stl)
    
    return None

### FUNCTIONALITY 2 VISUALIZATION ###
def visual_2(G,v):
    '''
    Prints one table that displays four centrality measures calculated for an input node.
    The centrality measures are:
    - Betweenness centrality
    - PageRank centrality
    - Closeness centrality
    - Degree centrality
    
    input
    G: the input graph
    v: the input node (ID)
    
    output
    None
    ''' 
    # Handle both citation and collaboration graphs
    if nx.is_directed(G):
        G_name = 'citation'
        # Calculate centrality measures - Apply Functionality 2
        bet, pr, cc, dc = funct_2(G,str(v),G_name)
        # Create a dataframe to store the calculated measures
        colnames = ['Betweenness Centrality', 'PageRank Centrality', 'Closeness Centrality', 'Degree Centrality (In)', 'Degree Centrality (Out)']
        node_info = pd.DataFrame(np.array([[bet, pr, cc, dc[0], dc[1]]]), columns = colnames)
    else:
        G_name = 'collaboration'
        # Calculate centrality measures - Apply Functionality 2
        bet, pr, cc, dc = funct_2(G,str(v),G_name)
        # Create a dataframe to store the calculated measures
        colnames = ['Betweenness Centrality', 'PageRank Centrality', 'Closeness Centrality', 'Degree Centrality']
        node_info = pd.DataFrame(np.array([[bet, pr, cc, dc]]), columns = colnames)
    
    # Change dataframe style to display prettier table
    node_info_stl = node_info.style\
    .set_caption('Node ' + str(v) + ' Centrality Measures')\
    .set_properties(**{'text-align':'center'})\
    .set_table_styles([{
     'selector': 'caption',
     'props': 'caption-side: top; font-size: 24px; text-align: center; color: black; font-weight: bold'
     },{
     'selector': 'th',
     'props': 'font-size: 14px; text-align: center'
     },{
     'selector': 'td',
     'props': 'font-size: 14px'
     }], overwrite = False)\
    .format('{:.3f}')\
    .hide(axis = 'index')
    
    display(node_info_stl)
    
    return None

### FUNCTIONALITY 3 VISUALIZATION ###
def visual_3(G,a1,a,an,N):
    '''
    input
    G: the graph data
    a1: starting node
    a: string that is a sequence of authors  [a2,a3,...,an-1] separated by a blank space
    an: finish node
    N: numerosity of top authors by degree to consider
    
    output
    None
    ''' 
    # --- Shortest path table ---
    # Generate a list of nodes from the input string
    a = a.split(' ')
    
    # Calculate the shortest path - Apply Functionality 3
    path, papers = funct_3(G,a,str(a1),str(an),N)
    path_from = path[:-1]
    path_to = path[1:]
    path_papers = [list(x) for x in zip(path_from, path_to, papers)]
    
    # Create a DataFrame to store the path
    walk_df = pd.DataFrame(np.array(path_papers), columns = ['From (Author ID)', 'To (Author ID)', 'Paper Title'])
    
    # Change dataframe style to display prettier table
    walk_df_stl = walk_df.style\
    .set_caption('Shortest path from ' + str(a1) + ' to ' + str(an))\
    .set_properties(**{'text-align':'center'})\
    .set_table_styles([{
     'selector': 'caption',
     'props': 'caption-side: top; font-size: 24px; text-align: center; color: black; font-weight: bold'
     },{
     'selector': 'th',
     'props': 'font-size: 14px; text-align: center'
     },{
     'selector': 'td',
     'props': 'font-size: 14px'
     }], overwrite = False)\
    .hide(axis = 'index')
    
    display(walk_df_stl)
    
    # --- Visualization on graph ---
    #Compute the subgraph of G induced by the top N nodes by degree
    degrees = dict(G.degree())
    sorted_nodes = [k for k, v in sorted(degrees.items(), key=lambda x: x[1], reverse = True)]
    G_sub = G.subgraph(sorted_nodes[:N])
    # Compute a list of edges involved in the path
    path_edges = list(zip(path_from, path_to))
    # Compute a dictionary where edges in path are keys and papers are values
    labels = dict(list(zip(path_edges,[*range(1, len(path_edges)+1)])))
    
    # Initialize MatPlotLib figure
    plt.figure(figsize=(12, 8))
    # Use spring layout
    pos = nx.spring_layout(G_sub)
    
    # Draw nodes and edges not included in path
    nx.draw_networkx_nodes(G_sub, pos, nodelist=set(G_sub.nodes)-set(path), node_size = 50)
    nx.draw_networkx_edges(G_sub, pos, edgelist=set(G_sub.edges)-set(path_edges), edge_color='gray', node_size = 50)
    
    # Draw nodes and edges included in path
    nx.draw_networkx_nodes(G_sub, pos, nodelist=path, node_color='r', node_size = 50)
    nx.draw_networkx_edges(G_sub, pos, edgelist=path_edges, edge_color='r', node_size = 50)
    
    # Draw labels
    nx.draw_networkx_edge_labels(G_sub, pos, edge_labels = labels)
    
    # Zoom on the nodes of interest
    pos_path = {k:pos[str(k)] for k in path}
    xmin = min(xx for xx,yy in pos_path.values())
    xmax = max(xx for xx,yy in pos_path.values())
    xrange = xmax-xmin
    ymin = min(yy for xx,yy in pos_path.values())
    ymax = max(yy for xx,yy in pos_path.values())
    yrange = ymax-ymin
    axis = plt.gca()
    axis.set_xlim(left = xmin - 0.1*xrange, right = xmax + 0.1*xrange)
    axis.set_ylim(bottom = ymin - 0.1*yrange, top = ymax + 0.1*yrange)
    
    #nx.draw(G, pos, node_size=10, edge_color='gray', with_labels=False)
    plt.title("Zoomed graph with shortest walk highlighted")
    plt.tight_layout()
    plt.show()
    
    return None
    
### FUNCTIONALITY 4 VISUALIZATION ###
def visual_4(G,authorA,authorB,N):
    '''
    input
    G: the graph data
    authorA: the id of the first node which will be in the first sub-graph
    authorB: the id of the second node which will be in the second sub-graph
    N: numerosity of top authors by degree to consider
    
    output
    None
    '''
    # Split the original graph in two disconnected subgraphs, 
    # one containing node A and the other containing node B 
    # Apply Functionality 4 to do so
    min_weight, partition, edge_cut_list = funct_4(G,authorA,authorB,N)
    nedge_cut = len(edge_cut_list)
    
    # --- Print the number of links that should be disconnected ---
    print(f'A minimum of {nedge_cut} edges with an overall weight of {min_weight} need to be removed in order to split the graph in the two following (disconnected) sub-graphs')
    
    # --- Visualization on graph ---
    #Compute the subgraph induced by the top N nodes by degree
    degrees = dict(G.degree())
    sorted_nodes = [k for k, v in sorted(degrees.items(), key=lambda x: x[1], reverse = True)]
    G_sub = G.subgraph(sorted_nodes[:N])
    
    # Now, let's plot the induced sub-graph
    # Initialize MatPlotLib figure
    fig, axes = plt.subplots(nrows = 2, ncols = 1, figsize=(12, 10))
    # Use spring layout
    pos = nx.spring_layout(G_sub)
    
    # Plot the original graph
    nx.draw_networkx(G_sub, pos = pos, with_labels = False, edge_color = 'gray', node_size = 30, ax = axes[0])
    
    axes[0].set_title("Collaboration sub-graph")
    
    # Let's plot the two disconnected sub-graphs
    # Remove the cut edges from the original subgraph
    G_sub_cut = G_sub.copy()
    G_sub_cut.remove_edges_from(edge_cut_list)
    # Highlight the authorA and authorB nodes
    color_map = ['red' if node == authorA else '#00ff00' if node == authorB else '#1f78b4' for node in G_sub_cut] 
    size_map = [90 if node == authorA or node == authorB else 30 for node in G_sub_cut]
    # Draw the induced subgraph without the cut edges
    pos = nx.spring_layout(G_sub_cut)
    nx.draw_networkx(G_sub_cut, pos = pos, with_labels = False, edge_color = 'gray', node_color = color_map, node_size = size_map, ax = axes[1])
    
    # Check if authorA and authorB were originally in the same connected component
    connected_components = list(nx.connected_components(G_sub))
    in_same_component = any(authorA in component and authorB in component for component in connected_components)
    
    # Handle the visualization if they belonged to the same connected component or not
    if in_same_component:
        for i,comp in enumerate(connected_components):
            if authorA in comp:
                pos_path = {k:pos[k] for k in comp}
    else:
        pos_path = {}
        for i,comp in enumerate(connected_components):
            if (authorA in comp) or (authorB in comp):
                pos_path.update({k:pos[k] for k in comp})
    
    # Zoom on the nodes of interest
    xmin = min(xx for xx,yy in pos_path.values())
    xmax = max(xx for xx,yy in pos_path.values())
    xrange = xmax-xmin
    ymin = min(yy for xx,yy in pos_path.values())
    ymax = max(yy for xx,yy in pos_path.values())
    yrange = ymax-ymin
    axis = plt.gca()
    axis.set_xlim(left = xmin - 0.1*xrange, right = xmax + 0.1*xrange)
    axis.set_ylim(bottom = ymin - 0.1*yrange, top = ymax + 0.1*yrange)
    
    # Setup legend to identify paper_1 and paper_2 communities
    legend_elements = [
    Line2D([0], [0], marker='o', color='gray', label=f'{authorA} node',markerfacecolor='red', markersize=12),
    Line2D([0], [0], marker='o', color='gray', label=f'{authorB} node',markerfacecolor='#00ff00', markersize=12),        
    ]
    
    axes[1].legend(handles=legend_elements, loc='lower right')
    axes[1].set_title("Partition of sub-graph after mincut")
    plt.tight_layout()
    plt.show()
    
    return None


### FUNCTIONALITY 5 VISUALIZATION ###
def visual_5(G,paper_1,paper_2,N):
    '''
    input
    G: the graph data
    paper_1, paper_2:  strings of paper_ids
    N: numerosity of top authors by degree to consider
    
    output
    None
    '''
    # --- Communities in table ---
    # Find the communities - Apply functionality 5
    num_links, communities, are_in_same_comm = funct_5(G,paper_1,paper_2,N)
    
    # Stop if there are no communities (it means that one of the papers isn't in the induced subgraph)
    if communities == []:
        return None
    
    if num_links == 0:
        print('There is no need to remove links to have the following communities')
    else:
        print(f'A total of {num_links} links need to be removed to have the following communities')
    
    print('\n\n\n')
    
    # Store communities in a dataframe
    comm_df = pd.DataFrame(list(enumerate(communities)), columns = ['Community', 'Nodes'])
    
    # Change dataframe style to display prettier table
    comm_df_stl = comm_df.style\
    .set_caption('Citation Sub-Graph: List of Communities')\
    .set_properties(**{'text-align':'center'})\
    .set_table_styles([{
    "selector": "tr", 
    "props": "line-height: 30px;"
     },{
     'selector': 'caption',
     'props': 'caption-side: top; font-size: 24px; text-align: center; color: black; font-weight: bold'
     },{
     'selector': 'th',
     'props': 'font-size: 14px; text-align: center; line-height: inherit'
     },{
     'selector': 'td',
     'props': 'font-size: 14px; line-height: inherit'
     }], overwrite = False)\
    .hide(axis = 'index')
    
    show(comm_df_stl, classes="display compact")
    
    # --- Visualization on graph ---
    #Compute the subgraph induced by the top N nodes by degree
    degrees = dict(G.degree())
    sorted_nodes = [k for k, v in sorted(degrees.items(), key=lambda x: x[1], reverse = True)]
    G_sub = G.subgraph(sorted_nodes[:N])
    
    # Now, let's plot the induced sub-graph
    # Initialize MatPlotLib figure
    fig, axes = plt.subplots(nrows = 2, ncols = 1, figsize=(12, 10))
    # Use spring layout
    pos = nx.spring_layout(G_sub)
    
    # Plot the original graph
    nx.draw_networkx(G_sub, pos = pos, with_labels = False, edge_color = 'gray', node_size = 30, ax = axes[0])
    
    axes[0].set_title("Citation sub-graph")
    
    # Let's plot the same graph, with highlighted communities
    # Draw the induced subgraph
    nx.draw_networkx(G_sub, pos = pos, with_labels = False, edge_color = 'gray', node_size = 40, ax = axes[1])
    # Re-draw the nodes with different colors (random) by belonging community
    comm_cols = [tuple(np.random.choice(range(256), size=3)/256) for i in range(len(communities))]
    for i,com in enumerate(communities):
        if paper_1 in com:
            paper_1_comm = i
        if paper_2 in com:
            paper_2_comm = i
        nx.draw_networkx_nodes(G_sub, pos = pos, nodelist = G_sub.subgraph(com).nodes(), node_size = 40,node_color = comm_cols[i])
    
    # Setup legend to identify paper_1 and paper_2 communities
    legend_elements = [
    Line2D([0], [0], marker='o', color='gray', label=f'{paper_1} community',markerfacecolor=comm_cols[paper_1_comm], markersize=12),
    Line2D([0], [0], marker='o', color='gray', label=f'{paper_2} community',markerfacecolor=comm_cols[paper_2_comm], markersize=12),        
    ]
    
    axes[1].legend(handles=legend_elements, loc='lower right')
    axes[1].set_title("Citation sub-graph with communities")
    plt.tight_layout()
    plt.show()
    
    return None
    
    