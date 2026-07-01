import datetime

import streamlit as st

from charts.dashboard_charts import (
    monthly_revenue_line,
    monthly_sales_bar,
    monthly_sales_line,
    revenue_by_category_bar,
    revenue_by_state_bar,
    revenue_map,
    sales_by_category_bar,
    sales_map,
    seller_revenue_bar,
    seller_sales_bar,
)
from services.analytics_service import (
    build_revenue_tables,
    build_sales_tables,
    build_seller_table,
    calculate_summary,
)
from services.data_service import filter_sales_data, load_sales_data
from utils.filters import normalize_date_range, sorted_options
from utils.formatters import format_compact_number, format_currency


def app():
    st.set_page_config(page_title="Sales Dashboard", layout="wide")
    st.title("Sales Dashboard")
    st.caption("Interactive analysis of sales by revenue, volume and sellers.")
    st.caption(f"Last update: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    try:
        sales_data = load_sales_data()
    except Exception as error:
        st.error(f"Error loading data: {error}")
        st.stop()

    selected_filters, seller_limit = render_sidebar(sales_data)
    filtered_data = filter_sales_data(sales_data, **selected_filters)

    st.sidebar.divider()
    st.sidebar.metric("Filtered Purchases", format_compact_number(filtered_data.shape[0]))

    if filtered_data.empty:
        st.warning("No sales found with the selected filters.")
        st.stop()

    summary = calculate_summary(filtered_data)
    revenue_tables = build_revenue_tables(filtered_data)
    sales_tables = build_sales_tables(filtered_data)
    sellers = build_seller_table(filtered_data)

    render_summary(summary)

    revenue_tab, sales_tab, sellers_tab = st.tabs(
        ["Revenue", "Sales Volume", "Sellers"]
    )

    with revenue_tab:
        render_revenue_tab(revenue_tables)

    with sales_tab:
        render_sales_tab(sales_tables)

    with sellers_tab:
        render_sellers_tab(sellers, seller_limit)


def render_sidebar(dataframe):
    st.sidebar.header("Filters")

    min_date = dataframe["Data da Compra"].min().date()
    max_date = dataframe["Data da Compra"].max().date()

    selected_date_range = st.sidebar.date_input(
        "Purchase Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY",
    )
    start_date, end_date = normalize_date_range(
        selected_date_range,
        min_date,
        max_date,
    )

    price_min = float(dataframe["Preço"].min())
    price_max = float(dataframe["Preço"].max())

    price_range = st.sidebar.slider(
        "Price Range",
        min_value=price_min,
        max_value=price_max,
        value=(price_min, price_max),
        step=10.0,
    )

    categories = sorted_options(dataframe, "Categoria do Produto")
    states = sorted_options(dataframe, "Local da compra")
    payment_types = sorted_options(dataframe, "Tipo de pagamento")
    sellers = sorted_options(dataframe, "Vendedor")

    selected_categories = st.sidebar.multiselect(
        "Categories",
        options=categories,
        default=categories,
    )
    selected_states = st.sidebar.multiselect(
        "States",
        options=states,
        default=states,
    )
    selected_payment_types = st.sidebar.multiselect(
        "Payment Types",
        options=payment_types,
        default=payment_types,
    )
    selected_sellers = st.sidebar.multiselect(
        "Sellers",
        options=sellers,
        default=sellers,
    )

    rating_min = int(dataframe["Avaliação da compra"].min())
    rating_max = int(dataframe["Avaliação da compra"].max())
    min_rating = st.sidebar.slider(
        "Minimum Rating",
        min_value=rating_min,
        max_value=rating_max,
        value=rating_min,
        step=1,
    )

    max_sellers = min(10, len(sellers))
    min_sellers = 1 if max_sellers == 1 else 2
    default_sellers = min(8, max_sellers)

    seller_limit = st.sidebar.slider(
        "Top Sellers",
        min_value=min_sellers,
        max_value=max_sellers,
        value=max(min_sellers, default_sellers),
        step=1,
    )

    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "categories": selected_categories,
        "states": selected_states,
        "payment_types": selected_payment_types,
        "sellers": selected_sellers,
        "min_rating": min_rating,
        "price_range": price_range,
    }

    return filters, seller_limit


def render_summary(summary):
    revenue_column, sales_column, ticket_column = st.columns(3)

    revenue_column.metric("Total Revenue", format_currency(summary["revenue"]))
    sales_column.metric(
        "Total Sales",
        format_compact_number(summary["sales_count"]),
    )
    ticket_column.metric("Average Ticket", format_currency(summary["average_ticket"]))


def render_revenue_tab(revenue_tables):
    left_column, right_column = st.columns(2)

    with left_column:
        st.plotly_chart(revenue_map(revenue_tables.by_state), use_container_width=True)
        st.plotly_chart(
            revenue_by_state_bar(revenue_tables.by_state),
            use_container_width=True,
        )

    with right_column:
        st.plotly_chart(
            monthly_revenue_line(revenue_tables.monthly),
            use_container_width=True,
        )
        st.plotly_chart(
            revenue_by_category_bar(revenue_tables.by_category),
            use_container_width=True,
        )


def render_sales_tab(sales_tables):
    left_column, right_column = st.columns(2)

    with left_column:
        st.plotly_chart(sales_map(sales_tables.by_state), use_container_width=True)
        st.plotly_chart(
            monthly_sales_bar(sales_tables.monthly_grouped),
            use_container_width=True,
        )

    with right_column:
        st.plotly_chart(
            monthly_sales_line(sales_tables.monthly),
            use_container_width=True,
        )
        st.plotly_chart(
            sales_by_category_bar(sales_tables.by_category),
            use_container_width=True,
        )


def render_sellers_tab(sellers, seller_limit):
    left_column, right_column = st.columns(2)

    with left_column:
        st.plotly_chart(
            seller_revenue_bar(sellers, seller_limit),
            use_container_width=True,
        )

    with right_column:
        st.plotly_chart(
            seller_sales_bar(sellers, seller_limit),
            use_container_width=True,
        )


if __name__ == "__main__":
    app()
