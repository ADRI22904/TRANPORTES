import streamlit as st
import pandas as pd
import math
import urllib.parse

#############################################
# FUNCIONES DE CÁLCULO
#############################################
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def ordenar_rutas(df, centro_lat, centro_lon, incluir_peaje, peso_carga):
    # Cálculo de distancia
    df["dist_km"] = df.apply(lambda row: haversine_km(
        centro_lat, centro_lon, row["lat"], row["lon"]), axis=1)

    # Prioridad primero
    df = df.sort_values(by=["prioridad", "dist_km"], ascending=[False, False])

    # Ajustes opcionales
    df["requiere_peaje"] = incluir_peaje
    df["peso_carga_ton"] = peso_carga

    return df

#############################################
# STREAMLIT UI
#############################################
st.title("Optimizador de Rutas — Más Lejana a Más Cercana con Prioridad")
st.markdown("Herramienta para organizar rutas de alisto tomando en cuenta prioridad, distancia y opciones adicionales.")

st.header("1. Configuración del Punto de Inicio (Centro)")
centro_lat = st.number_input("Latitud del centro", value=9.9333, format="%f")
centro_lon = st.number_input("Longitud del centro", value=-84.0833, format="%f")

st.header("2. Configuración extra")
incluir_peaje = st.checkbox("¿Necesita pasar por peaje?")
peso_carga = st.number_input("Peso de la carga (toneladas)", min_value=0.0, value=1.0, step=0.1)

st.header("3. Cargar rutas")
st.write("Suba un archivo CSV con las columnas: **nombre, lat, lon, prioridad** (prioridad = 1 si es urgente, 0 si no)")
archivo = st.file_uploader("Subir archivo CSV", type=["csv"]) 

if archivo:
    df = pd.read_csv(archivo)

    st.subheader("Vista previa de datos cargados")
    st.dataframe(df)

    st.header("4. Procesar y ordenar rutas")
    if st.button("Procesar rutas"):
        df_ordenado = ordenar_rutas(df.copy(), centro_lat, centro_lon, incluir_peaje, peso_carga)

        st.subheader("Rutas ordenadas")
        st.dataframe(df_ordenado)

        #############################################################
        # Google Maps — Crear URL con marcadores en orden
        #############################################################
        st.header("5. Ver rutas en Google Maps")

        # Crear una URL para Google Maps con los puntos ordenados
        base_url = "https://www.google.com/maps/dir/"

        # Añadir punto de inicio
        url = base_url + f"{centro_lat},{centro_lon}/"

        # Añadir destinos en el orden calculado
        for _, row in df_ordenado.iterrows():
            encoded = urllib.parse.quote(f"{row['lat']},{row['lon']}")
            url += f"{encoded}/"

        st.markdown(f"[**Abrir rutas en Google Maps**]({url})")

        st.success("Proceso completado. Las rutas han sido ordenadas y están listas para verificar en Google Maps.")
