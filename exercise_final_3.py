import heapq
import networkx as nx
import matplotlib.pyplot as plt


# 1) Створення ВЛАСНОГО зваженого графа 
# Граф підібрано так, щоб було кілька альтернативних шляхів різної ваги
G = nx.Graph()
weighted_edges = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 5),
    ("B", "D", 10),
    ("C", "E", 3),
    ("E", "D", 4),
    ("D", "F", 11),
    ("E", "F", 2),
]
G.add_weighted_edges_from(weighted_edges)


# 2) Реалізація алгоритму Дейкстри з бінарною купою 
def dijkstra(graph: nx.Graph, start):
    # Ініціалізація відстаней: нескінченність, окрім старту
    dist = {v: float("inf") for v in graph.nodes}
    dist[start] = 0.0

    # Для відновлення шляхів зберігаємо попередника
    prev = {v: None for v in graph.nodes}

    # Бінарна купа: пари (поточна_відстань, вершина)
    pq = [(0.0, start)]

    # Поки купа не порожня — дістаємо вершину з найменшою відстанню
    while pq:
        cur_d, u = heapq.heappop(pq)

        # Якщо це "застарілий" запис (у купі може лежати гірша відстань) — ігноруємо
        if cur_d > dist[u]:
            continue

        # Релаксація всіх ребер з u
        for v, attrs in graph[u].items():
            w = attrs.get("weight", 1.0)
            nd = cur_d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev


def reconstruct_path(prev, start, target):
    """Відновлює список вершин найкоротшого шляху start→target, або [] якщо шляху нема."""
    if prev.get(target) is None and start != target:
        return []  # недосяжно
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


# 3) Запуск алгоритму 
start = "A"
distances, parents = dijkstra(G, start)
print("Найкороткі відстані від вершини", start)
for v in sorted(G.nodes):
    print(f"  {start} -> {v}: {distances[v]}")

# Приклад відновлення конкретного шляху
target = "F"
path = reconstruct_path(parents, start, target)
if path:
    print(f"Найкоротший шлях {start} -> {target}: {' → '.join(path)} (довжина {distances[target]})")
else:
    print(f"Вершина {target} недосяжна зі старту {start}")


# 4) Візуалізація графа 
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_size=700, node_color="#DCEBFF", edgecolors="#1F4B99", linewidths=1.5)
nx.draw_networkx_edges(G, pos, width=2, edge_color="#7AA6FF")
nx.draw_networkx_labels(G, pos, font_size=14)

edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

plt.title("Зважений граф для Дейкстри (heapq)")
plt.axis("off")
plt.show()