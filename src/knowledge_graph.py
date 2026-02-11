import networkx as nx

from models import Store, Category, Item


def create_expense_graph():
    G = nx.Graph()

    # ----------------------
    # 1. Добавляем узлы-категории
    # ----------------------
    categories = [
        Category("Продукты", typical_stores=["Magnum", "Small", "Ramstore"]),
        Category("Кафе и рестораны", typical_stores=["Starbucks", "KFC", "Burger King"]),
        Category("Транспорт", typical_stores=["Яндекс Go", "Водитель"]),
        Category("Алкоголь", typical_stores=["Магнум", "А также"]),
        Category("Развлечения", typical_stores=["Кинотеатр", "Game Center"]),
    ]

    for cat in categories:
        G.add_node(cat.name, type="category", obj=cat)

    # ----------------------
    # 2. Добавляем узлы-магазины
    # ----------------------
    stores = [
        Store("Magnum", common_categories=["Продукты", "Алкоголь"]),
        Store("Small", common_categories=["Продукты"]),
        Store("Starbucks", common_categories=["Кафе и рестораны"]),
        Store("Яндекс Go", common_categories=["Транспорт"]),
    ]

    for store in stores:
        G.add_node(store.name, type="store", obj=store)

    # ----------------------
    # 3. Добавляем несколько товаров (примеры)
    # ----------------------
    items = [
        Item("Молоко", "Продукты"),
        Item("Хлеб", "Продукты"),
        Item("Кофе латте", "Кафе и рестораны"),
        Item("Бензин", "Транспорт"),
        Item("Пиво", "Алкоголь"),
    ]

    for item in items:
        G.add_node(item.name, type="item", obj=item)

    # ----------------------
    # 4. Создаём связи
    # ----------------------
    edges = []

    # Магазин → относится к → Категория
    for store in stores:
        for cat_name in store.common_categories:
            edges.append((store.name, cat_name))

    # Товар → входит в → Категория
    for item in items:
        if item.default_category:
            edges.append((item.name, item.default_category))

    # Магазин → часто продаёт → Товар (пример)
    edges.extend([
        ("Magnum", "Молоко"),
        ("Magnum", "Хлеб"),
        ("Magnum", "Пиво"),
        ("Starbucks", "Кофе латте"),
        ("Яндекс Go", "Бензин"),
    ])

    G.add_edges_from(edges)

    return G


def find_related(graph, node_name):
    """Возвращает соседей узла + типы связей"""
    if node_name not in graph:
        return []

    neighbors = []
    for neighbor in graph.neighbors(node_name):
        edge_data = graph.get_edge_data(node_name, neighbor)
        neighbors.append((neighbor, graph.nodes[neighbor].get("type", "unknown")))
    return neighbors
