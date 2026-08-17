import yfinance as yf
import pandas as pd
import numpy as np

def obtener_datos_mercado(ticker, periodo="1mo"):
    """
    Descarga los datos históricos de precios para un ticker específico usando yfinance.
    periodo: ej. '1mo' (1 mes), '3mo', '1y' (1 año).
    """
    try:
        print(f"Descargando datos para {ticker}...")
        activo = yf.Ticker(ticker)
        df = activo.history(period=periodo)
        
        if df.empty:
            print(f"No se encontraron datos para el ticker {ticker}.")
            return None
            
        return df
    except Exception as e:
        print(f"Error al conectar con Yahoo Finance: {e}")
        return None
    
def calcular_gestion_riesgo(capital, riesgo_porcentaje, distancia_sl):
    """
    Calcula cuántas acciones comprar y el riesgo monetario.
    distancia_sl: diferencia entre precio de entrada y precio de stop loss.
    """
    if distancia_sl <= 0:
        return 0, 0
    
    riesgo_decimal = riesgo_porcentaje / 100
    monto_a_arriesgar = capital * riesgo_decimal
    
    # Cantidad de acciones = Monto a arriesgar / Distancia al Stop Loss
    acciones_sugeridas = int(monto_a_arriesgar / distancia_sl)
    
    return acciones_sugeridas, monto_a_arriesgar

def calcular_indicadores(df):
    """
    Calcula indicadores simples usando Pandas y NumPy:
    - Retorno diario porcentual
    - Media móvil simple de 5 días
    - Volatilidad básica
    """
    if df is None or df.empty:
        return None

    # Creamos una copia para evitar advertencias de Pandas
    data = df.copy()
    
    # Cálculo del cambio porcentual diario
    data['Retorno_Diario'] = data['Close'].pct_change() * 100
    
    # Media Móvil Simple (SMA) de 5 periodos
    data['SMA_5'] = data['Close'].rolling(window=5).mean()
    
    # Volatilidad basada en la desviación estándar de los retornos
    volatilidad = np.std(data['Retorno_Diario'])
    
    # Obtenemos el precio actual de cierre (el último registro)
    precio_actual = data['Close'].iloc[-1]
    
    resultado = {
        "precio_actual": round(float(precio_actual), 2),
        "volatilidad": round(float(volatilidad), 2),
        "dataframe": data
    }
    
    return resultado

# Bloque de pruebas local
if __name__ == "__main__":
    # Probamos con una acción conocida como AAPL (Apple) o NVDA (Nvidia)
    ticker_prueba = "NVDA"
    datos = obtener_datos_mercado(ticker_prueba, periodo="1mo")
    analisis = calcular_indicadores(datos)
    
    if analisis:
        print(f"\n--- Resultados del análisis para {ticker_prueba} ---")
        print(f"Precio actual: ${analisis['precio_actual']}")
        print(f"Volatilidad diaria: {analisis['volatilidad']}%")