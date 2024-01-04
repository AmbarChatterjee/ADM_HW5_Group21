from .backend import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
from IPython.display import display

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
        hubs_df = pd.DataFrame(hubs, columns = ['ID', 'Degree'])
        hubs_info = degs_in_out_df.merge(hubs_df, how = 'inner', on = 'ID').sort_values('Degree', ascending = False)
        
    # Case 2: weighted and undirected graph - "in" and "out" degree are included in the analysis
    else:
        G_name = 'collaboration'
        # Apply functionality 1 to retrieve needed data
        n, e, dens, degs, avg_deg, perc_95, hubs, is_sparse = funct_1(G, G_name)
        # Store hubs info in pandas dataframe
        hubs_info = pd.DataFrame(hubs, columns = ['ID', 'Degree']).sort_values('Degree', ascending = False)
    
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
     'props': 'font-size: 14px'
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
    
    # WIP - output.csv is needed to add author and paper names as attributes to nodes (part 1)
    hubs_info_stl = hubs_info.style\
    .set_caption(G_name.capitalize() + ' Graph Hubs')\
    .set_properties(**{'text-align':'center'})\
    .set_table_styles([{
     'selector': 'caption',
     'props': 'caption-side: top; font-size: 24px; text-align: center; color: black; font-weight: bold'
     },{
     'selector': 'th',
     'props': 'font-size: 14px'
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
    # Case 2: weighted and undirected graph, plot the top k authors by degree WIP - replace ids with names
    else:
        fig, ax = plt.subplots(figsize = (12,6))
        ax.bar(hubs_info.ID[:k], hubs_info.Degree[:k], color = 'royalblue', edgecolor = 'black')
        ax.set_title('Number of collaborations\nTop '+str(k)+' authors')
        ax.set_xlabel('Author')
        ax.set_ylabel('Number of collaborations')
        ax.set_xticks(range(k), hubs_info.ID[:k], rotation = -45, ha='left', rotation_mode='anchor')
        ax.set_axisbelow(True)
        ax.grid(zorder = 0)
        
    return None
