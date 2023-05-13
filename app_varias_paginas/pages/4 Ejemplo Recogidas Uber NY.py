import streamlit as st
import pandas as pd
import numpy as np

st.title('Recogidas de Uber en Nueva York 🚖')

# Comencemos escribiendo una función para cargar los datos.

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


# Envolvemos la función en un decorador de caché de datos para que no se vuelva a ejecutar cada vez que se cambia un widget en la barra lateral o se vuelve a ejecutar la aplicación.
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Ahora probemos la función y revisemos el resultado


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Cargando datos... ⏳')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Datos cargados ...¡Hecho! ✅')

# Ahora que tenemos los datos, podemos imprimir una tabla de resumen y un histograma de las horas de recogida de Uber en Nueva York por hora del día.

st.checkbox('Mostrar datos en bruto 📊')
st.subheader('Datos en bruto ')
st.write(data)

st.subheader('Numero de recogidas de Uber por hora ⏰')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

#Trazar datos en un mapas

st.subheader('Mapa de todas las recogidas de Uber en Nueva York 🗺️')
st.map(data)

# Filtrar datos y trazar mapas interactivos
# min: 0h, max: 23h, default: 17h
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Mapa de todas las recogidas de Uber a las {hour_to_filter}:00')
st.map(filtered_data)
