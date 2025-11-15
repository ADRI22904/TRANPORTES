import streamlit as st
import pandas as pd
import urllib.parse

#############################################
# STREAMLIT – OPTIMIZADOR DE RUTAS POR NOMBRES
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
origen = st.text_input("Dirección de origen (Ej: Bodega Central, Cartago)")

#############################################
# 3. Lugares que debe cubrir la ruta
#############################################
st.header("3. Lugares a visitar en la ruta")
st.write("Ingrese los lugares en orden aproximado o desordenado (el mapa mostrará todos). Ejemplo: Granadilla, Concepción, San Francisco…")

lugares_input = st.text_area(
    "Lista de lugares (uno por línea)",
    placeholder = "
    Granadilla
    Concepción
    San Francisco")

# Procesar lista
lugares = [l.strip() for l in lugares_input.split("") if l.strip() != ""]

#############################################
# 4. Generar ruta en Google Maps
#############################################
st.header("4. Generar ruta en Google Maps")

if st.button("Mostrar ruta en mapa"):
    if origen == "" or len(lugares) == 0:
        st.error("Debe ingresar el origen y al menos un lugar de destino.")
    else:
        # Crear URL para Google Maps
        base_url = "https://www.google.com/maps/dir/"
        url = base_url

        # Agregar origen
        url += urllib.parse.quote(origen) + "/"

        # Agregar destinos
        for lugar in lugares:
            url += urllib.parse.quote(lugar) + "/"

        st.subheader("Mapa de Google Maps")
        st.markdown(f"[**Abrir ruta en Google Maps**]({url})")

        st.info("El mapa mostrará: tiempo estimado, distancias y orden sugerido según Google Maps.")

#############################################
# FIN DEL PROGRAMA
#############################################
