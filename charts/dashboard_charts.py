import plotly.express as px

from utils.formatters import MONTH_ORDER


COLOR_SCALE = "Teal"
MAP_TEMPLATE = "seaborn"


def revenue_map(revenue_by_state):
    return px.scatter_geo(
        revenue_by_state,
        lat="lat",
        lon="lon",
        size="Preço",
        scope="south america",
        template=MAP_TEMPLATE,
        hover_name="Local da compra",
        hover_data={"lat": False, "lon": False},
        projection="natural earth",
        title="Revenue by state",
    )


def revenue_by_state_bar(revenue_by_state, limit=10):
    figure = px.bar(
        revenue_by_state.head(limit),
        x="Local da compra",
        y="Preço",
        title=f"Top {limit} states by revenue",
        color="Preço",
        color_continuous_scale=COLOR_SCALE,
        labels={"Preço": "Revenue (R$)", "Local da compra": "State"},
    )
    figure.update_layout(xaxis_title="State", yaxis_title="Revenue (R$)")
    return figure


def revenue_by_category_bar(revenue_by_category):
    figure = px.bar(
        revenue_by_category,
        x="Categoria do Produto",
        y="Preço",
        title="Revenue by category",
        color="Preço",
        color_continuous_scale=COLOR_SCALE,
        labels={"Preço": "Revenue (R$)", "Local da compra": "State"},
    )
    figure.update_layout(xaxis_title="Category", yaxis_title="Revenue (R$)")
    return figure


def monthly_revenue_line(monthly_revenue):
    figure = px.line(
        monthly_revenue,
        x="Mês",
        y="Preço",
        markers=True,
        color="Ano",
        line_dash="Ano",
        category_orders={"Mês": MONTH_ORDER},
        title="Monthly Revenue",
        labels={"Preço": "Revenue (R$)", "Local da compra": "State"},
    )
    figure.update_layout(yaxis_title="Revenue (R$)")
    return figure


def sales_map(sales_by_state):
    return px.scatter_geo(
        sales_by_state,
        lat="lat",
        lon="lon",
        size="Vendas",
        scope="south america",
        template=MAP_TEMPLATE,
        hover_name="Local da compra",
        hover_data={"lat": False, "lon": False},
        projection="natural earth",
        title="Sales by state",
    )


def monthly_sales_line(monthly_sales):
    figure = px.line(
        monthly_sales,
        x="Mês",
        y="Vendas",
        markers=True,
        color="Ano",
        line_dash="Ano",
        category_orders={"Mês": MONTH_ORDER},
        title="Monthly Sales",
    )
    figure.update_layout(yaxis_title="Sales Quantity")
    return figure


def monthly_sales_bar(monthly_sales_grouped):
    figure = px.bar(
        monthly_sales_grouped,
        x="Mês",
        y="Vendas",
        title="Monthly Sales",
        color="Vendas",
        color_continuous_scale=COLOR_SCALE,
        category_orders={"Mês": MONTH_ORDER},
    )
    figure.update_layout(xaxis_title="Month", yaxis_title="Sales Quantity")
    return figure


def sales_by_category_bar(sales_by_category):
    figure = px.bar(
        sales_by_category,
        x="Categoria do Produto",
        y="Vendas",
        title="Sales by category",
        color="Vendas",
        color_continuous_scale=COLOR_SCALE,
    )
    figure.update_layout(xaxis_title="Category", yaxis_title="Sales Quantity")
    return figure


def seller_revenue_bar(sellers, limit):
    data = sellers.sort_values("Receita", ascending=False).head(limit)
    figure = px.bar(
        data,
        x=data.index,
        y="Receita",
        title=f"Top {limit} sellers by revenue",
        color="Receita",
        color_continuous_scale=COLOR_SCALE,
    )
    figure.update_layout(xaxis_title="Seller", yaxis_title="Revenue (R$)")
    return figure


def seller_sales_bar(sellers, limit):
    data = sellers.sort_values("Vendas", ascending=False).head(limit)
    figure = px.bar(
        data,
        x=data.index,
        y="Vendas",
        title=f"Top {limit} sellers by sales volume",
        color="Vendas",
        color_continuous_scale=COLOR_SCALE,
    )
    figure.update_layout(xaxis_title="Seller", yaxis_title="Sales Quantity")
    return figure
