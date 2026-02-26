import streamlit as st
import pandas as pd

st.title("История расходов")

# Пример данных (в будущем — из CSV или базы)
if "expenses" not in st.session_state:
    st.session_state.expenses = [
        {"Дата": "2026-02-20", "Магазин": "Magnum", "Сумма": 4580, "Категория": "Продукты"},
        {"Дата": "2026-02-21", "Магазин": "Starbucks", "Сумма": 2300, "Категория": "Кафе"},
        {"Дата": "2026-02-24", "Магазин": "Яндекс Go", "Сумма": 1800, "Категория": "Транспорт"},
        {"Дата": "2026-02-25", "Магазин": "Small", "Сумма": 3200, "Категория": "Продукты"},
    ]

df = pd.DataFrame(st.session_state.expenses)

st.dataframe(df.style.format({"Сумма": "{:,.0f} ₸"}))

total = df["Сумма"].sum()
st.metric("Всего потрачено", f"{total:,.0f} ₸")

st.subheader("Расходы по категориям")
category_sum = df.groupby("Категория")["Сумма"].sum().reset_index()
st.bar_chart(category_sum.set_index("Категория")["Сумма"])