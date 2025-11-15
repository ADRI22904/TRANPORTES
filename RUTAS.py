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
    "Lista de lugares (separados por una coma y un espacio)",
    placeholder="Granadilla, Concepción, San Francisco")


#############################################
# 4. Cálculo y visualización de peajes

#############################################
st.header("4. Costos estimados de peajes")

st.write("Indique cada peaje por separado si tienen diferentes montos.")

pasa_peajes = st.checkbox("¿La ruta incluye peajes?")

if pasa_peajes:
    cantidad = st.number_input(
        "Cantidad de peajes distintos", min_value=1, value=1, step=1
    )

    peajes = []
    total_peajes = 0

    for i in range(cantidad):
        st.subheader(f"Peaje #{i+1}")
        nombre = st.text_input(f"Nombre del peaje #{i+1}", key=f"peaje_nombre_{i}")
        costo = st.number_input(
            f"Costo del peaje #{i+1} (₡)", min_value=0, value=450, step=50, key=f"peaje_costo_{i}"
        )
        peajes.append((nombre, costo))
        total_peajes += costo

    st.subheader(f"Total a pagar en peajes: ₡{total_peajes:,.0f}")

    df_peajes = pd.DataFrame(peajes, columns=["Peaje", "Costo (₡)"])
    st.table(df_peajes)

else:
    st.info("No se han indicado peajes en esta ruta.")

# 5. Generar ruta en Google Maps
#############################################
st.header("5. Generar ruta en Google Maps")

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
# 6. Guardar ruta en Excel
#############################################
st.header("6. Guardar la ruta en Excel")


# Procesar lista de lugares de forma segura
lugares = [l.strip() for l in lugares_input.split(", ") if l.strip()] if lugares_input else []


# Configurar Google Sheets
import gspread
from google.oauth2.service_account import Credentials


SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]


try:
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open("Registro Rutas Transporte").sheet1
    conexion_ok = True
except Exception:
    st.error("⚠️ No se pudo conectar a Google Sheets. Asegúrese de subir el archivo service_account.json y que exista una hoja llamada 'Registro Rutas Transporte'.")
    conexion_ok = False


if origen and lugares and conexion_ok:
    if st.button("Guardar en Google Sheets"):
        # ---- Preparar filas para la hoja principal ----
        filas = []
        for destino in lugares:
            filas.append([
                nombre_ruta,
                str(fecha_ruta),
                str(hora_salida),
                origen,
                destino,
                "Sí" if pasa_peajes else "No",
                total_peajes if pasa_peajes else 0
        ])


    # Agregar filas a Google Sheets
    for fila in filas:
        sheet.append_row(fila)


# ---- Guardar peajes en segunda hoja ----
    try:
        hoja_peajes = client.open("Registro Rutas Transporte").worksheet("Peajes")
    except:
        hoja_peajes = client.open("Registro Rutas Transporte").add_worksheet(title="Peajes", rows="1000", cols="3")
        hoja_peajes.append_row(["Nombre ruta", "Peaje", "Costo (₡)"])


    if pasa_peajes:
        for nombre, costo in peajes:
            hoja_peajes.append_row([nombre_ruta, nombre, costo])


    st.success("Toda la información fue guardada en Google Sheets correctamente.")
# FIN DEL PROGRAMA


