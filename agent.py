import groq
from extract_alternatives import extract_car_alternatives


# Imposta la tua API Key di Groq
GROQ_API_KEY = "apigroq"
client = groq.Client(api_key=GROQ_API_KEY)

def get_car_consultant_advice(car_model, kms_driven, car_age, estimated_value):

    prompt= f"""
    Eres un experto asesor de automóviles. Con base en la información proporcionada, proporciona:
    1. Los problemas comunes que pueden ocurrir con un {car_model} con {kms_driven} km recorridos.
    2. El consumo típico (consumo medio de combustible) de un {car_model}.
    3. Dos alternativas de autos similares según el valor de mercado en euro estimado para este vehículo ({estimated_value}).

    Responde de manera concisa y estructurada. Limita la respuesta a un máximo de 150 palabras.
    La respuesta debe estar exclusivamente en español.
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    text_response = response.choices[0].message.content

    # Estrai le alternative di auto
   # alternatives = extract_car_alternatives(text_response)

    # Cerca le immagini delle alternative su Google
   # alternative_images = [image_search.search_image(alt) for alt in alternatives]

    return  text_response
