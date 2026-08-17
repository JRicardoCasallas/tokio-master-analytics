import os
from google import genai
from google.genai import errors

def generar_analisis_ia(ticker, precio, volatilidad):
    """
    Utiliza el cliente de Gemini para redactar un reporte táctico breve 
    sobre el activo financiero analizado.
    """
    # Verificamos si la API Key está configurada en las variables de entorno
    # (Si no la tienes configurada aún, puedes colocarla directamente como texto temporalmente para probar)
    api_key = "TU_API_KEY_AQUI"
    
    if not api_key:
        return "⚠️ Advertencia: No se encontró la variable de entorno GEMINI_API_KEY. Configúrala para usar la IA."

    try:
        # Inicializamos el cliente oficial de Google GenAI
        client = genai.Client(api_key=api_key)
        
        # Construimos el mensaje (prompt) para la IA
        prompt = (
            f"Actúa como un analista financiero experto. Analiza brevemente el siguiente activo:\n"
            f"- Ticker: {ticker}\n"
            f"- Precio actual: ${precio}\n"
            f"- Volatilidad diaria estimada: {volatilidad}%\n\n"
            f"Proporciona un comentario táctico de dos párrafos máximo indicando "
            f"qué lectura rápida se le puede dar a este comportamiento de mercado."
        )
        
        # Llamada al modelo moderno (gemini-2.5-flash es rápido y eficiente para esto)
        respuesta = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        
        return respuesta.text
        
    except errors.APIError as e:
        return f"Error de API de Gemini: {e}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

# Bloque de pruebas local
if __name__ == "__main__":
    print("Módulo de IA cargado correctamente. Listo para integrarse con main.py")