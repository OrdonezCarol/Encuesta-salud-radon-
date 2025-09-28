import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, spearmanr

# Archivo para almacenar respuestas
RESPONSES_FILE = "responses.csv"

# Inicializar archivo si no existe
if not os.path.exists(RESPONSES_FILE):
    df = pd.DataFrame(columns=[
        "Edad", "Sexo", "Tiempo_residencia", "Tos_cronica", "Disnea", "Dolor_toracico",
        "Antecedente_familiar", "Consumo_tabaco"
    ])
    df.to_csv(RESPONSES_FILE, index=False)

# Cargar datos existentes
data = pd.read_csv(RESPONSES_FILE)

st.title("Encuesta: Salud respiratoria y exposición a radón (2023 → 2025)")

st.write("Por favor, complete las siguientes preguntas.")

# Formulario de encuesta
with st.form("radon_survey_form"):
    edad = st.number_input("Edad", min_value=15, max_value=100, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
    tiempo_residencia = st.number_input("¿Cuántos años vivió en la vivienda medida en 2023?", min_value=0, max_value=50)
    tos_cronica = st.radio("¿Presenta tos crónica (más de 3 meses)?", ["Sí", "No"])
    disnea = st.radio("¿Presenta dificultad para respirar (disnea)?", ["Sí", "No"])
    dolor_toracico = st.radio("¿Presenta dolor torácico recurrente?", ["Sí", "No"])
    antecedente_familiar = st.radio("¿Tiene antecedentes familiares de cáncer de pulmón?", ["Sí", "No"])
    consumo_tabaco = st.radio("¿Consume o consumió tabaco?", ["Sí", "No"])

    submitted = st.form_submit_button("Enviar")
    if submitted:
        new_data = pd.DataFrame({
            "Edad": [edad],
            "Sexo": [sexo],
            "Tiempo_residencia": [tiempo_residencia],
            "Tos_cronica": [tos_cronica],
            "Disnea": [disnea],
            "Dolor_toracico": [dolor_toracico],
            "Antecedente_familiar": [antecedente_familiar],
            "Consumo_tabaco": [consumo_tabaco]
        })
        new_data.to_csv(RESPONSES_FILE, mode='a', header=False, index=False)
        st.success("¡Gracias! Sus respuestas han sido registradas.")

# --- Panel de análisis estadístico en tiempo real ---
st.header("📊 Panel de análisis preliminar de respuestas")

if not data.empty:
    st.subheader("Frecuencias de síntomas")
    sintomas = ["Tos_cronica", "Disnea", "Dolor_toracico"]

    freq_table = data[sintomas].apply(pd.Series.value_counts)
    st.dataframe(freq_table)

    # Graficos de barras
    for col in sintomas:
        fig, ax = plt.subplots()
        data[col].value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f"Distribución de {col}")
        st.pyplot(fig)

    st.subheader("Distribución por edad")
    fig, ax = plt.subplots()
    data["Edad"].plot(kind='hist', bins=10, ax=ax, rwidth=0.8)
    ax.set_xlabel("Edad")
    ax.set_title("Histograma de edades")
    st.pyplot(fig)

    # --- Análisis bivariado ---
    st.header("🔎 Análisis bivariado: tiempo de residencia vs síntomas")
    for col in sintomas:
        st.subheader(f"Asociación entre tiempo de residencia y {col}")

        # Contingencia categórica
        contingency = pd.crosstab(data[col], pd.cut(data["Tiempo_residencia"], bins=3))
        st.write("Tabla de contingencia:")
        st.dataframe(contingency)

        try:
            chi2, p, dof, expected = chi2_contingency(contingency)
            st.write(f"Chi-cuadrado: {chi2:.2f}, p-valor: {p:.4f}")
        except:
            st.warning("No se pudo calcular chi-cuadrado (posiblemente por celdas vacías).");

    # --- Correlación de Spearman ---
    st.header("📈 Correlación de Spearman entre tiempo de residencia y número de síntomas")
    data_symptoms_numeric = data[sintomas].applymap(lambda x: 1 if x == "Sí" else 0)
    data["Total_sintomas"] = data_symptoms_numeric.sum(axis=1)

    corr, pval = spearmanr(data["Tiempo_residencia"], data["Total_sintomas"])
    st.write(f"Coeficiente rho de Spearman: {corr:.2f}, p-valor: {pval:.4f}")

    fig, ax = plt.subplots()
    ax.scatter(data["Tiempo_residencia"], data["Total_sintomas"])
    ax.set_xlabel("Tiempo de residencia (años)")
    ax.set_ylabel("Número de síntomas")
    ax.set_title("Relación entre tiempo de residencia y síntomas")
    st.pyplot(fig)

else:
    st.info("Aún no hay respuestas registradas.")

# --- Descarga de datos ---
st.header("🔐 Acceso de investigador")
password = st.text_input("Ingrese contraseña para descargar todas las respuestas:", type="password")
if password == "investigador2025":
    st.success("Acceso concedido. Puede descargar los datos.")
    st.download_button("Descargar respuestas en CSV", data.to_csv(index=False), file_name="respuestas.csv")
else:
    st.warning("Acceso restringido. Ingrese la contraseña correcta.")
