import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from models import Store, Category, Item
from knowledge_graph import create_expense_graph, find_related

# Настройки страницы
st.set_page_config(
    page_title="Граф знаний расходов",
    layout="wide",
    page_icon="🧾"
)

st.title("Граф знаний расходов 🧾🕸")
st.write("Исследуйте связи между магазинами, категориями и товарами")

# Загружаем граф
@st.cache_data
def get_graph():
    return create_expense_graph()

G = get_graph()

# Выбор узла
all_nodes = sorted(list(G.nodes()))
selected = st.selectbox(
    "Выберите узел (магазин / категория / товар):",
    all_nodes,
    index=0
)

# Кнопка для показа связей
if st.button("Показать связи", type="primary"):
    related = find_related(G, selected)
    
    if related:
        st.subheader(f"Связи для **{selected}**")
        for neigh, ntype in related:
            st.write(f"→ **{neigh}**  ({ntype})")
    else:
        st.info("Связей не найдено для этого узла")

# Визуализация графа
st.subheader("Визуализация графа")

fig, ax = plt.subplots(figsize=(12, 9))

# Цвета в зависимости от типа узла
node_colors = []
for node in G.nodes():
    ntype = G.nodes[node].get("type", "unknown")
    if ntype == "category":
        node_colors.append("#a8e6cf")   # светло-зелёный
    elif ntype == "store":
        node_colors.append("#b3d4fc")   # светло-синий
    elif ntype == "item":
        node_colors.append("#fff3b0")   # светло-жёлтый
    else:
        node_colors.append("#e0e0e0")   # серый

# Раскладка графа
pos = nx.spring_layout(G, seed=42, k=0.6)

# Рисуем
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=2400,
    font_size=9,
    font_weight="bold",
    edge_color="gray",
    linewidths=1.5,
    ax=ax
)

# Улучшаем отображение
plt.title("Граф связей расходов", fontsize=14, pad=20)
plt.tight_layout()

st.pyplot(fig)

# Дополнительная информация
st.markdown("---")
st.caption("Граф построен на основе примеров магазинов, категорий и товаров. "
           "Цвета: зелёный — категории, синий — магазины, жёлтый — товары.")