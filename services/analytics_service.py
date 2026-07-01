from dataclasses import dataclass

import pandas as pd

from utils.formatters import month_name


@dataclass(frozen=True)
class RevenueTables:
    by_state: pd.DataFrame
    monthly: pd.DataFrame
    by_category: pd.DataFrame


@dataclass(frozen=True)
class SalesTables:
    by_state: pd.DataFrame
    monthly: pd.DataFrame
    monthly_grouped: pd.DataFrame
    by_category: pd.DataFrame


def calculate_summary(dataframe: pd.DataFrame) -> dict[str, float]:
    return {
        "revenue": float(dataframe["Preço"].sum()),
        "sales_count": int(dataframe.shape[0]),
        "average_ticket": float(dataframe["Preço"].mean()) if not dataframe.empty else 0,
    }


def build_revenue_tables(dataframe: pd.DataFrame) -> RevenueTables:
    by_state = _state_table(dataframe, value_column="Preço", metric_name="Preço", agg="sum")

    monthly = _monthly_table(dataframe, value_column="Preço", metric_name="Preço", agg="sum")

    by_category = (
        dataframe.groupby("Categoria do Produto", as_index=False)["Preço"]
        .sum()
        .sort_values("Preço", ascending=False)
    )

    return RevenueTables(
        by_state=by_state,
        monthly=monthly,
        by_category=by_category,
    )


def build_sales_tables(dataframe: pd.DataFrame) -> SalesTables:
    by_state = _state_table(dataframe, value_column="Preço", metric_name="Vendas", agg="count")

    monthly = _monthly_table(dataframe, value_column="Preço", metric_name="Vendas", agg="count")

    monthly_grouped = (
        monthly.groupby(["Mês", "Mês Número"], as_index=False)[["Vendas"]]
        .sum()
        .sort_values("Mês Número")
    )

    by_category = (
        dataframe.groupby("Categoria do Produto", as_index=False)["Preço"]
        .count()
        .rename(columns={"Preço": "Vendas"})
        .sort_values("Vendas", ascending=False)
    )

    return SalesTables(
        by_state=by_state,
        monthly=monthly,
        monthly_grouped=monthly_grouped,
        by_category=by_category,
    )


def build_seller_table(dataframe: pd.DataFrame) -> pd.DataFrame:
    return (
        dataframe.groupby("Vendedor")
        .agg(Receita=("Preço", "sum"), Vendas=("Preço", "count"))
        .sort_values("Receita", ascending=False)
    )


def _state_table(
    dataframe: pd.DataFrame,
    value_column: str,
    metric_name: str,
    agg: str,
) -> pd.DataFrame:
    grouped = dataframe.groupby("Local da compra")[[value_column]].agg(agg)

    return (
        dataframe.drop_duplicates(subset=["Local da compra"])[
            ["Local da compra", "lat", "lon"]
        ]
        .merge(grouped, left_on="Local da compra", right_index=True)
        .rename(columns={value_column: metric_name})
        .sort_values(metric_name, ascending=False)
    )


def _monthly_table(
    dataframe: pd.DataFrame,
    value_column: str,
    metric_name: str,
    agg: str,
) -> pd.DataFrame:
    monthly = (
        dataframe.set_index("Data da Compra")
        .groupby(pd.Grouper(freq="ME"))[[value_column]]
        .agg(agg)
        .reset_index()
        .rename(columns={value_column: metric_name})
    )

    monthly["Mês Número"] = monthly["Data da Compra"].dt.month
    monthly["Mês"] = monthly["Mês Número"].apply(month_name)
    monthly["Ano"] = monthly["Data da Compra"].dt.year.astype(str)

    return monthly
