import streamlit as st
import networkx as nx

from src.knowledge_graph import create_expense_graph
from src.logic import process_text_message

st.set_page_config(
    page_title="Чат-бот анализа расходов",
    page_icon="🧾💬",
    layout="wide"
)

st.title("Чат-бот анализа расходов")
st.markdown("Спрашивай про магазины, категории или товары — я поищу связи в графе.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph" not in st.session_state:
    with st.spinner("Загружаю граф знаний..."):
        st.session_state.graph = create_expense_graph()

if "expenses" not in st.session_state:
    st.session_state.expenses = []

graph = st.session_state.graph

# Приветствие при первом открытии
if len(st.session_state.messages) == 0:
    welcome = process_text_message("привет", graph)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напиши сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            response = process_text_message(prompt, graph, st.session_state.expenses)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("Очистить чат"):
    st.session_state.messages = []
    st.rerun()