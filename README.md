# Sales Dashboard

Dashboard interativo de vendas desenvolvido com Streamlit, Pandas e Plotly. O app consome dados públicos de compras, aplica filtros dinâmicos e apresenta indicadores de receita, volume de vendas e desempenho de vendedores.


## Funcionalidades

- Carregamento de dados via API pública `https://labdados.com/produtos`.
- Filtros por período da compra, faixa de preço, categoria, estado, tipo de pagamento, vendedor e avaliação mínima.
- Indicadores de receita total, quantidade de vendas e ticket médio.
- Abas separadas para análise de receita, volume de vendas e vendedores.
- Mapas geográficos com concentração de receita e vendas por localidade.
- Gráficos mensais, rankings por estado, categorias de produto e ranking de vendedores.
- Cache de dados com Streamlit para reduzir chamadas repetidas à API.

## Tecnologias

- Python
- Streamlit
- Pandas
- Plotly
- Requests

## Estrutura do projeto

```text
.
|-- Dashboard.py
|-- requirements.txt
|-- charts/
|   |-- dashboard_charts.py
|-- services/
|   |-- analytics_service.py
|   |-- data_service.py
|-- utils/
|   |-- filters.py
|   |-- formatters.py
```

## Como executar

Pré-requisitos:

- Python 3.13.0, versão validada localmente
- Acesso à internet para consultar a API de dados

No PowerShell, a partir da raiz do projeto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run Dashboard.py
```

Depois de iniciar, o Streamlit abrirá o dashboard no navegador. Se ele não abrir automaticamente, use a URL exibida no terminal.

## Fonte de dados

O projeto usa o endpoint público `https://labdados.com/produtos`, que retorna registros de compras com campos como:

- produto
- categoria do produto
- preço
- frete
- data da compra
- vendedor
- local da compra
- avaliação da compra
- tipo de pagamento
- quantidade de parcelas
- latitude e longitude

O carregamento é feito em `services/data_service.py`, com conversão da coluna `Data da Compra` para data e cache de 30 minutos via `st.cache_data`.

## Validação local

Uma checagem rápida de sintaxe pode ser feita com:

```powershell
.\venv\Scripts\python.exe -m py_compile Dashboard.py services\data_service.py services\analytics_service.py charts\dashboard_charts.py utils\filters.py utils\formatters.py
```

## Observações

- O app depende da disponibilidade da API externa. Se o endpoint estiver fora do ar ou sem conexão, o dashboard exibirá erro de carregamento.
- O arquivo principal é `Dashboard.py`.
- As agregações ficam em `services/analytics_service.py`.
- Os gráficos ficam centralizados em `charts/dashboard_charts.py`.
