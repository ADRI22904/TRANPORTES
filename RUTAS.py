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


if origen and lugares:
    df_export = pd.DataFrame({
        "Nombre de ruta": [nombre_ruta]*len(lugares),
        "Fecha": [fecha_ruta]*len(lugares),
        "Hora de salida": [hora_salida]*len(lugares),
        "Origen": [origen]*len(lugares),
        "Destino": lugares
    })

nombre_archivo = "registro_rutas.xlsx"

if st.button("Guardar en Excel"):
    try:
        # Si el archivo existe, cargarlo y agregar nueva información
        df_existente = pd.read_excel(nombre_archivo)
        df_final = pd.concat([df_existente, df_export], ignore_index=True)
    except FileNotFoundError:
        # Si no existe, crear uno nuevo
        df_final = df_export


df_final.to_excel(nombre_archivo, index=False)
st.success(f"La ruta fue agregada al archivo: {nombre_archivo}")
# FIN DEL PROGRAMA


