# Question 1
echo "Is there any node that acts as an important "'connector'" between the different parts of the graph?"
grep -o 'target="[0-9]*"' citation_graph.graphml | cut -d'"' -f2 | sort | uniq -c | sort -nr | head -n 1
# Question 2
echo "How does the degree of citation vary among the graph nodes?"
max=$(grep -o 'target="[0-9]*"' citation_graph.graphml | cut -d'"' -f2 | sort | uniq -c | sort -nr | awk '{print "Ranges from " $1}' | head -n 1)
min=$(grep -o 'target="[0-9]*"' citation_graph.graphml | cut -d'"' -f2 | sort | uniq -c | sort -nr | awk '{print "to " $1}' | tail -n 1)
echo "Ranges from $max to $min"
# Question 3
echo "What is the average length of the shortest path among nodes?"

# pip install networkx
python -c'
import networkx as nx

# Load the graph from a GraphML file
G = nx.read_graphml("citation_graph.graphml")
sum = 0
# Check if the graph is strongly connected
if nx.is_strongly_connected(G):
    average_distance = nx.average_shortest_path_length(G)
    print(f"Average shortest path length: {average_distance}")
else:
    print("Graph is not strongly connected.")

    # Calculate average shortest path length for each connected component
    components = list(nx.strongly_connected_components(G))
    for i, component in enumerate(components, start=1):
        subgraph = G.subgraph(component)
        component_average_distance = nx.average_shortest_path_length(subgraph)
        sum = sum + component_average_distance
    print(f"Average shortest path length: {sum/i}")
'