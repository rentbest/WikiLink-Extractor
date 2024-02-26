import argparse
import json
import logging


class Graph:
    def __init__(self, directed=True):
        self.graph = {}
        self.directed = directed

    def add_edge(self, source, target):
        if source not in self.graph:
            self.graph[source] = set()
        self.graph[source].add(target)

        if not self.directed:
            if target not in self.graph:
                self.graph[target] = set()
            self.graph[target].add(source)

    def get_neighbors(self, node):
        return list(self.graph.get(node, set()))


def convert_to_graph_structure(original_json):
    graph = Graph()
    convert_recursive(original_json, graph)
    return graph.graph


def convert_recursive(data, graph, parent=None):
    for key, value in data.items():
        graph.add_edge(parent, key)
        if isinstance(value, dict):
            convert_recursive(value, graph, key)


def find_shortest_path(graph, start, end):
    visited = set()
    queue = [[start]]

    if start == end:
        return [start]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in visited:
            neighbors = graph.get_neighbors(node)
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

                if neighbor == end:
                    return new_path

            visited.add(node)

    return []


def main():
    parser = argparse.ArgumentParser(
        description="Find the shortest path between two pages.")
    parser.add_argument("--from", dest="start_page",
                        required=True, help="Starting page")
    parser.add_argument("--to", dest="end_page",
                        required=True, help="Ending page")
    parser.add_argument("--non-directed", action="store_true",
                        help="Treat edges as non-directed")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    wiki_file_path = "wiki.json"

    try:
        with open(wiki_file_path, "r"):
            pass
    except:
        print("Database not found")
        return

    with open(wiki_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    directed = not args.non_directed
    graph = Graph(directed)

    converted_data = convert_to_graph_structure(data)

    for source, targets in converted_data.items():
        for target in targets:
            graph.add_edge(source, target)

    path = find_shortest_path(graph, args.start_page, args.end_page)

    if path:
        if args.verbose:
            logging.info(f"Shortest path found: {' -> '.join(path)}")
        print(len(path) - 1)
    else:
        print("Path not found")


if __name__ == "__main__":
    main()
