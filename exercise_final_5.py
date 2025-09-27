import uuid
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from collections import deque
from typing import List, Dict, Optional


class Node:
    def __init__(self, key, color="#87fab9"):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0.0, y=0.0, layer=1):
    """(Рекурсивно) готує граф і позиції для малювання дерева."""
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


def draw_tree(tree_root: Node, colors: Dict[str, str], title: str = ""):
    """Малює дерево з урахуванням розфарбування вузлів."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    node_colors = [colors.get(node, "#87fac2") for node in tree.nodes()]
    labels = {node_id: data['label'] for node_id, data in tree.nodes(data=True)}

    plt.figure(figsize=(9, 5.5))
    if title:
        plt.title(title)
    nx.draw(
        tree, pos=pos, labels=labels, arrows=False,
        node_size=2500, node_color=node_colors, with_labels=True,
        font_color="black"
    )
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def build_heap_tree(heap: List[int]) -> Optional[Node]:
    """
    Побудова бінарного дерева з масиву-купи (array-репрезентація).
    Індекс i: лівий = 2*i+1, правий = 2*i+2.
    """
    if not heap:
        return None

    # Створюємо вузли
    nodes = [Node(val) for val in heap]

    # Зв'язуємо дітей
    n = len(nodes)
    for i in range(n):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < n:
            nodes[i].left = nodes[li]
        if ri < n:
            nodes[i].right = nodes[ri]

    return nodes[0]  # корінь


def _lerp(a: float, b: float, t: float) -> float:
    """Лінійна інтерполяція між a і b."""
    return a + (b - a) * t


def generate_color(step: int, total_steps: int) -> str:
    """
    Генерує колір від темного до світлого для кроку обходу.
    Використовує лінійну інтерполяцію між start_rgb та end_rgb.
    step: 1..total_steps
    """
    # Темний і світлий відтінки (можете підкоригувати палітру)
    start_rgb = (137, 135, 250)#(16, 44, 96)     # #102C60 — темно-синій
    end_rgb   = (250, 135, 214)#(179, 212, 255)  # #B3D4FF — світло-блакитний

    if total_steps <= 1:
        t = 1.0
    else:
        # нормалізуємо у [0..1]
        t = (step - 1) / (total_steps - 1)

    r = int(round(_lerp(start_rgb[0], end_rgb[0], t)))
    g = int(round(_lerp(start_rgb[1], end_rgb[1], t)))
    b = int(round(_lerp(start_rgb[2], end_rgb[2], t)))
    return f'#{r:02x}{g:02x}{b:02x}'


def dfs_visualize(root: Node, total_steps: int) -> Dict[str, str]:
    """
    Ітеративний DFS: використовує стек.
    Порядок: лівий потім правий (тому спочатку кладемо правого, потім лівого).
    """
    if root is None:
        return {}

    visited = set()
    stack: List[Node] = [root]
    colors: Dict[str, str] = {}
    step = 0

    while stack:
        node = stack.pop()
        if node.id in visited:
            continue
        visited.add(node.id)

        step += 1
        col = generate_color(step, total_steps)
        colors[node.id] = col
        node.color = col  # збережемо і у самому вузлі (для draw_tree)

        # Спочатку правий, потім лівий — щоб лівий обробився першим
        if node.right and node.right.id not in visited:
            stack.append(node.right)
        if node.left and node.left.id not in visited:
            stack.append(node.left)

    return colors


def bfs_visualize(root: Node, total_steps: int) -> Dict[str, str]:
    """
    Ітеративний BFS: використовує чергу (deque).
    """
    if root is None:
        return {}

    visited = set()
    queue: deque[Node] = deque([root])
    colors: Dict[str, str] = {}
    step = 0

    while queue:
        node = queue.popleft()
        if node.id in visited:
            continue
        visited.add(node.id)

        step += 1
        col = generate_color(step, total_steps)
        colors[node.id] = col
        node.color = col

        if node.left and node.left.id not in visited:
            queue.append(node.left)
        if node.right and node.right.id not in visited:
            queue.append(node.right)

    return colors


def count_nodes(node: Optional[Node]) -> int:
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


if __name__ == '__main__':
    # Початкова купа (list)
    heap_list = [1, 3, 5, 7, 9, 2, 4, 34, 2, 1, 2]
    heapq.heapify(heap_list)  # перетворюємо у валідну мін-купу

    # Побудова дерева з купи
    heap_tree_root = build_heap_tree(heap_list)

    # Кількість вузлів = кількість кроків обходу
    total_steps = count_nodes(heap_tree_root)

    # DFS
    dfs_colors = dfs_visualize(heap_tree_root, total_steps)
    draw_tree(heap_tree_root, dfs_colors, title="DFS (ітеративно, стек)")

    # Щоб показати інший обхід на «чистому» дереві, перебудуємо знову
    heap_tree_root = build_heap_tree(heap_list)
    total_steps = count_nodes(heap_tree_root)

    # BFS
    bfs_colors = bfs_visualize(heap_tree_root, total_steps)
    draw_tree(heap_tree_root, bfs_colors, title="BFS (ітеративно, черга)")