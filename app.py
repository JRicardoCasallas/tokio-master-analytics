import streamlit as st
import plotly.graph_objects as go
import engine
import ia_service
import database
import pandas as pd

# Configuración de la página en modo ancho y oscuro nativo
st.set_page_config(page_title="Tokio Master Analytics Pro", layout="wide")

st.title("📊 Tokio Master Analytics Pro")
st.markdown("---")

# Barra lateral con los controles de entrada
with st.sidebar:
    st.header("⚙️ Configuración de Análisis")
    ticker = st.text_input("Ticker", "NVDA").upper()
    periodo = st.selectbox("Periodo", ["1mo", "3mo", "1y"])
    capital = st.number_input("Capital ($)", value=10000.0)
    riesgo = st.number_input("Riesgo (%)", value=2.0)
    sl = st.number_input("Distancia SL (pts)", value=5.0)
    
    if st.button("Ejecutar Análisis Pro", type="primary"):
        with st.spinner('Consultando mercado y generando IA...'):
            datos = engine.obtener_datos_mercado(ticker, periodo=periodo)
            if datos is not None and not datos.empty:
                acciones, monto_riesgo = engine.calcular_gestion_riesgo(capital, riesgo, sl)
                ind = engine.calcular_indicadores(datos)
                ia = ia_service.generar_analisis_ia(ticker, ind["precio_actual"], ind["volatilidad"])
                
                # Guardar en base de datos
                database.guardar_registro(ticker, ind["precio_actual"], ind["volatilidad"], ia)
                
                # Guardar estado en la sesión de la web
                st.session_state.data = datos
                st.session_state.ia = ia
                st.session_state.acciones = acciones
                st.session_state.riesgo_monto = monto_riesgo
                st.success("¡Análisis completado!")
            else:
                st.error("No se encontraron datos o el Ticker es incorrecto.")

# Sección Principal si ya se ejecutó un análisis (Ajustamos proporciones para que el texto respire)
if 'data' in st.session_state:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("📋 Reporte Operativo")
        
        # Métricas organizadas en subcolumnas internas
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Acciones", value=st.session_state.acciones)
        with m2:
            st.metric(label="Riesgo ($)", value=f"${st.session_state.riesgo_monto:.2f}")
            
        st.markdown("### 🤖 Análisis de Inteligencia Artificial")
        st.info(st.session_state.ia)
        
    with col2:
        st.subheader("📈 Gráfico de Velas Interactivo")
        fig = go.Figure(data=[go.Candlestick(
            x=st.session_state.data.index,
            open=st.session_state.data['Open'], 
            high=st.session_state.data['High'],
            low=st.session_state.data['Low'], 
            close=st.session_state.data['Close']
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=480)
        st.plotly_chart(fig, use_container_width=True)

# Sección de Historial Interactiva abajo
st.markdown("---")
st.subheader("🗂️ Historial de Operaciones Guardadas")
historial_raw = database.obtener_historial()
if historial_raw:
    df_historial = pd.DataFrame(historial_raw, columns=["Ticker", "Precio ($)", "Volatilidad (%)", "Fecha / Hora"])
    st.dataframe(df_historial, use_container_width=True)
else:
    st.info("Aún no hay registros guardados en la base de datos.")