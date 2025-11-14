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
origen = st.text_input("Dirección de origen (Ej: Bodega Central, Cartago)")

#############################################
# 3. Lugares que debe cubrir la ruta
#############################################
st.header("3. Lugares a visitar en la ruta")
st.write("Ingrese los lugares en orden aproximado o desordenado (el mapa mostrará todos). Ejemplo: Granadilla, Concepción, San Francisco…")

lugares_input = st.text_area(
    "Lista de lugares (uno por línea)",
    placeholder="Granadilla\nConcepción\nSan Francisco"
Concepción
San Francisco"
)

# Procesar lista
lugares = [l.strip() for l in lugares_input.split("
") if l.strip() != ""]

#############################################
# 4. Ordenar lugares de más lejano a más cercano
st.header("4. Ordenar automáticamente los lugares antes de enviar a Google Maps")

import requests

# Función geocodificar (Nominatim)
def geocode(lugar):
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": lugar, "format": "json"},
            headers={"User-Agent": "streamlit-app"}
        )
        data = resp.json()
        if len(data) > 0:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except:
        return None
    return None

# Función para distancia Haversine
import math
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

lugares_ordenados = []

if origen and len(lugares) > 0:
    origen_geo = geocode(origen)
    if origen_geo:
        origen_lat, origen_lon = origen_geo
        for l in lugares:
            geo = geocode(l)
            if geo:
                dist = haversine(origen_lat, origen_lon, geo[0], geo[1])
                lugares_ordenados.append((l, geo[0], geo[1], dist))

        # Ordenar de más lejano a más cercano
        lugares_ordenados.sort(key=lambda x: x[3], reverse=True)

        st.subheader("Lugares ordenados (de más lejos a más cerca)")
        for nombre, la, lo, d in lugares_ordenados:
            st.write(f"{nombre} — {d:.2f} km")

#############################################
# 5. Generar ruta en Google Maps
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
