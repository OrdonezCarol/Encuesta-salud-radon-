import streamlit as st
import pandas as pd
import os

# --- Configuración inicial ---
st.set_page_config(page_title="Encuesta Radón y Salud", layout="centered")

# Archivo de almacenamiento
DATA_FILE = "data/respuestas.csv"
os.makedirs("data", exist_ok=True)

# --- Función para guardar respuestas ---
def guardar_respuesta(respuestas_dict):
    df_nueva = pd.DataFrame([respuestas_dict])
    if os.path.exists(DATA_FILE):
        df_existente = pd.read_csv(DATA_FILE)
        df_final = pd.concat([df_existente, df_nueva], ignore_index=True)
    else:
        df_final = df_nueva
    df_final.to_csv(DATA_FILE, index=False)

# --- Pantalla 1: Consentimiento ---
st.title("Encuesta: Salud respiratoria y exposición a radón")
st.header("Consentimiento informado")

consentimiento = st.radio(
   " En el año 2023 usted participó en un estudio en el que se realizaron mediciones de radón en su vivienda. Por tal motivo, le invitamos a participar en la presente investigación. Su participación es completamente voluntaria, anónima y confidencial, y puede retirarse en cualquier momento sin ninguna consecuencia. La encuesta tiene una duración aproximada de 10 minutos. ¿Acepta participar?",
    ["Sí, acepto", "No, no acepto"]
)

if consentimiento == "No, no acepto":
    st.warning("Gracias, la encuesta ha finalizado.")
    st.stop()

# Diccionario donde se guardarán las respuestas
respuestas = {"consentimiento": consentimiento}

# --- Sección A ---
st.header("Sección A: Vínculo con medición de radón")
vivienda_actual = st.radio("¿Actualmente vive en la misma vivienda desde el 2023?", ["Sí", "No"])
respuestas["vive_misma_vivienda"] = vivienda_actual
if vivienda_actual == "No":
    respuestas["tiempo_vivio_2023_meses"] = st.number_input("¿Durante cuánto tiempo vivió en esa vivienda en 2023? (meses)", min_value=0, step=1)

# --- Sección B ---
st.header("Sección B: Datos sociodemográficos")
respuestas["edad"] = st.number_input("Edad (años)", min_value=0, step=1)
respuestas["sexo"] = st.radio("Sexo", ["Femenino", "Masculino"])
respuestas["nivel_educativo"] = st.selectbox("Nivel educativo", ["Universitario en curso", "Titulado universitario", "Posgrado", "Otro"])

# --- Sección C ---
st.header("Sección C: Exposiciones respiratorias relevantes")
respuestas["fumaba_2023"] = st.radio("¿Fumaba en el 2023?", ["Nunca fumé", "Exfumador", "Fumador actual"])
if respuestas["fumaba_2023"] in ["Exfumador", "Fumador actual"]:
    respuestas["paquetes_año"] = st.number_input("Paquetes-año aproximados", min_value=0.0, step=0.1)

respuestas["fumadores_casa"] = st.radio("¿Usted vivía con alguien que fumaba en la casa en el 2023?", ["Sí", "No", "No recuerdo"])
if respuestas["fumadores_casa"] == "Sí":
    respuestas["num_fumadores_casa"] = st.number_input("Número de fumadores en la vivienda (sin incluirlo)", min_value=1, step=1)

respuestas["combustibles"] = st.radio("¿Usaba combustibles sólidos/leña para cocinar o calefacción en el 2023?", ["Sí, frecuentemente", "A veces", "No"])
if respuestas["combustibles"] != "No":
    respuestas["tipo_combustible"] = st.multiselect("¿Qué combustible?", ["Leña", "Carbón", "Kerosene", "Gas", "Otro"])

respuestas["trabajo_expuesto"] = st.radio("¿Trabajó en 2023 en ocupaciones con exposición a carcinógenos respiratorios?", ["Sí", "No", "No recuerdo"])
if respuestas["trabajo_expuesto"] == "Sí":
    respuestas["ocupacion"] = st.text_input("Especifique la ocupación")

# --- Sección D ---
st.header("Sección D: Antecedentes médicos")
respuestas["cancer_pulmon"] = st.radio("¿ Usted tiene diagnóstico de cáncer de pulmón?", ["Sí", "No", "Prefiero no decir"])
if respuestas["cancer_pulmon"] == "Sí":
    respuestas["año_dx_cancer"] = st.number_input("Año del diagnóstico", min_value=1900, max_value=2025, step=1)

respuestas["enf_respiratoria"] = st.multiselect("¿ Usted tiene diagnóstico de enfermedad respiratoria crónica?", ["Asma", "EPOC", "Bronquitis crónica", "Ninguna", "Otro"])

respuestas["cancer_pulmon"] = st.radio("¿ Algun familiar con quien convivió con usted en la misma vivienda tiene diagnóstico de cáncer de pulmón?", ["Sí", "No", "Prefiero no decir"])

# --- Sección E ---
st.header("Sección E: Síntomas respiratorios. Instrucción: Marque si ha tenido estos síntomas desde 2023 hasta la fecha (2025). Para cada síntoma indique año aproximado de inicio si lo recuerda y la severidad actual (escala 1 = leve a 5 = muy severo)")
sintomas = ["Tos persistente", "Tos con sangre", "Disnea", "Pérdida de peso", "Dolor torácico", "Fatiga persistente"]
respuestas_sintomas = {}
for sintoma in sintomas:
    con_sintoma = st.checkbox(f"{sintoma}")
    if con_sintoma:
        inicio = st.number_input(f"Año de inicio de {sintoma}", min_value=1900, max_value=2025, step=1)
        severidad = st.slider(f"Severidad de {sintoma} (1=leve, 5=muy severo)", 1, 5, 1)
        respuestas_sintomas[sintoma] = {"inicio": inicio, "severidad": severidad}
respuestas["sintomas"] = respuestas_sintomas

# --- Sección F ---
st.header("Sección F: Impacto y acceso a salud")
respuestas["seguro_salud"] = st.radio("¿Cuenta con seguro de salud?", ["Sí, público", "Sí, privado", "No"])
respuestas["limitaciones_salud"] = st.radio("¿Tuvo limitaciones para acceder a salud desde 2023?", ["Sí", "No"])
if respuestas["limitaciones_salud"] == "Sí":
    respuestas["detalle_limitaciones"] = st.text_area("Explique brevemente")

# --- Sección G ---
st.header("Sección G: Disposición al seguimiento")
respuestas["cambio_sintomas"] = st.radio("¿Cómo evolucionaron sus síntomas?", ["Mejorado", "Empeorado", "Sin cambios", "No aplica"])
respuestas["contacto_profesional"] = st.radio("¿Desea que un profesional de salud lo contacte?", ["Sí", "No"])
if respuestas["contacto_profesional"] == "Sí":
    respuestas["contacto"] = st.text_input("Correo electrónico o teléfono (opcional)")
respuestas["comentarios"] = st.text_area("Comentarios adicionales")

# --- Botón Finalizar ---
if st.button("Enviar respuestas"):
    guardar_respuesta(respuestas)
    st.success("✅ Gracias, sus respuestas fueron registradas.")

       
