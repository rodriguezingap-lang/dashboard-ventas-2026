import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Corporativo", page_icon="📊", layout="wide")

# 2. Inyectar CSS Minimalista y Ejecutivo (Estilo Claro)
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    [data-testid="stMetricValue"] {
        color: #0F52BA !important; 
        font-weight: 700;
        font-size: 30px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-size: 15px !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard Ejecutivo de Ventas")
st.markdown("---")

# 3. Cargar la base de datos
@st.cache_data
def cargar_datos():
    return pd.read_excel("ventas_consolidadas_procesadas.xlsx")

df = cargar_datos()

# 4. BARRA LATERAL: Segmentadores (MENÚS DESPLEGABLES)
st.sidebar.header("🎯 Filtros Dinámicos")

# A. Crear las listas de opciones, agregando "Todos" al inicio
canales = ["Todos"] + list(df["canal"].unique())
vendedores = ["Todos"] + list(df["vendedor"].unique())
categorias = ["Todos"] + list(df["categoria"].unique())

# B. Crear los menús desplegables clásicos (selectbox)
canal_seleccionado = st.sidebar.selectbox("Canal de Venta:", canales)
vendedor_seleccionado = st.sidebar.selectbox("Vendedor:", vendedores)
categoria_seleccionada = st.sidebar.selectbox("Categoría:", categorias)

# C. Aplicar los filtros a la base de datos
df_filtrado = df.copy()

if canal_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["canal"] == canal_seleccionado]
    
if vendedor_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["vendedor"] == vendedor_seleccionado]
    
if categoria_seleccionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria_seleccionada]


# 5. CÁLCULOS DE KPIs
total_ingresos = df_filtrado["ingreso_total"].sum()
total_unidades = df_filtrado["cantidad"].sum()
ticket_promedio = total_ingresos / total_unidades if total_unidades > 0 else 0
total_transacciones = len(df_filtrado)

if not df_filtrado.empty:
    mejor_vendedor = df_filtrado.groupby("vendedor")["ingreso_total"].sum().idxmax()
    producto_estrella = df_filtrado.groupby("nombre_producto")["cantidad"].sum().idxmax()
else:
    mejor_vendedor = "N/A"
    producto_estrella = "N/A"

# 6. RENDERIZAR TARJETAS KPI
st.subheader("📋 Resumen General")

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Totales", f"S/ {total_ingresos:,.2f}")
col2.metric("Unidades Vendidas", f"{total_unidades:,.0f}")
col3.metric("Ticket Promedio", f"S/ {ticket_promedio:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
col4.metric("Total Transacciones", f"{total_transacciones}")
col5.metric("Mejor Vendedor", f"{mejor_vendedor}")
col6.metric("Producto Estrella", f"{producto_estrella}")

st.markdown("---")

# 7. GRÁFICOS CORPORATIVOS
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Ingresos por Vendedor")
    df_vendedor = df_filtrado.groupby("vendedor")["ingreso_total"].sum().reset_index()
    df_vendedor = df_vendedor.sort_values(by="ingreso_total", ascending=True)
    
    fig_barras = px.bar(
        df_vendedor, x="ingreso_total", y="vendedor", 
        orientation='h', text_auto='.2s',
        color_discrete_sequence=['#0F52BA'], 
        template="plotly_white"
    )
    fig_barras.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_barras, use_container_width=True)

with col_graf2:
    st.subheader("Participación por Categoría")
    fig_dona = px.pie(
        df_filtrado, names="categoria", values="ingreso_total", hole=0.5,
        color_discrete_sequence=['#0F52BA', '#4FA4F2', '#94A3B8', '#F59E0B'], 
        template="plotly_white"
    )
    fig_dona.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_dona, use_container_width=True)

# 8. GRÁFICO DE TENDENCIA
st.subheader("Evolución de Ingresos")
df_fechas = df_filtrado.groupby("fecha_venta")["ingreso_total"].sum().reset_index()

fig_lineas = px.line(
    df_fechas, x="fecha_venta", y="ingreso_total", markers=True,
    color_discrete_sequence=['#F59E0B'], 
    template="plotly_white"
)
fig_lineas.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_lineas, use_container_width=True)