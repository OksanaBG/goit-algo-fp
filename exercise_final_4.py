import uuid
import math
import heapq
from typing import List, Optional, Any

import networkx as nx
import matplotlib.pyplot as plt


# БАЗОВІ СТРУКТУРИ ТА МАЛЮВАННЯ ДЕРЕВА 

class Node:
    def __init__(self, key, color="skyblue"):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color            # колір вузла
        self.id = str(uuid.uuid4())   # унікальний ідентифікатор вузла (не плутати зі значенням)


def add_edges(graph: nx.DiGraph, node: Optional[Node], pos: dict, x=0.0, y=0.0, layer=1) -> nx.DiGraph:
    """
    Рекурсивно додає вузли/ребра у граф і розкладає їх у площині (pos).
    """
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root: Node, title: str = "Бінарне дерево"):
    """
    Малює дерево, починаючи з кореня tree_root.
    """
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node_attrs['color'] for _, node_attrs in tree.nodes(data=True)]
    labels = {node_id: node_attrs['label'] for node_id, node_attrs in tree.nodes(data=True)}

    plt.figure(figsize=(9, 5))
    plt.title(title)
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors
    )
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# перетворення масиву купи на дерево вузлів 

def array_to_heap_tree(arr: List[Optional[Any]]) -> Optional[Node]:
    """
    Перетворює масив (0-індексація), що репрезентує повне бінарне дерево/купу,
    у зв’язану структуру вузлів Node. Значення None пропускаються.
    """
    if not arr:
        return None

    nodes: List[Optional[Node]] = [Node(v) if v is not None else None for v in arr]

    for i, node in enumerate(nodes):
        if node is None:
            continue
        li, ri = 2 * i + 1, 2 * i + 2
        if li < len(nodes) and nodes[li] is not None:
            node.left = nodes[li]
        if ri < len(nodes) and nodes[ri] is not None:
            node.right = nodes[ri]

    return nodes[0]  # корінь


def visualize_heap(heap_array: List[Optional[Any]],
                   heapify_first: bool = False,
                   as_max_heap: bool = False,
                   title_prefix: str = "Бінарна купа"):
    """
    Візуалізує бінарну купу з масиву.
      - heapify_first=True: спочатку викликаємо heapq.heapify (мін-купу).
      - as_max_heap=True:   якщо разом із heapify_first — імітуємо max-heap через інверсію знака.
    Примітка: heapq у Python підтримує лише мін-купу.
    """
    arr = list(heap_array)

    # Нормалізуємо: heapq не підтримує None усередині, тому при heapify приберемо None
    if heapify_first:
        if as_max_heap:
            # Макс-купа через інверсію: з упаковкою (-x, x) і без None
            compact = [(-x, x) for x in arr if x is not None]
            heapq.heapify(compact)
            # Повертаємо масив значень у порядку купи (щільний)
            arr = [pair[1] for pair in compact]
        else:
            compact = [x for x in arr if x is not None]
            heapq.heapify(compact)
            arr = list(compact)

    if not arr:
        print("Порожня купа — нічого візуалізувати.")
        return

    # Створюємо дерево
    root = array_to_heap_tree(arr)

    # Декоративне забарвлення рівнів дерева (градієнт прозорості)
    def level_of_index(i: int) -> int:
        return int(math.floor(math.log2(i + 1)))

    max_level = level_of_index(len(arr) - 1)
    palette = []
    for lvl in range(max_level + 1):
        alpha = 0.35 + 0.65 * (lvl / max(1, max_level))  # від 0.35 до 1.0
        palette.append((0.40, 0.60, 1.00, alpha))        # RGBA блакитний

    # Проставляємо кольори відповідно до рівня індексу
    index_to_node: List[Optional[Node]] = [None] * len(arr)
    q = [(root, 0)]
    while q:
        node, i = q.pop(0)
        if i < len(index_to_node):
            index_to_node[i] = node
        li, ri = 2 * i + 1, 2 * i + 2
        if node.left is not None:
            q.append((node.left, li))
        if node.right is not None:
            q.append((node.right, ri))

    for i, node in enumerate(index_to_node):
        if node is None:
            continue
        node.color = palette[level_of_index(i)]

    title = f"{title_prefix} (n={len(arr)})"
    draw_tree(root, title=title)


#  ДЕМО-ЗАПУСК 
if __name__ == "__main__":
    # 1) Уже-heap-масив (мін-купа у вигляді повного дерева)
    min_heap_arr = [1, 3, 2, 7, 8, 5]
    visualize_heap(min_heap_arr, heapify_first=False, title_prefix="Мін-heap (готовий масив)")

    # 2) Довільний масив -> робимо мін-heap через heapify -> малюємо
    random_arr = [8, 1, 7, 3, 9, 2, 6, 5, 4]
    visualize_heap(random_arr, heapify_first=True, as_max_heap=False, title_prefix="Мін-heap (heapify)")

    # 3) Імітація max-heap (інверсія знака під час heapify), потім малюємо
    visualize_heap(random_arr, heapify_first=True, as_max_heap=True, title_prefix="Макс-heap (імітація через -x)")