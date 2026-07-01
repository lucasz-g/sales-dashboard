from datetime import date

import pandas as pd
import requests
import streamlit as st


API_URL = "https://labdados.com/produtos"


@st.cache_data(ttl=60 * 30, show_spinner=False)
def load_sales_data(url: str = API_URL) -> pd.DataFrame:
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    dataframe = pd.DataFrame.from_records(response.json())
    dataframe["Data da Compra"] = pd.to_datetime(
        dataframe["Data da Compra"],
        format="%d/%m/%Y",
    )

    return dataframe


def filter_sales_data(
    dataframe: pd.DataFrame,
    start_date: date,
    end_date: date,
    categories: list[str],
    states: list[str],
    payment_types: list[str],
    sellers: list[str],
    min_rating: int,
    price_range: tuple[float, float],
) -> pd.DataFrame:
    filtered = dataframe.copy()

    filtered = filtered[
        filtered["Data da Compra"].dt.date.between(start_date, end_date)
    ]

    if categories:
        filtered = filtered[filtered["Categoria do Produto"].isin(categories)]

    if states:
        filtered = filtered[filtered["Local da compra"].isin(states)]

    if payment_types:
        filtered = filtered[filtered["Tipo de pagamento"].isin(payment_types)]

    if sellers:
        filtered = filtered[filtered["Vendedor"].isin(sellers)]

    min_price, max_price = price_range
    filtered = filtered[filtered["Preço"].between(min_price, max_price)]
    filtered = filtered[filtered["Avaliação da compra"] >= min_rating]

    return filtered
