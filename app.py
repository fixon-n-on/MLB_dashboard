import streamlit as st
import pandas as pd
import altair as alt

# Cargar el nuevo archivo de datos
st.set_page_config(page_title="Dashboard Completo", layout="wide")
df = pd.read_csv("archivo_completo.csv")

st.title("📊 Dashboard General de Jugadores de Béisbol")

# Filtros por equipo y posición
equipos = df['team'].unique()
posiciones = df['position'].unique()
equipo_seleccionado = st.sidebar.multiselect("Selecciona equipo(s):", equipos, default=equipos)
posicion_seleccionada = st.sidebar.multiselect("Selecciona posición(es):", posiciones, default=posiciones)

# Filtrar el dataframe según selección
df_filtrado = df[(df['team'].isin(equipo_seleccionado)) & (df['position'].isin(posicion_seleccionada))]

# Tabla de datos
st.subheader("📋 Tabla de Jugadores Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Métricas generales
col1, col2, col3 = st.columns(3)
col1.metric("Total HR", int(df_filtrado['hr_total'].sum()))
col2.metric("HR Promedio por Jugador", round(df_filtrado['hr_total'].mean(), 1))
col3.metric("Promedio HR trot (s)", round(df_filtrado['avg_hr_trot'].mean(), 2))

# Tabs para visualizaciones
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏏 HR Totales",
    "⚾ HR vs XHR",
    "⏱️ Promedio de Trotada",
    "📊 % HR sin Duda",
    "📶 Doubters vs No Doubters",
    "🌟 Shohei Ohtani"
])

# Tab 1: HR Totales
with tab1:
    st.subheader("Home Runs Totales por Jugador")
    chart = alt.Chart(df_filtrado).mark_bar().encode(
        x=alt.X('player', sort='-y'),
        y='hr_total',
        color='team'
    ).properties(width=800, height=400)
    st.altair_chart(chart, use_container_width=True)

# Tab 2: HR vs XHR
with tab2:
    st.subheader("HR Totales vs HR Esperados")
    scatter = alt.Chart(df_filtrado).mark_circle(size=90).encode(
        x='xhr',
        y='hr_total',
        tooltip=['player', 'xhr', 'hr_total'],
        color='team'
    ).interactive().properties(width=800, height=400)
    st.altair_chart(scatter, use_container_width=True)

# Tab 3: Promedio de trotada
with tab3:
    st.subheader("Promedio de Trotada por Jugador")
    trot = alt.Chart(df_filtrado).mark_bar().encode(
        x=alt.X('player', sort='-y'),
        y='avg_hr_trot',
        color='team'
    ).properties(width=800, height=400)
    st.altair_chart(trot, use_container_width=True)

# Tab 4: % HR sin duda
with tab4:
    st.subheader("Porcentaje de HR sin Duda")
    doubt = alt.Chart(df_filtrado).mark_bar().encode(
        x=alt.X('player', sort='-y'),
        y='no_doubter_per',
        color='team'
    ).properties(width=800, height=400)
    st.altair_chart(doubt, use_container_width=True)

# Tab 5: Comparación de Doubters
with tab5:
    st.subheader("Comparación de HR: Doubters vs No Doubters")
    df_melted = df_filtrado.melt(id_vars=['player', 'team'], 
                                 value_vars=['doubters', 'no_doubters'], 
                                 var_name='Tipo', value_name='Cantidad')
    stacked = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X('player:N', sort='-y'),
        y='Cantidad:Q',
        color=alt.Color('Tipo:N'),
        tooltip=['player', 'Tipo', 'Cantidad']
    ).properties(width=800, height=400)
    st.altair_chart(stacked, use_container_width=True)

# Tab 6: Shohei Ohtani
with tab6:
    st.subheader("Estadísticas de Shohei Ohtani")
    ohtani_df = df_filtrado[df_filtrado['player'].str.contains("Shohei Ohtani", case=False)]

    if not ohtani_df.empty:
        st.write(ohtani_df[['team', 'position', 'hr_total', 'xhr', 'avg_hr_trot', 'no_doubter_per']])

        ohtani_chart = alt.Chart(ohtani_df).transform_fold(
            ['hr_total', 'xhr']
        ).mark_bar().encode(
            x=alt.X('key:N', title='Tipo HR'),
            y=alt.Y('value:Q', title='Cantidad'),
            color='key:N'
        ).properties(width=600, height=400)
        st.altair_chart(ohtani_chart, use_container_width=True)
    else:
        st.info("Shohei Ohtani no está en los datos filtrados.")

st.caption("Fuente: archivo_completo.csv")
