import streamlit as st
import pandas as pd
import urllib.parse

#############################################
# STREAMLIT – OPTIMIZADOR DE RUTAS POR NOMBRES (CON ORDEN DE LEJOS A CERCA)
#############################################
#############################################
st.title("Generador de Rutas con Visualización en Google Maps")
st.markdown("Ingrese los datos de la ruta y obtenga un enlace directo a Google Maps con el recorrido y tiempos estimados.")

#############################################
# 1. Datos Generales de la Ruta
#############################################
st.header("1. Información general")
nombre_ruta = st.text_input("Nombre de la ruta")
fecha_ruta = st.date_input("Fecha de la ruta")
hora_salida = st.time_input("Hora de salida")

#############################################
# 2. Origen del Camión
#############################################
st.header("2. Punto de salida del camión")
origen = st.text_input(
    "Dirección de origen (Ej: Bodega Central, Cartago)"
)

#############################################
# 3. Lugares que debe cubrir la ruta
#############################################
st.header("3. Lugares a visitar en la ruta")
st.write("Ingrese los lugares en orden aproximado o desordenado (el mapa mostrará todos). Ejemplo: Granadilla, Concepción, San Francisco…")

lugares_input = st.text_area(
    "Lista de lugares (uno por línea)",
    placeholder="Granadilla Concepción San Francisco")

#############################################
# 5. Guardar ruta en Excel
#############################################
st.header("5. Guardar la ruta en Excel")

if origen and lugares:
    df_export = pd.DataFrame({
        "Nombre de ruta": [nombre_ruta]*len(lugares),
        "Fecha": [fecha_ruta]*len(lugares),
        "Hora de salida": [hora_salida]*len(lugares),
        "Origen": [origen]*len(lugares),
        "Destino": lugares
    })

    nombre_archivo = f"ruta_{nombre_ruta}.xlsx" if nombre_ruta else "ruta_generada.xlsx"

    if st.button("Guardar en Excel"):
        df_export.to_excel(nombre_archivo, index=False)
        st.success(f"Archivo guardado: {nombre_archivo}")

#############################################
# 6. Cálculo y visualización de peajes
#############################################
st.header("6. Costos estimados de peajes")

st.write("Seleccione si la ruta pasa por peajes para mostrar el total estimado.")

pasa_peajes = st.checkbox("¿La ruta incluye peajes?")

costo_peaje_unitario = st.number_input(
    "Costo por peaje (₡)", min_value=0, value=450, step=50
)
cantidad_peajes = st.number_input(
    "Cantidad de peajes en la ruta", min_value=0, value=0, step=1
)

if pasa_peajes and cantidad_peajes > 0:
    total_peajes = costo_peaje_unitario * cantidad_peajes
    st.subheader(f"Total a pagar en peajes: ₡{total_peajes:,.0f}")
else:
    st.info("No se han indicado peajes en esta ruta.")

# FIN DEL PROGRAMA

