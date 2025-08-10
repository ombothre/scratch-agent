def make_graph(nodes: list[str]) -> str:
    edges = []
    for i in range(len(nodes) - 1):
        edges.append(f"    {nodes[i]} -> {nodes[i+1]};")
    dot = "digraph {\n    rankdir=LR;\n" + "\n".join(edges) + "\n}"
    return dot
