import streamlit as st
import pandas as pd
import os
st.markdown(
    """
    <style>
    .section-title {
        font-size: 28px !important;
        font-weight: bold;
        color: #0000FF;   /* blue */
        font-family: 'Georgia', serif;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
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

# ---  Consentimiento ---
st.markdown('<div class="section-title">Encuesta: Salud respiratoria y exposición a radón</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Consentimiento informado</div>', unsafe_allow_html=True)

consentimiento = st.radio(
   " Usted participó en un estudio en el que se realizaron mediciones de radón en su vivienda en el 2016-2019. Por tal motivo, le invitamos a participar en la presente investigación. Su participación es completamente voluntaria, anónima y confidencial, y puede retirarse en cualquier momento sin ninguna consecuencia. La encuesta tiene una duración de aproximadamente 10 minutos. ¿Acepta participar?",
    ["Sí, acepto", "No, no acepto"]
)

if consentimiento == "No, no acepto":
    st.warning("Gracias, la encuesta ha finalizado.")
    st.stop()

# Diccionario donde se guardarán las respuestas
respuestas = {"consentimiento": consentimiento}

# --- Sección A ---
st.markdown('<div class="section-title">Sección A: Datos generales del participante</div>', unsafe_allow_html=True)
respuestas["edad"] = st.number_input("Edad (años)", min_value=0, step=1)
respuestas["sexo"] = st.radio("Sexo", ["Femenino", "Masculino"])
respuestas["nivel_educativo actual"] = st.selectbox("Nivel educativo", ["Universitario en curso", "Titulado universitario", "Posgrado", "Técnico", "Otro"])
respuestas["ocupacion actual"] = st.selectbox("Ocupacion", ["Trabajador dependiente", "Trabajador independiente", "Desempleado", "Ama de casa", "Otro"])
respuestas["estado_civil actual"] = st.selectbox("Estado civil", ["Soltero", "Casado", "Viudo", "Divorciado", "Pareja conviviente"])
respuestas["distrito de residencia actual"] = st.text_input("Escriba el distrito")

# --- Sección B ---
st.markdown('<div class="section-title">Sección B: Vinculo con el monitoreo de radon</div>', unsafe_allow_html=True)
vivienda_actual = st.radio("¿Actualmente vive en la misma vivienda desde el 2016?", ["Sí", "No"])
respuestas["vive_misma_vivienda"] = vivienda_actual
if vivienda_actual == "No":
    respuestas["tiempo_vivio_2016_meses"] = st.number_input("¿Durante cuánto tiempo vivió en esa vivienda en 2016? (meses)", min_value=0, step=1)
respuestas["enf_respiratoria"] = st.multiselect("¿ Dónde colocó el dispositivo de monitoreo de radón?", ["Sala", "Cocina", "Dormitorio", "Baño", "Garaje", "Sotano", "Semisotano", "Primer piso","Segundo piso", "Otro"])

# --- Sección C ---
st.markdown('<div class="section-title">Sección C: Exposicion ambiental y laboral</div>', unsafe_allow_html=True)
respuestas["fumaba_2016"] = st.radio("¿Usted fuma?", ["Nunca fumé", "Exfumador", "Fumador actual"])
if respuestas["fumaba_2016"] in ["Exfumador", "Fumador actual"]:
    respuestas["paquetes_año"] = st.number_input("Paquetes-año aproximados", min_value=0.0, step=0.1)

respuestas["fumadores_casa"] = st.radio("¿Vive con alguien que fumaba?", ["Sí", "No", "No recuerdo"])
if respuestas["fumadores_casa"] == "Sí":
    respuestas["num_fumadores_casa"] = st.number_input("Número de fumadores en la vivienda (sin incluirlo)", min_value=1, step=1)

respuestas["combustibles"] = st.radio("¿Usa combustibles sólidos o leña para cocinar o calefacción en su vivienda?", ["Sí, frecuentemente", "A veces", "No"])
if respuestas["combustibles"] != "No":
    respuestas["tipo_combustible"] = st.multiselect("¿Qué combustible?", ["Leña", "Carbón", "Kerosene", "Gas", "Otro"])

respuestas["trabajo_expuesto"] = st.radio("¿Ha estado expuesto regularmente al humo del tabaco en su lugar de trabajo?", ["Sí", "No", "No recuerdo"], key="trabajo_expuesto_tabaco")
respuestas["trabajo_expuesto_carcinogenos"] = st.radio("¿Trabajó en ocupaciones con posibles agentes carcinogenos respiratorios como el asbesto?", ["Sí", "No", "No recuerdo"], key="trabajo_expuesto_carcinogenos")
if respuestas["trabajo_expuesto_carcinogenos"] == "Sí":
    respuestas["ocupacion_carcinogenos"] = st.text_input("Especifique la ocupación (mineria, soldadura, construccion, industria quimica, etc")

# --- Sección D ---
st.markdown('<div class="section-title">Sección D: Antecedentes médicos</div>', unsafe_allow_html=True)
respuestas["cancer_pulmon"] = st.radio("¿ Usted tiene diagnóstico de cáncer de pulmón?", ["Sí", "No", "Prefiero no decir"])
if respuestas["cancer_pulmon"] == "Sí":
    respuestas["año_dx_cancer"] = st.number_input("Año del diagnóstico", min_value=1900, max_value=2025, step=1)
respuestas["enf_respiratoria_cronica"] = st.multiselect("¿ Usted tiene diagnóstico de enfermedad respiratoria crónica?", ["Asma", "EPOC", "Bronquitis crónica", "Efisema pulmonar","Ninguna", "Otro"], key="enf_respiratoria_cronica")
respuestas["diabetes"] = st.radio("¿ Usted tiene diagnóstico de Diabetes mellitus?", ["Sí", "No", "Prefiero no decir"])
respuestas["hipertension"] = st.radio("¿ Usted tiene diagnóstico de Hipertension arterial?", ["Sí", "No", "Prefiero no decir"])
if respuestas["hipertension"] == "Sí":
    respuestas["cancer_pulmon_fam"] = st.radio("¿ Algun familiar con quien convivió con usted en la misma vivienda tiene diagnóstico de cáncer de pulmón?", ["Sí", "No", "Prefiero no decir"])
respuestas["enf_respiratoria_fam"] = st.multiselect("¿ Algun familiar con quien convivió con usted en la misma vivienda tiene diagnóstico de enfermedad respiratoria crónica?", ["Asma", "EPOC", "Bronquitis crónica", "Efisema pulmonar","Ninguna", "Otro"])

# --- Sección E ---
st.markdown('<div class="section-title">Sección E: Síntomas respiratorios</div>', unsafe_allow_html=True) 
st.markdown('<div class="section-title">Instrucción: Marque si ha tenido estos síntomas desde 2016 hasta la fecha (2025). Para cada síntoma indique año aproximado de inicio si lo recuerda y la severidad actual (escala 1 = leve a 5 = muy severo)</div>', unsafe_allow_html=True) 
sintomas = ["Tos persistente", "Tos con sangre", "Disnea", "Pérdida de peso", "Pérdida de apetito", "Fiebre o sensación de alza termica", "Dolor torácico", "Fatiga persistente"]
respuestas_sintomas = {}
for sintoma in sintomas:
    con_sintoma = st.checkbox(f"{sintoma}", key=f"sintoma_{sintoma}")
    if con_sintoma:
        inicio = st.number_input(f"Año de inicio de {sintoma}", min_value=1900, max_value=2025, step=1, key=f"inicio_{sintoma}")
        severidad = st.slider(f"Severidad de {sintoma} (1=leve, 5=muy severo)", 1, 5, 1)
        respuestas_sintomas[sintoma] = {"inicio": inicio, "severidad": severidad}
respuestas["sintomas"] = respuestas_sintomas

# --- Sección F ---
st.markdown('<div class="section-title">Sección F: Identificación de barreras de acceso a servicios de salud</div>', unsafe_allow_html=True) 
respuestas["seguro"] = st.radio("¿Cuenta con seguro médico de salud", ["Sí", "No"])
if respuestas["seguro"] == "Sí":
    respuestas["tipo_seguro"] = st.multiselect("¿ Qué tipo de seguro medico de salud?", ["Essalud", "SIS", "Privado", "Seguro universitario", "Otro"])
respuestas["economico"] = st.radio("¿Usted ha dejado de acudir a consultas médicas por motivos económicos?", ["Sí", "No"])
respuestas["distancia"] = st.radio("¿Usted encuentra dificultades para acceder a servicios de salud debido a la distancia?", ["Sí", "No"])
respuestas["sinatenccion"] = st.radio("¿En algún centro de salud lo han dejado de atender por su condición de étnica, orientación sexual o discapacidad?", ["Sí", "No"])
respuestas["creencias"] = st.radio("¿Ha dejado de realizarse procedimientos médicos por sus creencias religiosas o culturales?", ["Sí", "No"])
respuestas["discriminacion"] = st.radio("¿Ha experimentado discriminación o falta de comprensión cultural por parte del personal médico en el centro de salud que se atiende?", ["Sí", "No"])

# --- Botón Finalizar ---
if st.button("Enviar respuestas"):
    guardar_respuesta(respuestas)
    st.success("✅ Gracias, sus respuestas fueron registradas.")
