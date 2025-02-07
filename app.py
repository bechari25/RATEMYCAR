import numpy as np
import pandas as pd
import pickle as pkl
import streamlit as st
from ricerca import RicercaImmagini
from agent import get_car_consultant_advice

API_KEY = "api"
SEARCH_ENGINE_ID = "engineid"

# Cargar el modelo entrenado
model = pkl.load(open("models/random_forest_regression_model (1).pkl", "rb"))

# Cargar los datos para las selecciones
car_data = pd.read_csv("data/car data.csv")
car_data["Car_Name"] = car_data["Car_Name"].apply(lambda x: x.split(" ")[0])

# Inicializar el objeto de búsqueda de imágenes
ricerca = RicercaImmagini(API_KEY, SEARCH_ENGINE_ID)

# Función para convertir rupias a euros
def convert_rupia_to_euro(amount):
    exchange_rate = 0.011  # Tasa de cambio hipotética
    return round(amount * exchange_rate, 2)

# Almacenar los resultados para que no desaparezcan
if "predicted_price_eur" not in st.session_state:
    st.session_state.predicted_price_eur = None
if "car_image_url" not in st.session_state:
    st.session_state.car_image_url = None
if "ai_tips" not in st.session_state:
    st.session_state.ai_tips = None

# CSS para personalizar el título
st.markdown(
    """
    <style>
        .header-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .custom-title {
                    font-size: 48px;
            font-weight: bold;
            color: #2E3B55;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            background: linear-gradient(45deg, #FFA500, #FF4500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .logo {
            max-width: 120px;
        }
    </style>
    <div class="header-container">
        <h1 class="custom-title">🚗 RateMyCar</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Diseño con dos columnas (30% parámetros - 70% resultados)
col_parametros, col_resultados = st.columns([1, 2])

with col_parametros:
    st.markdown("<h3>🚘 Ingresa los datos de tu coche</h3>", unsafe_allow_html=True)
    car_name = st.selectbox("Marca del coche", car_data["Car_Name"].unique())
    year = st.slider("Año de fabricación", 2003, 2017)
    kms_driven = st.slider("Kilómetros recorridos", 500, 500000)
    fuel_type = st.selectbox("Tipo de combustible", car_data["Fuel_Type"].unique())
    transmission = st.selectbox("Tipo de transmisión", car_data["Transmission"].unique())
    owner = st.selectbox("Número de propietarios anteriores", car_data["Owner"].unique())
    present_price_euro = st.slider("Precio del coche nuevo (€)", 3000, 100000)

    # Conversión a rupias para el modelo
    present_price_rupie = present_price_euro * 90

if st.button("🔍 Predecir precio"):
    # Preparar los datos para la predicción
    x_test = pd.DataFrame([[present_price_rupie, kms_driven, owner, year, fuel_type, transmission]],
                           columns=['Present_Price', 'Kms_Driven', 'Owner', 'Year', 'Fuel_Type', 'Transmission'])

    # Convertir 'Year' en 'no_year' y eliminar 'Year'
    x_test['no_year'] = 2025 - x_test['Year']
    x_test.drop(['Year'], axis=1, inplace=True)

    # One-Hot Encoding de las variables categóricas
    x_test = pd.get_dummies(x_test, drop_first=True)

    # Asegurar que todas las características esperadas estén presentes en el modelo
    expected_features = ['Present_Price', 'Kms_Driven', 'Owner', 'no_year',
                         'Fuel_Type_Diesel', 'Fuel_Type_Petrol', 'Transmission_Manual']

    for feature in expected_features:
        if feature not in x_test.columns:
            x_test[feature] = 0

    # Reordenar las columnas para que coincidan con el modelo
    x_test = x_test[expected_features]

    # Escalar el precio
    x_test['Present_Price'] = x_test['Present_Price'] * (10 ** (-5))

    # Realizar la predicción
    selling_price_predicted = model.predict(x_test)
    predicted_price_inr = round(selling_price_predicted[0] * (10 ** 5), 2)
    st.session_state.predicted_price_eur = predicted_price_inr / 90

    # Obtener la imagen del coche a través de Google Custom Search
    st.session_state.car_image_url = ricerca.get_car_image_google(car_name)

    # Generar consejos de mantenimiento
    car_age = 2024 - year
    st.session_state.ai_tips = get_car_consultant_advice(car_name, kms_driven, car_age, round(predicted_price_inr/90))

# En la columna derecha mostramos la imagen, el precio y los consejos
with col_resultados:
    if st.session_state.predicted_price_eur is not None:
        st.success(f"💰 Precio estimado: €{round(st.session_state.predicted_price_eur)}")

    if st.session_state.car_image_url:
        st.image(st.session_state.car_image_url, caption=f"{car_name}", use_container_width=True)
    else:
        st.warning("❌ ¡No se encontró ninguna imagen!")

    if st.session_state.ai_tips:
        st.subheader("💵 Nuestros consejos")
        st.write(st.session_state.ai_tips)
