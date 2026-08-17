import sqlite3

def conectar():
    """Establece la conexión con la base de datos SQLite."""
    return sqlite3.connect("trading_data.db")

def crear_tabla():
    """Crea la tabla de registros si no existe."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            precio REAL NOT NULL,
            volatilidad REAL NOT NULL,
            analisis_ia TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("Base de datos y tabla verificadas/creadas correctamente.")

def guardar_registro(ticker, precio, volatilidad, analisis_ia):
    """Guarda un nuevo análisis completo en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registros (ticker, precio, volatilidad, analisis_ia)
        VALUES (?, ?, ?, ?)
    """, (ticker, precio, volatilidad, analisis_ia))
    conn.commit()
    conn.close()
def obtener_historial():
    """Recupera todos los registros guardados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT ticker, precio, volatilidad, fecha FROM registros ORDER BY fecha DESC")
    datos = cursor.fetchall()
    conn.close()
    return datos