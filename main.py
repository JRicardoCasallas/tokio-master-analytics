import streamlit as st
import plotly.graph_objects as go
import engine
import ia_service
import database
import datetime

# Configuración inicial
st.set_page_config(page_title="Tokio Master Analytics Pro", layout="wide")

st.title("📊 Tokio Master Analytics Pro")
st.markdown("---")

# Barra lateral para configuración
with st.sidebar:
    st.header("Configuración de Análisis")
    ticker = st.text_input("Ticker", "NVDA").upper()
    periodo = st.selectbox("Periodo", ["1mo", "3mo", "1y"])
    capital = st.number_input("Capital ($)", value=10000)
    riesgo = st.number_input("Riesgo (%)", value=2)
    sl = st.number_input("Distancia SL (pts)", value=5)
    
    if st.button("Ejecutar Análisis"):
        datos = engine.obtener_datos_mercado(ticker, periodo=periodo)
        if datos is not None:
            # Cálculos
            acciones, monto_riesgo = engine.calcular_gestion_riesgo(capital, riesgo, sl)
            ind = engine.calcular_indicadores(datos)
            ia = ia_service.generar_analisis_ia(ticker, ind["precio_actual"], ind["volatilidad"])
            
            # Guardar
            database.guardar_registro(ticker, ind["precio_actual"], ind["volatilidad"], ia)
            
            # Guardar en sesión para mostrar
            st.session_state.data = datos
            st.session_state.ia = ia
            st.session_state.acciones = acciones
            st.session_state.riesgo_monto = monto_riesgo

# Área principal
if 'data' in st.session_state:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Reporte Operativo")
        st.write(f"**Acciones Sugeridas:** {st.session_state.acciones}")
        st.write(f"**Riesgo Monetario:** ${st.session_state.riesgo_monto:.2f}")
        st.info(st.session_state.ia)
        
    with col2:
        st.subheader("Gráfico Interactivo")
        fig = go.Figure(data=[go.Candlestick(x=st.session_state.data.index,
                        open=st.session_state.data['Open'], high=st.session_state.data['High'],
                        low=st.session_state.data['Low'], close=st.session_state.data['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

# Historial abajo
st.subheader("Historial de Consultas")
st.table(database.obtener_historial_df()) # Nota: Asegúrate que esto devuelva un DataFrame