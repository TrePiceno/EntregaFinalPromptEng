# main.py is intentionally left empty

# PROMPTS USADOS EN EN CHAT DE COPILOT

# 1. Creame un archivo main.py vacío y guarda las dependencias del entorno virtual en un nuevo archivo que creeras llamado requirements.txt

# 2. Crea un archivo llamado requirements.txt y guarda las dependencias del entorno virtual

# 3. Esas no son las dependencias del entorno virtual. Es en en la carpeta .venv/Lib/site-packages. Accede ahí y guarda un listado de las dependencias instaladas en el archivo requirements.txt recien creado. 

# Me dio el comando para hacerlo manualmente: pip freeze > requirements.txt

# 4. Puedes crear un asistente que analize palabras clave y sugiera estrategias para mejorar el posicionamiento web, intengrando el modelo de IA. También que se integre con Google Search Console y herremientas de analisis de SEO. Esto será una página en Streamlit.

# 5. Podrias modificarlo en los siguentes aspectos:

# Que todo este en español.
# Que permita seleccionar de 1 a 5 palabras clave principales, de 1 a 5 palabras clave secundarias y de 1 a 5 palabras clave long-tail (Fraes más largas y especificas).
# Genera con la IA títulos, meta descripciones y keywords optimizados para usar.

# streamlit run main.py comando para ejecutar la app

# 6. Solución de unos errores

# ----------------------------------------------------------------

import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["api_key"])

# Function to generate keyword suggestions
def generate_keyword_suggestions(business_activity, num_keywords):
    prompt = f"""
    Genera {num_keywords} palabras clave relevantes para SEO, relacionadas con la siguiente actividad de negocio: {business_activity}.
    Proporciona las palabras clave en español.  Solo dame las palabras clave, una por línea, sin numeración ni texto adicional.
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    return [line.strip() for line in chat_completion.choices[0].message.content.split('\n') if line.strip()]

# Function to get SEO suggestions from Groq
def get_seo_suggestions(selected_keywords):
    prompt = f"""
    Analiza las siguientes palabras clave para SEO: {', '.join(selected_keywords)}.

    Sugiere:
    1. Títulos optimizados para SEO (máximo 60 caracteres).
    2. Meta descripciones optimizadas para SEO (máximo 160 caracteres).
    3. Una lista de keywords optimizadas para usar en el contenido.

    Proporciona sugerencias en español.
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    return chat_completion.choices[0].message.content

# Streamlit UI
st.title("Asistente de Análisis de Palabras Clave SEO")

# Sidebar
with st.sidebar:
    st.header("Acerca de este Asistente")
    st.write("Este asistente te ayuda a encontrar palabras clave relevantes para SEO y a obtener sugerencias para optimizar tu contenido.")
    st.write("1. Describe tu negocio.")
    st.write("2. Elige cuántas palabras clave generar.")
    st.write("3. Selecciona las palabras clave que te interesan.")
    st.write("4. Obtén sugerencias de SEO.")

# Business Activity Input
business_activity = st.text_input("Describe la actividad de tu negocio:")

# Number of Keywords Selection
num_keywords = st.selectbox("¿Cuántas palabras clave quieres generar?", list(range(1, 21)))

# Generate keyword suggestions only when business_activity or num_keywords changes
if 'keyword_suggestions' not in st.session_state or st.session_state.business_activity != business_activity or st.session_state.num_keywords != num_keywords:
    st.session_state['keyword_suggestions'] = generate_keyword_suggestions(business_activity, num_keywords)
    st.session_state.business_activity = business_activity
    st.session_state.num_keywords = num_keywords
    st.session_state.selected_keywords = []  # Clear selected keywords when new suggestions are generated

if 'selected_keywords' not in st.session_state:
    st.session_state['selected_keywords'] = []

# Keyword Selection
st.subheader("Selecciona las palabras clave que deseas usar:")

for i, keyword in enumerate(st.session_state['keyword_suggestions']):
    checkbox_key = f"keyword_{i}"
    is_selected = st.checkbox(keyword, key=checkbox_key, value=(keyword in st.session_state['selected_keywords']))

    if is_selected:
        if keyword not in st.session_state['selected_keywords']:
            st.session_state['selected_keywords'].append(keyword)
    else:
        if keyword in st.session_state['selected_keywords']:
            st.session_state['selected_keywords'].remove(keyword)

if st.button("Obtener Sugerencias SEO"):
    if not st.session_state['selected_keywords']:
        st.error("Por favor, selecciona al menos una palabra clave.")
    else:
        st.subheader("Sugerencias SEO:")
        seo_suggestions = get_seo_suggestions(st.session_state['selected_keywords'])
        st.write(seo_suggestions)

st.markdown("---")
st.markdown("Esta es una herramienta para el análisis de palabras clave SEO.  Utiliza la API de Groq para proporcionar sugerencias basadas en las palabras clave seleccionadas.")