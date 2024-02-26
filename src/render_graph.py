import os
import networkx as nx
from itertools import combinations
from random import randint
import matplotlib.pyplot as plt
import json


def create_filtered_networkx_graph(input_dict, filter_probability=0.3):
    G = nx.Graph()

    # Use the provided dictionary
    large_dict = input_dict

    # Add edges between random nodes based on the filter probability
    for edge in combinations(large_dict.keys(), 2):
        if randint(0, 10) < filter_probability * 10:
            G.add_edge(*edge)

    return G


def visualize_filtered_graph(graph, save_png_path, save_html_path):
    # Calculate node sizes based on the number of incoming connections
    node_sizes = dict(graph.degree())
    max_node_size = max(node_sizes.values())

    # Scale node sizes for better visualization
    scaled_node_sizes = [
        10 + 90 * (node_sizes[node] / max_node_size) for node in graph.nodes()]

    # Spring layout for visualization
    pos = nx.spring_layout(graph)

    plt.figure(figsize=(15, 12))

    # Draw nodes with size corresponding to the number of incoming connections
    nx.draw(graph, pos, with_labels=False, node_size=scaled_node_sizes,
            node_color='skyblue', font_size=8, edge_color='gray', linewidths=0.5)

    plt.title("Filtered Graph Visualization")

    # Save as PNG
    plt.savefig(save_png_path, format="png", bbox_inches="tight")
    plt.close()

    # Save as HTML using Plotly
    try:
        import plotly.graph_objects as go

        edge_x = []
        edge_y = []
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for x, y in pos.values():
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=scaled_node_sizes,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=0),
                            xaxis=dict(showgrid=False, zeroline=False,
                                       showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.write_html(save_html_path)

    except ImportError:
        print("Plotly is not installed. Please install it using 'pip install plotly' to save as HTML.")


def main():
    # Load data from the WIKI_FILE environment variable
    wiki_file_path = os.environ.get('WIKI_FILE', 'wiki.json')
    with open(wiki_file_path, "r") as json_file:
        your_dict = json.load(json_file)

    # Create and visualize the graph
    filtered_graph = create_filtered_networkx_graph(your_dict)
    save_filtered_png_path = "wiki_graph.png"
    save_filtered_html_path = "wiki_graph.html"
    visualize_filtered_graph(
        filtered_graph, save_filtered_png_path, save_filtered_html_path)


if __name__ == "__main__":
    main()
